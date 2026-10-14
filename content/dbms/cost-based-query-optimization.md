# Cost-Based Query Optimization

A cost-based optimizer compares ways to run a query and chooses one it expects to be cheap. It estimates how many rows each step will handle, how much work those rows need, and how much data may be read. It cannot know the future exactly. A plan is a reasoned choice based on statistics and cost settings, not a guarantee of the fastest possible run.

## What the planner compares

For a single table, PostgreSQL may compare a sequential scan, an index scan, or a bitmap scan. For joins, it also compares join order and join algorithms. Later steps may sort, group, or limit rows. A plan with a higher setup cost can be good for many rows; a plan that returns its first rows quickly can be better with `LIMIT`.

In `EXPLAIN`, **startup cost** estimates work before the first row is returned. **Total cost** estimates work to return all rows from a node. Cost units are not milliseconds. The displayed `rows` and `width` are estimates of row count and average row size. Parent-node costs include work done by children, so adding every printed cost gives the wrong total.

## Why row estimates matter

Statistics collected by `ANALYZE` help estimate table size, the share of rows matching a condition, common values, and value ranges. The share expected to pass a filter is its **selectivity**. If a filter is expected to keep 1% of 100,000 rows, the planner estimates about 1,000 rows before considering later steps. A wrong estimate can make an index scan look attractive when a table scan would be cheaper, or make a join's build side much larger than planned.

```sql
CREATE TEMP TABLE events (
    event_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    kind TEXT NOT NULL
);

INSERT INTO events VALUES
    (1, 10, 'open'),
    (2, 20, 'open'),
    (3, 10, 'click'),
    (4, 10, 'close'),
    (5, 30, 'open');

CREATE INDEX events_account_idx ON events (account_id);
ANALYZE events;

SELECT event_id, kind
FROM events
WHERE account_id = 10
ORDER BY event_id;
```

The result is `(1, open)`, `(3, click)`, and `(4, close)`. The index gives PostgreSQL a possible lookup path. Three of five rows match, so a small-table scan may be cheaper. The answer is the same whichever path is chosen.

To compare estimates with a real run in PostgreSQL, use:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT event_id, kind
FROM events
WHERE account_id = 10
ORDER BY event_id;
```

Read the scan's estimated `rows` beside its actual rows. Look for `Index Cond` versus `Filter`, a separate `Sort`, and buffer hits or reads. `EXPLAIN ANALYZE` executes the query and adds measurement overhead. It does not include every cost of sending rows to an application.

## When estimates are wrong

Statistics are based on samples and can become stale after large data changes. Values can be skewed: one account might have half the events while most have only a few. Two columns can be related, so multiplying independent selectivity estimates can be wrong. PostgreSQL can collect extended statistics on selected column groups to help with some of these cases. Check the measured plan before adding one.

Parameterized queries add another choice. PostgreSQL may use a **custom plan** built for the supplied values or a **generic plan** reused across values. A generic plan saves planning work but may be poor when common and rare parameter values need different access paths. This is a reason to test realistic parameter values, not just one convenient case.

For many joined tables, trying every possible join order takes too long. PostgreSQL limits planning search and can use a genetic search method above a join-count threshold. The chosen plan is therefore not necessarily the absolute best plan among all possible plans.

Start a slow-query investigation with the actual plan, row estimates, actual rows, and buffer activity. Then check statistics, useful indexes, query shape, and data skew. Avoid changing planner cost settings or disabling plan methods as a first guess; those settings affect more than one query.

## Try it yourself

1. Why might the example use a sequential scan despite the index?
2. What does a large difference between estimated and actual rows suggest?
3. How can a plan for a common account differ from a plan for a rare account?

## References

- [PostgreSQL planner statistics](https://www.postgresql.org/docs/current/planner-stats.html)
- [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL planner overview](https://www.postgresql.org/docs/current/planner-optimizer.html)
- [PostgreSQL prepared plans](https://www.postgresql.org/docs/current/sql-prepare.html)
