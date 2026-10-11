# Joins Deep Dive

A join combines rows from tables using a relationship. An order can carry `customer_id`, while the customer table carries the name. A join lets a query show the order beside that name.

## Match rows by a key

```sql
WITH customers(customer_id, name) AS (
  VALUES (1, 'Ana'), (2, 'Ben')
), orders(order_id, customer_id) AS (
  VALUES (10, 1), (11, 1)
)
SELECT o.order_id, c.name
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
ORDER BY o.order_id;
```

The result is `(10, Ana)` and `(11, Ana)`. `o` and `c` are short names for the tables. The `ON` condition says which customer belongs to each order. In a real table, a primary key on `customers.customer_id` would mean each order can match at most one customer. If a customer has three orders, that customer can still appear in three result rows. Joins do not promise one output row per customer.

## Choose which unmatched rows to keep

An `INNER JOIN` keeps matching pairs only. A `LEFT JOIN` also keeps each unmatched row from the left table, with `NULL` in columns from the right. A `RIGHT JOIN` does the reverse. A `FULL OUTER JOIN` keeps unmatched rows from both sides. A `CROSS JOIN` makes every possible pair and has no match condition.

An outer join can multiply rows too. If one customer has two matching orders, a left join returns two rows for that customer. `COUNT(*)` then counts joined rows, not customers. When you need one row per customer, group by customer or join to a query that already has one row per customer.

## Check the relationship

Match on every column that defines the relationship. If order numbers restart in each store, join on both `store_id` and `order_id`. Joining only on `order_id` can connect unrelated rows. A missing key normally does not match another missing key because `NULL = NULL` is not true.

`ON` determines matches. `WHERE` filters the joined result. For outer joins, putting a right-table filter in `WHERE` can remove the rows the outer join was meant to keep. Check the [ON vs. WHERE](/topics/sql/on-vs-where.html) page before adding such a filter.

For large tables, indexes on join keys can help, but the database chooses a plan based on table sizes and filters. First make the result correct. Then inspect the plan if the query is slow.

## Check your understanding

1. Why can one customer appear three times after joining to orders?
2. Which join keeps customers who have no orders?
3. Why might joining on `order_id` alone be wrong when several stores use the same numbers?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
