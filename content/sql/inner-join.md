# INNER JOIN

An `INNER JOIN` returns pairs of rows whose join condition is true. Rows with no match on the other side do not appear.

```sql
WITH customers(customer_id, name) AS (
  VALUES (1, 'Ana'), (2, 'Ben')
), orders(order_id, customer_id) AS (
  VALUES (10, 1), (11, 1), (12, 99)
)
SELECT o.order_id, c.name
FROM orders AS o
INNER JOIN customers AS c
  ON c.customer_id = o.customer_id
ORDER BY o.order_id;
```

The result is `(10, 'Ana')` and `(11, 'Ana')`. Ben has no order. Order 12 has no customer row in this sample, so neither appears in the joined output. A real foreign key could prevent such an orphan order from being stored.

`JOIN` by itself means `INNER JOIN` in PostgreSQL. Write the full form when it helps a reader. A matching customer can appear more than once if several orders point to them. If both sides have repeated values in the join key, every matching pair is returned, so counts can grow quickly.

## Put all key parts in the match

If order IDs are only unique inside a store, joining order lines to orders needs both `store_id` and `order_id`:

```sql
SELECT l.line_id, o.ordered_on
FROM order_lines AS l
JOIN orders AS o
  ON o.store_id = l.store_id AND o.order_id = l.order_id;
```

Matching only `order_id` could attach a line to the wrong store's order. An inner join also does not match two `NULL` key values with ordinary `=`. If missing keys should match, that needs an explicit rule and careful thought about what a missing key means.

## Check your understanding

1. Why is order 12 absent from the first result?
2. Why can Ana appear twice after this join?
3. What error could occur if `store_id` were omitted from the second join condition?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
