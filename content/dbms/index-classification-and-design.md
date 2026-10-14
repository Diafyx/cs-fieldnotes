# Index Classification and Design

An index is a separate structure that helps a database find table rows. A good index matches a real search, join, or ordering pattern. It uses storage and adds work to writes, so index design starts with queries and measured plans.

## Ways to classify an index

| Classification | Meaning |
| --- | --- |
| Unique or non-unique | A unique index rejects duplicate key values under its SQL rules. A non-unique index allows several rows per key. |
| Single or multicolumn | One key column, or an ordered list of key columns. The order matters for many access methods. |
| Full or partial | A full index includes qualifying entries from all table rows. A partial index includes only rows meeting its predicate. |
| Plain or expression | A plain index uses stored column values. An expression index stores a computed key such as `lower(email)`. |
| Covering | The index has every column a query needs, possibly with extra included columns. A heap visit may still be needed for visibility. |

Textbooks also distinguish **primary** and **secondary**, **dense** and **sparse**, and **clustered** and **unclustered** indexes. A dense index has an entry for each search-key value or row pointer; a sparse index has entries for selected data pages and relies on ordered data between them. A clustered layout puts table rows near an index's key order, while an unclustered index points to rows spread through the table. These terms describe physical designs, and their exact meaning varies across products. In PostgreSQL, a primary key creates a unique B-tree index, but it does not keep heap rows in key order.

## Pick the access method

PostgreSQL offers several index types. B-tree is the default and handles equality, ranges, and ordered scans. Hash handles equality only. GIN is useful when a value contains searchable parts, such as array elements. GiST and SP-GiST support operator-specific searches such as spatial data. BRIN stores small summaries of ranges of table pages and can help on large tables whose indexed values follow physical row order. The operator and data type must be supported by the chosen index type.

An index does not force a plan. The planner may prefer a table scan when many rows match or the table is small. A bitmap scan can combine index matches and visit heap pages in batches. Use `EXPLAIN (ANALYZE, BUFFERS)` on realistic data when a query is slow; `ANALYZE` actually runs the query, so use care with writes.

## Design from one query

Suppose a page shows a customer's newest orders. It filters by customer, then sorts by date and ID:

```sql
CREATE TEMP TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    placed_at DATE NOT NULL,
    amount INTEGER NOT NULL
);

INSERT INTO orders VALUES
    (1, 10, DATE '2026-01-02', 20),
    (2, 10, DATE '2026-01-03', 30),
    (3, 20, DATE '2026-01-04', 40),
    (4, 10, DATE '2026-01-03', 50);

CREATE INDEX orders_customer_recent_idx
ON orders (customer_id, placed_at DESC, order_id DESC);

SELECT order_id, amount
FROM orders
WHERE customer_id = 10
ORDER BY placed_at DESC, order_id DESC
LIMIT 2;
```

The result is `(4, 50)` followed by `(2, 30)`. The leading `customer_id` supports the equality filter. The next keys can support the requested order within that customer. The ID breaks the date tie, so repeated runs ask for the same two rows. The index still may not be used on this tiny table.

For an index on `(customer_id, placed_at)`, a condition on `customer_id` is a strong match for the leading key. A condition only on `placed_at` often cannot use it as efficiently. Check the actual PostgreSQL version and plan before treating any simple left-prefix rule as absolute; the planner has several access paths.

## Costs and traps

Every extra index consumes space and needs updates when indexed values change. It can also reduce the chance of a HOT update. Primary keys and unique constraints create indexes in PostgreSQL, but a foreign key does not automatically index the referencing column. An index on a low-selectivity flag may have little value for a query that reads most rows; a partial index can help if it covers a small, often queried subset.

A covering index is useful only when its columns and visibility conditions let the query avoid enough heap work. PostgreSQL's visibility map matters for index-only scans. Do not duplicate an existing index without comparing its leading keys, predicate, included columns, and workload. The goal is enough useful indexes, not the maximum possible number.

## Try it yourself

1. Why is `customer_id` first in the example index?
2. Why is `order_id` included in the ordering even though `placed_at` is already sorted?
3. Why might a covering index still read heap pages?

## References

- [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html)
- [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html)
- [PostgreSQL index-only scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
