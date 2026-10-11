# IMPLICIT JOIN

An implicit join lists tables with commas and puts the matching condition in `WHERE`. It can produce the same rows as an inner join, but the relationship is less visible in a long query.

```sql
WITH customers(customer_id, name) AS (
  VALUES (1, 'Ana'), (2, 'Ben')
), orders(order_id, customer_id) AS (
  VALUES (10, 1), (11, 1)
)
SELECT o.order_id, c.name
FROM customers AS c, orders AS o
WHERE c.customer_id = o.customer_id
ORDER BY o.order_id;
```

The result is `(10, 'Ana')` and `(11, 'Ana')`. The comma first makes possible customer-order pairs; the `WHERE` condition keeps matching pairs. An explicit `INNER JOIN ... ON c.customer_id = o.customer_id` expresses the same relationship here.

## Watch for a missing condition

If the `WHERE` condition is left out, this example returns four rows: two customers times two orders. Larger tables can make many more unintended pairs. A filter such as `WHERE c.name = 'Ana'` is not enough to connect an order to the right customer.

The comma form cannot directly express a left, right, or full outer join. For those, use explicit join syntax. Mixing commas and `JOIN` in one `FROM` clause can also make table scope hard to follow because `JOIN` binds more tightly. Prefer explicit joins when writing or editing a multi-table query.

## Check your understanding

1. How many rows would the sample return without its `WHERE` condition?
2. What explicit join matches this example?
3. Why does filtering by a customer's name alone fail to connect orders correctly?

## Further reading

- [PostgreSQL table expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-FROM)
