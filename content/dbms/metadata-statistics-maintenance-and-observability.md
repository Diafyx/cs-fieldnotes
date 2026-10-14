# Metadata, Statistics, Maintenance, and Observability

A database stores facts about its own tables, columns, indexes, and activity. This is **metadata**. It also keeps estimates that help the query planner and counters that help an operator find trouble. These sources answer different questions. A table definition tells you what should exist; a statistic gives an estimate; a live activity view shows what is happening now.

## Find the definition

`information_schema` offers standard views for tables and columns. PostgreSQL's `pg_catalog` holds more detailed, product-specific metadata. A role may see only the information it has permission to see through some information schema views. System catalogs, such as `pg_class` and `pg_attribute`, are useful when a PostgreSQL-specific detail is needed, but their columns are less portable than the information schema.

Run this in PostgreSQL:

```sql
CREATE TEMP TABLE ops_notes (
    note_id INTEGER PRIMARY KEY,
    score INTEGER NOT NULL
);

INSERT INTO ops_notes VALUES (1, 10), (2, 20), (3, 30);
ANALYZE ops_notes;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = (
    SELECT nspname FROM pg_catalog.pg_namespace
    WHERE oid = pg_catalog.pg_my_temp_schema()
)
  AND table_name = 'ops_notes'
ORDER BY ordinal_position;
```

The result has two rows: `(note_id, integer)` and `(score, integer)`. The temporary table disappears when the session ends. `ANALYZE` samples table data to update planner statistics; it does not change the three rows. PostgreSQL can store common values, histograms, and estimated distinct counts. These are planning aids, not an exact answer to `SELECT count(*)`.

## Keep the storage healthy

PostgreSQL updates and deletes can leave old row versions behind for a while. Ordinary `VACUUM` makes dead space reusable and helps prevent transaction ID wraparound. It also maintains visibility information that can help index-only scans. `ANALYZE` refreshes planner estimates. Autovacuum normally schedules both jobs. Long open transactions can delay cleanup, so investigate sessions that remain idle in a transaction.

`VACUUM FULL` rewrites a table to return more space to the operating system, but it takes a strong lock and needs extra working space. It is not the routine first step for a growing table. `REINDEX` rebuilds an index when there is a specific reason; routine `VACUUM` and `ANALYZE` do different jobs. Do not disable autovacuum just to hide background work. Without enough vacuuming, table size and wraparound risk grow.

## Read a useful signal

This query lists user tables with the largest **estimated** dead-row counts in the current PostgreSQL database:

```sql
SELECT schemaname, relname, n_live_tup, n_dead_tup,
       last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 10;
```

Your result depends on the database. `n_live_tup` and `n_dead_tup` are estimates and may lag behind recent changes. A high number is a clue, not proof that vacuum is broken. Compare it with table size, update rate, last vacuum time, and old transactions before acting. Statistics can also be reset.

| Question | First place to look |
| --- | --- |
| What is this table's shape? | `information_schema` or `pg_catalog` |
| What is running or waiting now? | `pg_stat_activity` and wait events |
| Are tables accumulating dead versions? | `pg_stat_user_tables` and vacuum progress |
| Which query shapes use time and I/O? | `pg_stat_statements`, if enabled |
| Why was this plan chosen? | `EXPLAIN`, then `EXPLAIN (ANALYZE, BUFFERS)` for a safe query |
| Are errors, archiving, or backups failing? | Server logs and backup or archiver checks |

`pg_stat_statements` is an extension that needs server setup; it is not guaranteed to be present. `EXPLAIN` shows a planned path. `EXPLAIN ANALYZE` actually executes the statement, so an `UPDATE` inside it really changes data unless rolled back. Plan and runtime counts can differ because estimates, data, and concurrent work change. One slow query is not enough to judge the whole system. Look at repeated slow queries, waits, disk use, connection pressure, and error rates over time.

## Try it yourself

1. Why does `n_live_tup = 1000` not prove a table has exactly 1000 rows?
2. What does `ANALYZE` change, and what does it leave alone in the example?
3. Why might a long idle transaction make vacuum less effective?
4. Why should you be careful with `EXPLAIN ANALYZE` on a write statement?

## References

- [PostgreSQL information schema columns](https://www.postgresql.org/docs/current/infoschema-columns.html)
- [PostgreSQL statistics views](https://www.postgresql.org/docs/current/monitoring-stats.html)
- [PostgreSQL ANALYZE](https://www.postgresql.org/docs/current/sql-analyze.html)
- [PostgreSQL routine vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)
