# Scaling And Production Operations

A database can slow down for many reasons. More traffic is only one of them. A bad query, an absent index, a long transaction, or too many open connections can cause trouble even when the tables are small. First find the part that is under pressure. Then choose a change that addresses that part.

## Measure the work

Suppose an application serves 1,000 requests each second. Each request makes three database queries. That is 3,000 queries each second, before jobs and retries. If one screen loads the same data in a single query instead of three, the rough count falls to 1,000. This is a workload estimate, not a claim that either rate is safe for a given server.

```sql
WITH workload(requests_per_second, queries_per_request) AS (
  VALUES (1000, 3), (1000, 1)
)
SELECT requests_per_second,
       queries_per_request,
       requests_per_second * queries_per_request AS queries_per_second
FROM workload;
```

The two rows return 3,000 and 1,000. Real capacity also depends on query cost, cache hits, row counts, concurrent work, and hardware. A count of queries alone cannot explain latency.

For a slow query, record its duration and inspect `EXPLAIN (ANALYZE, BUFFERS)` on safe sample work. `ANALYZE` executes the query, so take care with writes. Check the plan, rows read, and disk activity. For a busy server, inspect active sessions, wait events, locks, connection counts, CPU, disk I/O, and replication lag. PostgreSQL exposes much of this through its statistics views. Keep application metrics too: request rate, error rate, and latency percentiles.

## Pick the change that fits

| Pressure | First things to check | Possible next step |
| --- | --- | --- |
| Slow read | Query plan, indexes, rows returned | Rewrite the query, add a useful index, cache suitable data, or add a read replica |
| Slow write | Index count, locks, WAL and disk I/O | Shorten transactions, batch suitable writes, or scale the writer |
| Too many connections | Pool settings and idle sessions | Use a connection pool and set a limit |
| Large time-based table | Filter and retention needs | Partition by time if pruning or removal helps |
| One server cannot hold the workload | Data size and write demand | Consider sharding after measuring its cost |

A read replica can add read capacity but does not increase the primary's write capacity. Partitioning keeps partitions in one PostgreSQL cluster; it is mainly a way to manage and prune data. Sharding places different data on different database servers and adds routing work to the application. These solve different problems.

## Keep the service recoverable

Take backups and test a restore. A backup that has never been restored is an untested recovery plan. Set a recovery point objective, which is how much data the business can afford to lose, and a recovery time objective, which is how long recovery may take. Configure backups, WAL archiving or another recovery method, and retention to match those targets. Replicas help availability, but they can copy accidental deletes and are not a replacement for backups.

Plan failover and schema changes before an incident. Know which application endpoint points to the primary, how clients reconnect, and how writes are kept on one primary. Test the procedure. Alert on symptoms users feel, such as rising latency or failed writes, as well as server metrics. Keep enough free storage for growth, WAL, indexes, and maintenance work.

## Check your understanding

1. A query becomes slow after a new index is added. What would you measure before adding a replica?
2. Why does a replica not fix a write bottleneck on the primary?
3. How would you prove that yesterday's backup can be used to recover the service?

## Further reading

- [PostgreSQL monitoring statistics](https://www.postgresql.org/docs/current/monitoring-stats.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
