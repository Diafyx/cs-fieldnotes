# Storage and Query-Plan Lab

An index can make a selective lookup faster, but the database chooses a plan from table size, data distribution, and statistics. This lab creates enough rows to compare plans. It shows how to read the result without assuming that every machine will choose the same plan.

## Set up a repeatable table

Use a scratch PostgreSQL database. The temporary table disappears when the session ends. `generate_series` is a PostgreSQL function. The table has 100,000 events spread over 1,000 tenants; each tenant gets 100 events.

```sql
CREATE TEMP TABLE lab_events (
    event_id INTEGER PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    event_day DATE NOT NULL,
    payload TEXT NOT NULL
);

INSERT INTO lab_events
SELECT n,
       n % 1000,
       DATE '2026-01-01' + (n % 365),
       'event-' || n
FROM generate_series(1, 100000) AS g(n);

ANALYZE lab_events;

SELECT COUNT(*) FROM lab_events WHERE tenant_id = 42;

EXPLAIN (ANALYZE, BUFFERS)
SELECT event_id, event_day
FROM lab_events
WHERE tenant_id = 42
ORDER BY event_day, event_id;
```

The count is `100`. Write down the plan, estimated rows, actual rows, execution time, and buffer hits or reads. The first plan may use a sequential scan because there is no tenant index. The primary key on `event_id` does not make a search by `tenant_id` fast.

Now add an index and repeat the same query:

```sql
CREATE INDEX lab_events_tenant_day_id
    ON lab_events (tenant_id, event_day, event_id);

ANALYZE lab_events;

EXPLAIN (ANALYZE, BUFFERS)
SELECT event_id, event_day
FROM lab_events
WHERE tenant_id = 42
ORDER BY event_day, event_id;
```

The index starts with the equality filter, then stores rows in the requested order within that tenant. The planner may choose an index scan or an index-only scan. An index-only scan may still fetch heap pages when its visibility map cannot prove that the matching tuples are visible. Do not promise one exact node name or timing. Compare your own plans and run the query several times because cache state changes the measured time.

## Read the plan from the bottom up

| Plan field | What to ask |
| --- | --- |
| `Seq Scan`, `Index Scan`, or `Bitmap Heap Scan` | How are candidate rows found? |
| `Index Cond` and `Filter` | Which conditions narrow the index search, and which are checked later? |
| Estimated `rows` and actual `rows` | Does the planner understand the data shape? |
| `Sort` | Did the index already provide the needed order? |
| `Buffers: shared hit/read` or `local hit/read` | Were blocks found in PostgreSQL's cache or read into it? |
| `loops` | How many times did a node run? |

This lab uses a temporary table, so `local` buffer counts can appear. An index is stored in pages too. A lookup may touch both index and heap pages. A sequential scan can be better when the query needs most rows. If estimates are far from actual counts, first check `ANALYZE`, filters, and data skew. Do not start by forcing an index.

The optimizer's cost numbers are its comparison units, not milliseconds. `EXPLAIN ANALYZE` really executes the query and adds measurement overhead. For an `UPDATE` or `DELETE`, it would change rows unless you wrap it in a transaction and roll it back. Timing from a 100,000-row sample does not predict the cost of a production table with a different size or cache.

## Try a broad query

Run `EXPLAIN (ANALYZE, BUFFERS) SELECT COUNT(*) FROM lab_events;`. It must examine the table's rows or an index that represents them. Compare that plan with the tenant lookup. Why might a sequential scan be reasonable for the count even after the new index exists? Next, try a predicate on `event_day` alone. The index begins with `tenant_id`, so ask whether it can narrow that day-only search well on your PostgreSQL version and data.

## Try it yourself

1. Why does an `event_id` primary key not directly help `WHERE tenant_id = 42`?
2. What do the second and third columns of the new index do for the example query?
3. Why can two runs of the same `EXPLAIN ANALYZE` have different times?
4. Why is a plan on this sample not proof of a production speedup?

## References

- [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL EXPLAIN options](https://www.postgresql.org/docs/current/sql-explain.html)
- [PostgreSQL planner statistics](https://www.postgresql.org/docs/current/planner-stats.html)
- [PostgreSQL index-only scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
