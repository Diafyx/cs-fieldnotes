# Debugging Queries with EXPLAIN

`EXPLAIN` shows how PostgreSQL plans to run a query. `EXPLAIN (ANALYZE)` runs it and reports what happened. Read the plan from the scan nodes upward: which rows were read, how they were filtered, and where they were joined, sorted, or grouped.

## Compare a plan before and after an index

```sql
CREATE TEMP TABLE demo_events AS
SELECT g AS event_id, (g % 100) + 1 AS user_id,
       DATE '2026-01-01' + (g % 30) AS event_day
FROM generate_series(1, 10000) AS series(g);

ANALYZE demo_events;

EXPLAIN (ANALYZE, BUFFERS)
SELECT event_id
FROM demo_events
WHERE user_id = 7
ORDER BY event_day, event_id
LIMIT 5;

CREATE INDEX demo_events_user_day_id_idx
ON demo_events (user_id, event_day, event_id);

ANALYZE demo_events;

EXPLAIN (ANALYZE, BUFFERS)
SELECT event_id
FROM demo_events
WHERE user_id = 7
ORDER BY event_day, event_id
LIMIT 5;

SELECT event_id
FROM demo_events
WHERE user_id = 7
ORDER BY event_day, event_id
LIMIT 5;
```

The final query returns event IDs `6`, `306`, `606`, `906`, and `1206`. There are 100 rows for user 7; these five come first by day and ID. The index matches the equality filter, then the sort order. PostgreSQL may still choose a different plan if its cost estimate says that is cheaper. The example does not promise a speedup on every machine.

## Read the important fields

`cost` is the planner's estimate in cost units, not milliseconds. `rows` beside cost is an estimated count. `actual time` is measured in milliseconds, and `actual rows` is what a node returned per execution. `loops` tells you how many times that node ran. For a node run many times, multiply its per-loop rows or time by the loop count to understand the repeated work. Node times include work in child nodes, so do not add all node times as if they were separate.

A sequential scan reads a table. An index scan uses an index to find candidate rows. A sort may appear before `ORDER BY`, a join, or an aggregate. Look for a large mismatch between estimated and actual row counts, a loop that repeats expensive work, or a sort that spills to temporary storage. `BUFFERS` distinguishes cache hits from page reads and can show temporary blocks. A cache hit is still work; it is not the same as a disk read.

The final `Execution Time` does not include sending result rows to the application. `EXPLAIN ANALYZE` adds some measurement overhead. Plain `EXPLAIN` does not run a `SELECT`, but `EXPLAIN ANALYZE` does run the statement. For an `UPDATE` or `DELETE`, use a test database or wrap the analyzed statement in a transaction and roll it back if you do not want to keep its changes.

## Check your understanding

1. Why does an index on `(user_id, event_day, event_id)` fit this filter and order?
2. What does a high `loops` count on an inner scan tell you?
3. Why can an `EXPLAIN ANALYZE` time differ from application request time?

## Further reading

- [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL EXPLAIN options](https://www.postgresql.org/docs/current/sql-explain.html)
