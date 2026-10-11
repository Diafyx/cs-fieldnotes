# Non-Recursive CTEs

A non-recursive CTE calculates a named result without referring to itself. You can build several steps and reuse an earlier result in the same statement. This is useful when an aggregate or filter would otherwise be repeated.

## Compare totals with their average

```sql
WITH orders(customer_id, amount) AS (
  VALUES (1, 20), (1, 40), (2, 10), (2, 10), (3, 30)
), totals AS (
  SELECT customer_id, SUM(amount) AS total
  FROM orders
  GROUP BY customer_id
)
SELECT customer_id, total
FROM totals
WHERE total > (SELECT AVG(total) FROM totals)
ORDER BY customer_id;
```

The customer totals are 60, 20, and 30. Their average is about 36.67, so only `(1, 60)` remains. The `totals` CTE is used by both the outer query and the scalar subquery. The comparison is against the average of customer totals, not the average of individual order amounts.

## How PostgreSQL may run it

A CTE is a way to express the query, not a promise that PostgreSQL will build a separate temporary table. A side-effect-free, non-recursive CTE referenced once is normally folded into its parent query. A CTE referenced more than once is normally calculated separately. PostgreSQL lets you request `MATERIALIZED` or `NOT MATERIALIZED` when you need to influence that choice. Forcing separate calculation can save repeated work, but can also stop an outer filter from being pushed down. Inspect `EXPLAIN` on real data before choosing a hint for speed.

If there are no orders, `totals` has no rows and the final query returns no rows. `AVG(total)` would be `NULL`, not zero. A CTE can make a query easier to read even when it is only used once; use names that describe the rows they hold.

## Check your understanding

1. Why is the comparison value about 36.67 rather than 22?
2. What does the query return with no orders?
3. Does writing `WITH totals AS (...)` guarantee a stored intermediate table?

## Further reading

- [PostgreSQL CTE materialization](https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-CTE-MATERIALIZATION)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
