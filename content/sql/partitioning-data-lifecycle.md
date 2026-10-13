# Partitioning & Data Lifecycle

Partitioning splits one logical table into smaller physical tables inside the same PostgreSQL database. A common choice is one partition per month of event time. Queries that filter on that time can skip unrelated partitions. Old months can be detached or removed as whole partitions after their retention period ends.

## Range partition example

This example keeps events for January and February 2026. The partition bounds are lower inclusive and upper exclusive.

```sql
CREATE TEMP TABLE events (
  event_id bigint NOT NULL,
  occurred_on date NOT NULL,
  message text NOT NULL,
  PRIMARY KEY (event_id, occurred_on)
) PARTITION BY RANGE (occurred_on);

CREATE TEMP TABLE events_2026_01 PARTITION OF events
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TEMP TABLE events_2026_02 PARTITION OF events
  FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

INSERT INTO events VALUES
  (1, '2026-01-10', 'opened'),
  (2, '2026-02-03', 'closed');

SELECT event_id, message FROM events
WHERE occurred_on >= DATE '2026-01-01'
  AND occurred_on < DATE '2026-02-01';
```

The query returns only event 1. PostgreSQL can prune the February partition because the filter uses the partition key. The exact plan depends on the query and planner settings; use `EXPLAIN` to check it. An insert dated March fails here because there is no March or default partition.

The primary key includes `occurred_on` because PostgreSQL requires a unique or primary key on a partitioned table to include every partition key column. This key does not enforce uniqueness of `event_id` alone across months. If the application needs globally unique event IDs, generate them with a separate scheme and understand that this table's key only enforces the pair.

## Keep and remove data on purpose

Decide which date owns a row, how late arrivals are handled, and when a new partition is created. Create future partitions before writes arrive. Keep indexes and constraints that the queries need on the partitioned table. Do not create thousands of tiny partitions without measuring planning and maintenance cost.

For retention, an old partition can be detached, archived or backed up if required, and then dropped. This is usually simpler than deleting millions of old rows one by one. Check legal holds and backup retention before removal. Detaching or dropping a partition is still a schema operation with locks and must be planned. A row written to the wrong date partition will follow the partition key, so choose that key carefully.

Partitioning does not move writes to several independent servers. All these partitions still belong to one PostgreSQL cluster. It helps most when queries filter on the partition key or when whole groups of rows can be removed. It may add complexity without making a small table faster.

## Check your understanding

1. Why does the January query avoid needing rows from February?
2. What happens when the example receives an event dated March 1?
3. Why does the primary key include `occurred_on`, and what uniqueness does it enforce?

## Further reading

- [PostgreSQL table partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
