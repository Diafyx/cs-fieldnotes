# Sharding

Sharding splits rows across separate databases. An application uses a shard key, such as `tenant_id`, to choose where each row lives. Each shard has its own storage and compute resources. This can spread data and writes beyond one server, but every request now needs the right route.

PostgreSQL does not make several independent databases act like one transparent sharded table. The example below is an application routing rule. Assume four shards numbered 0 through 3 and integer tenant IDs.

```python
def shard_for(tenant_id: int, shard_count: int = 4) -> int:
    if tenant_id < 0 or shard_count < 1:
        raise ValueError("invalid tenant or shard count")
    return tenant_id % shard_count

assert shard_for(10) == 2
assert shard_for(11) == 3
assert shard_for(10, 5) == 0
```

Tenant 10 moves from shard 2 to shard 0 when the count changes from four to five. Real data does not move just because the routing formula changed. Queries would look on the new shard and miss old rows. A production design needs a stable routing map, a controlled migration, or another scheme that limits movement. The routing rule and data placement must change together.

## Choose the key carefully

Keeping all rows for one tenant on one shard makes tenant-local joins and transactions easier. A query over all tenants must visit several shards and combine results. A single very large tenant can still overload its shard. If rows are split by an order ID instead, a customer page may have to ask many shards for its orders. Choose a key based on the queries and write patterns you actually have.

Each shard needs schema changes, backups, monitoring, and recovery. A primary key is unique only within its own database unless IDs are designed to be unique across shards. Cross-shard foreign keys and transactions are harder. If a multi-shard write partly succeeds, the application needs a recovery plan. Reports may be better served from a separate analytical copy than by querying every live shard.

Before sharding, check whether a slow query, poor index, oversized result, connection pressure, or a single hot tenant explains the problem. If sharding is needed, plan routing, tenant moves, shard failure, and resharding before putting data on the first shard.

## Check your understanding

1. Why would changing `shard_count` from four to five make the simple router unsafe?
2. What happens to a report that needs rows from every tenant?
3. Why might a tenant key still leave one shard overloaded?

## Further reading

- [PostgreSQL foreign data wrappers](https://www.postgresql.org/docs/current/postgres-fdw.html)
- [PostgreSQL partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
