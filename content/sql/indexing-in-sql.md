# Indexing in SQL

An index is a data structure that helps a database find rows for some queries. It can make a selective search much faster than reading every row. It also takes space and must be updated when indexed data changes. The right index follows a real query pattern, not a rule that every column should have one.

The examples here use PostgreSQL B-tree indexes, which are a common choice for equality, range, and ordered searches.

## Start from the query

Suppose a page shows a customer's latest orders:

```sql
SELECT order_id, placed_at, amount
FROM orders
WHERE customer_id = 10
ORDER BY placed_at DESC, order_id DESC
LIMIT 20;
```

A possible index for this pattern is:

```sql
CREATE INDEX orders_customer_recent_idx
ON orders (customer_id, placed_at DESC, order_id DESC);
```

The leading column helps locate one customer's orders. The next columns match the requested order. This does not guarantee the planner will use the index. On a tiny table, a scan can be cheaper. The planner also considers how many rows it expects to match and what data must still be read from the table.

## Column order matters

A multicolumn B-tree index is generally most efficient when a query constrains its leading columns. An index on `(customer_id, placed_at)` fits a query that starts with `customer_id = ...`. It is not the same as an index on `(placed_at, customer_id)`. Both indexes may be useful for different workloads, but each has a cost.

Primary keys and unique constraints create indexes in PostgreSQL. A foreign key does not automatically create an index on the referencing column. If `orders.customer_id` is a foreign key and the table is large, check whether queries and parent-row updates need an index there.

## Check instead of guessing

```sql
EXPLAIN
SELECT order_id, placed_at, amount
FROM orders
WHERE customer_id = 10
ORDER BY placed_at DESC, order_id DESC
LIMIT 20;
```

Look at the chosen scan, estimated rows, and sort. On a test database with realistic data, `EXPLAIN ANALYZE` adds actual measurements. A single fast query is not the whole story. Measure the write cost and storage cost too, especially on tables with frequent inserts or updates.

## Avoid common index mistakes

- Do not add an index to every column. More indexes make writes and maintenance more expensive.
- Do not expect an index to help when a query returns most of the table. A scan may be better.
- Do not judge an index only with a nearly empty development table.
- Do not assume a foreign key declaration indexed both tables.
- Do not add several overlapping indexes without checking which queries use each one.

## Check your understanding

1. Why is `customer_id` the first column in the example index?
2. Why might PostgreSQL scan a small table even when a matching index exists?
3. What work does each extra index add when an order is inserted?

## Further reading

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL examining index usage](https://www.postgresql.org/docs/current/indexes-examine.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
