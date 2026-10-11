# Query Lifecycle

A query travels through several parts of a database system before the client sees a result. Knowing the path helps when a statement fails, returns the wrong rows, or runs slowly. It also keeps two different ideas apart: the logical meaning of SQL and the physical plan chosen to carry it out.

This page describes PostgreSQL. Other database systems follow a similar broad path but use different internals.

## From text to a plan

Consider this query:

```sql
SELECT order_id, amount
FROM orders
WHERE customer_id = 10
ORDER BY order_id;
```

PostgreSQL parses the text, checks names and types, and builds an internal representation. Its rewrite step can account for things such as views and rules. The planner then considers ways to get the requested rows. It may scan the table or use an index, depending on the data, statistics, and query.

A syntax error happens early. A missing table or column also prevents the statement from reaching normal execution. A slow statement with valid SQL needs a different investigation: inspect its plan and how many rows each part reads.

## Execute and return rows

The executor runs the chosen plan. A plan is a tree of operations such as scans, filters, joins, aggregates, and sorts. Each operation produces rows for the next one. The result is sent to the client, which reads it through `psql`, Psycopg, JDBC, or another driver.

The database may not physically do work in the same order that the SQL clauses appear on the page. The SQL language defines the result. The planner has room to choose an efficient way to produce that result without changing its meaning.

## Inspect the plan

```sql
EXPLAIN
SELECT order_id, amount
FROM orders
WHERE customer_id = 10
ORDER BY order_id;
```

`EXPLAIN` shows the plan and estimates without running the query. `EXPLAIN ANALYZE` runs it and adds measured row counts and times. For a statement that changes data, `EXPLAIN ANALYZE` also performs the change. Use a safe environment or an appropriate transaction when inspecting such statements.

Plans can change after the table grows, after statistics are updated, or after an index is added. Estimated cost numbers are planner units, not milliseconds. Compare estimated and actual rows to find where the planner's picture of the data differs from reality.

## The client has work too

The database's execution time is not always the full time a user waits. The client may transfer many rows, decode them, build objects, and render a page. If a query returns far more rows than needed, a fast plan can still lead to a slow application. Select needed columns and set a sensible result size.

## Check your understanding

1. Which stage chooses between a table scan and an index scan?
2. Why is the logical order of SQL clauses not a physical execution plan?
3. What extra risk does `EXPLAIN ANALYZE` have for an `UPDATE` statement?

## Further reading

- [PostgreSQL path of a query](https://www.postgresql.org/docs/current/query-path.html)
- [PostgreSQL executor](https://www.postgresql.org/docs/current/executor.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
