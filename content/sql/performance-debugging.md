# Performance & Debugging

A slow query needs a clear problem statement. Record the SQL, its input values, the expected rows, and where the time is spent. A query that finishes quickly in the database can still feel slow if the application sends too many requests or transfers too many rows.

## Start with a result you can check

```sql
CREATE TEMP TABLE demo_orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  placed_on date NOT NULL,
  amount numeric(10, 2) NOT NULL
);

INSERT INTO demo_orders VALUES
  (1, 10, '2026-01-02', 10),
  (2, 10, '2026-01-03', 20),
  (3, 20, '2026-01-04', 5),
  (4, 20, '2026-02-01', 7);

SELECT customer_id, SUM(amount) AS january_total
FROM demo_orders
WHERE placed_on >= DATE '2026-01-01'
  AND placed_on < DATE '2026-02-01'
GROUP BY customer_id
ORDER BY customer_id;
```

The result is `(10, 30)` and `(20, 5)`. The February order is outside the range. Check this answer before trying to make the query faster. A faster query that includes order 4 is still wrong.

## Measure one change at a time

Run this after the setup above in PostgreSQL:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT customer_id, SUM(amount) AS january_total
FROM demo_orders
WHERE placed_on >= DATE '2026-01-01'
  AND placed_on < DATE '2026-02-01'
GROUP BY customer_id
ORDER BY customer_id;
```

`EXPLAIN` shows the plan. `ANALYZE` also runs the query and adds actual row counts and times. `BUFFERS` shows page access. With four rows, a table scan may be the best plan, so this sample teaches how to read a result rather than proving an index would help. Measure again with production-like row counts and value distributions before changing a real index.

For a slow request, separate application time from database time. Check how many SQL calls the request makes, whether it waits for locks, how many rows it returns, and whether sorting or joining creates much more work than expected. In the plan, compare estimated rows with actual rows. Large gaps can point to stale or insufficient statistics, a skewed value, or a mistaken join. Run `ANALYZE` after a large load and inspect the plan again.

Change one thing, then compare the same query with the same parameters and a similar cache state. A new index has storage and write costs. A faster plan in one tiny test may be slower for another parameter value. Keep the correctness check beside the timing check.

## Check your understanding

1. Why is order 4 absent from the January total?
2. Why might PostgreSQL scan this whole four-row table despite an index?
3. What would you investigate if database time is low but the page still loads slowly?

## Further reading

- [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL planner statistics](https://www.postgresql.org/docs/current/planner-stats.html)
