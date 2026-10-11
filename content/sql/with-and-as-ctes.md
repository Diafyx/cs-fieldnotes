# WITH and AS (CTEs)

`WITH` starts a list of named query results. `AS` connects each name to its query. The main statement can use those names like small input tables. This makes a long query easier to read when each step has a clear job.

## Name two steps

```sql
WITH orders(customer_id, amount) AS (
  VALUES (1, 20), (1, 40), (2, 10), (3, 35)
), customer_totals AS (
  SELECT customer_id, SUM(amount) AS total
  FROM orders
  GROUP BY customer_id
), large_totals AS (
  SELECT customer_id, total
  FROM customer_totals
  WHERE total >= 35
)
SELECT customer_id, total
FROM large_totals
ORDER BY customer_id;
```

The rows are `(1, 60)` and `(3, 35)`. `orders` supplies the sample rows. `customer_totals` groups them. `large_totals` filters the grouped results. The final `SELECT` sorts the answer. Each later CTE can refer to one defined earlier in this non-recursive list.

The column list after `orders` gives names to the columns returned by `VALUES`. For a CTE based on a `SELECT`, column names usually come from the selected expressions or aliases. Naming a CTE does not save it as a permanent table, and its rows have no guaranteed order unless the final query orders them.

PostgreSQL also allows a `WITH` clause on data-changing statements. Those need extra care because their execution and `RETURNING` results differ from a simple read-only CTE. Start with read-only CTEs until the one-statement scope is clear.

## Check your understanding

1. Which step computes the total per customer?
2. Why is customer 2 missing from the final answer?
3. Would a new statement be able to select from `large_totals`?

## Further reading

- [PostgreSQL WITH queries](https://www.postgresql.org/docs/current/queries-with.html)
- [PostgreSQL VALUES lists](https://www.postgresql.org/docs/current/queries-values.html)
