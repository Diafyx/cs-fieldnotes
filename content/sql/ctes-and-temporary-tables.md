# CTEs and Temporary Tables

A common table expression, or CTE, names the result of a query for one SQL statement. A temporary table is a real table that lives for one database session in PostgreSQL, unless it is set to end sooner. Both can help break work into steps, but they have different lifetimes.

## Try both ideas

Create a temporary table with three sales:

```sql
CREATE TEMP TABLE sales (
  sale_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  amount integer NOT NULL
);
INSERT INTO sales VALUES (1, 10, 20), (2, 10, 30), (3, 20, 15);
```

Use a CTE to name one calculation:

```sql
WITH customer_totals AS (
  SELECT customer_id, SUM(amount) AS total
  FROM sales
  GROUP BY customer_id
)
SELECT customer_id, total
FROM customer_totals
WHERE total >= 25
ORDER BY customer_id;
```

The result is `(10, 50)`. A later statement can still read `sales` on the same connection. It cannot read `customer_totals`, because that name existed only for the `WITH` statement.

## Choose the right lifetime

Use a CTE when a single query needs named steps. It does not create a table you can index or reuse in a later statement. Use a temporary table when several statements in one session need the same intermediate rows or when you need indexes or statistics for a larger staged result. Creating and filling a table has a cost, so do not use one merely to shorten a small query. PostgreSQL's autovacuum does not analyze temporary tables; run `ANALYZE` yourself after filling a large one when query plans depend on its row counts.

In PostgreSQL, a temporary table normally keeps its rows across commits until the session ends. `ON COMMIT DELETE ROWS` empties it at commit; `ON COMMIT DROP` removes it at commit. A temporary table can hide a permanent table with the same unqualified name, so use clear names and schema qualifications where needed. Session-based state also needs care with transaction poolers, which may give the next transaction a different server connection.

The database may fold a simple CTE into the surrounding query. It is therefore unsafe to assume every CTE is stored as a separate result. Check the execution plan if that choice matters for performance.

## Check your understanding

1. Which name still exists for a later statement on the same connection?
2. Which `ON COMMIT` option removes a PostgreSQL temporary table at commit?
3. Why might a transaction pooler make session temporary tables hard to use?

## Further reading

- [PostgreSQL WITH queries](https://www.postgresql.org/docs/current/queries-with.html)
- [PostgreSQL temporary tables](https://www.postgresql.org/docs/current/sql-createtable.html)
