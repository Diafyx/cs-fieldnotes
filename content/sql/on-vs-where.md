# ON vs. WHERE

`ON` decides which rows from two tables match. `WHERE` filters rows after the join result is made. With an inner join, a simple condition can often go in either place. With an outer join, moving a condition can change which unmatched rows survive.

```sql
WITH customers(customer_id) AS (VALUES (1), (2)),
     orders(order_id, customer_id, status) AS (
       VALUES (10, 1, 'paid'), (11, 1, 'pending')
     )
SELECT c.customer_id, o.order_id
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id AND o.status = 'paid'
ORDER BY c.customer_id;
```

This returns `(1, 10)` and `(2, NULL)`. Customer 2 remains because the left join keeps customers. The `ON` condition only allows paid orders to match. Customer 1's pending order is ignored.

If `o.status = 'paid'` is moved to `WHERE`, customer 2 is removed. Its unmatched row has `NULL` for `o.status`, and that comparison is not true. The result then has only `(1, 10)`.

```sql
WITH customers(customer_id) AS (VALUES (1), (2)),
     orders(order_id, customer_id, status) AS (
       VALUES (10, 1, 'paid'), (11, 1, 'pending')
     )
SELECT c.customer_id, o.order_id
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.status = 'paid'
ORDER BY c.customer_id;
```

## Use each clause for its job

Put the relationship and restrictions on which right rows may match in `ON`. Put filters on the finished result in `WHERE`. A filter on the left table, such as `WHERE c.customer_id > 1`, intentionally removes left rows too.

Sometimes you *want* to remove unmatched rows after a left join. `WHERE o.order_id IS NOT NULL` keeps only customers with a matched order. If the goal is customers without an order, use `WHERE o.order_id IS NULL` after joining on the order key. Make sure the tested right column cannot be `NULL` in a real matched row.

## Check your understanding

1. Why does customer 2 survive when the status test is in `ON`?
2. What happens to customer 2 when the status test moves to `WHERE`?
3. Which clause should hold a filter that removes customers from the final result?

## Further reading

- [PostgreSQL ON and WHERE in joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
