# LEFT JOIN

A `LEFT JOIN` keeps every row from the table on the left. Matching right rows add their values. If no right row matches, right-side columns are `NULL`.

```sql
WITH customers(customer_id, name) AS (
  VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara')
), orders(order_id, customer_id) AS (
  VALUES (10, 1), (11, 1), (12, 2)
)
SELECT c.customer_id, c.name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
ORDER BY c.customer_id, o.order_id;
```

The rows are `(1, 'Ana', 10)`, `(1, 'Ana', 11)`, `(2, 'Ben', 12)`, and `(3, 'Cara', NULL)`. Ana appears twice because she has two orders. Cara appears because the left side is kept even without a match. A left join never promises exactly one result row for each left row.

## Count matches without losing zeroes

```sql
WITH customers(customer_id) AS (VALUES (1), (2), (3)),
     orders(order_id, customer_id) AS (
       VALUES (10, 1), (11, 1), (12, 2)
     )
SELECT c.customer_id, COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY c.customer_id;
```

The counts are 2, 1, and 0. `COUNT(o.order_id)` ignores the `NULL` added for Cara. `COUNT(*)` would count Cara's joined row and report 1, which is wrong for an order count. This works because `order_id` is never null for a real order.

A `WHERE` condition on a right-table column can discard the unmatched rows. To count only paid orders while keeping every customer, put `o.status = 'paid'` in `ON`, or use conditional aggregation. Check that the chosen rule matches the report.

## Check your understanding

1. Why does Ana appear twice?
2. Why does `COUNT(*)` give the wrong order count for Cara?
3. Where could a paid-order restriction go if Cara must stay in the result?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
