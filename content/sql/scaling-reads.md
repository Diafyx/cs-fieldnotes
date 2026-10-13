# Scaling Reads

Read scaling means serving more reads without making every read compete on the primary database. First make each read reasonably cheap. Select needed columns, check query plans, add useful indexes, avoid repeated queries for one request, and use a connection pool. If the primary still spends too much time on reads, a cache or read replica may help.

## Primary and replica

A PostgreSQL primary accepts writes. A physical standby receives changes from the primary. A standby in hot standby mode can answer read-only queries. Streaming replication is asynchronous by default, so a standby can be behind the primary. Sending a write to a replica fails; reading from it just after a write may return old data.

For example, a customer changes a shipping address and immediately opens the confirmation page. If the page reads from a lagging replica, it may show the old address. Route that read to the primary, or use a design that waits until the replica has replayed the needed change. A fixed sleep is not a reliable way to guarantee this. Some systems use synchronous replication for stronger durability guarantees, but it adds commit latency and does not automatically make every replica read current.

Here is a small routing rule. It is application policy, not a PostgreSQL command:

```python
def read_target(needs_latest_data: bool) -> str:
    return "primary" if needs_latest_data else "replica"

assert read_target(True) == "primary"  # confirmation after a write
assert read_target(False) == "replica"  # a report that allows some delay
```

The second read is safe only if the report can tolerate stale data. An important account balance or permission check may need the primary even without a write in the same request.

## What to watch

Measure replica replay lag, errors, and how long read queries run. A long query on a standby can conflict with WAL replay; PostgreSQL may delay replay or cancel the query, depending on its settings. Replicas also consume primary resources to send WAL and may increase storage and operating cost. Test failover and make sure clients do not keep writing to an old primary endpoint.

A cache can answer common reads quickly, but it needs an expiry or invalidation rule. If a cached value must change at the same time as a write, define how that happens and what readers see during a failure. Start with a measured, bounded use case, such as a public list that can be a minute old.

## Check your understanding

1. A user updates a profile and sees the old value on the next page. What is one likely cause?
2. Which queries can safely use an asynchronous replica in your application?
3. Why can adding replicas leave the write bottleneck unchanged?

## Further reading

- [PostgreSQL warm standby and streaming replication](https://www.postgresql.org/docs/current/warm-standby.html)
- [PostgreSQL hot standby](https://www.postgresql.org/docs/current/hot-standby.html)
