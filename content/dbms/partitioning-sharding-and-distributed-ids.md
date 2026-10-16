# Partitioning, Sharding, and Distributed IDs

Partitioning means splitting a data set into pieces using a rule. The pieces may stay inside one database or live on separate servers. Sharding usually means the second case. The key that chooses a piece affects query speed, load balance, and how hard it is to move data later.

## Three different splits

| Design | Where pieces live | Example | Main cost |
| --- | --- | --- | --- |
| Table partitioning | Child tables inside one PostgreSQL database. | Events by month. | More tables and partition management. |
| Sharding | Separate databases or server groups. | Tenants assigned to shards. | Routing, cross-shard work, and resharding. |
| Functional split | Different services own different data. | Billing owns invoices; shipping owns parcels. | Cross-service workflows and shared reports. |

PostgreSQL partition pruning can skip table partitions when a query filters on the partition key. It does not turn one database into a multi-server system. Some other databases use the word **partition** for a group of rows placed on a set of nodes, so read the product's definition.

## Pick a key from the queries

| Key method | Good at | Watch for |
| --- | --- | --- |
| Time range | Recent-data queries and dropping old time periods. | A busy newest partition and late events. |
| Hash of an ID | Spreading many IDs across shards. | Queries by other fields may contact every shard. |
| Tenant ID | Keeping one tenant's rows and transactions together. | One huge tenant can overload its shard. |
| Region | Keeping data near a region or within a required location. | Cross-region users and uneven regional load. |

For example, place every row for tenant 42 on shard A and every row for tenant 43 on shard B. A tenant-specific order lookup can contact one shard. A report of all orders must ask both and combine the answers. If customer and order rows use different shard keys, even a simple customer page may need a cross-shard join.

The router and the stored data must agree. A toy rule such as `tenant_id % 4` is easy to write, but changing the shard count to five changes many destinations before the rows have moved. Use a stable placement map or a controlled migration. A migration must copy data, capture writes made during the copy, switch routes safely, and verify the destination. Hot keys may still need special handling even with an even hash distribution.

## IDs across independent writers

Two database sequences can both issue order number `101`. Each shard's primary key can reject duplicates locally, yet the combined system can still have two `101` values. A globally unique identity can include a stable namespace, such as `(tenant_id, local_order_id)`, or use an ID generator designed for independent writers.

```python
# Two shards may each have a local order number 101.
orders = [(42, 101), (43, 101)]

assert len({local_id for _, local_id in orders}) == 1
assert len(set(orders)) == 2
```

The first set has one value, `101`. The second has two distinct pairs. This works only if tenant IDs themselves are unique and an order never moves to a different tenant without an identity plan. A fixed shard ID plus local sequence can also work if shard IDs are never reused. Avoid making a public order number depend on a physical shard if customers need it to remain stable through resharding.

UUID version 4 uses random bits and avoids a central counter in normal use. UUID version 7 includes time information and can improve index locality, but it is not a strict commit-order clock. PostgreSQL 18 provides `gen_random_uuid()` and `uuidv7()`; older servers may not have the latter. Time-and-node ID schemes need care with clock rollback, node ID assignment, and counter exhaustion. Whatever format you choose, keep the database uniqueness constraint and define what happens on a rare collision or duplicate request.

## The hidden cross-shard cost

A foreign key in one database does not usually check a row on another independent database. A local transaction cannot atomically update two separate shards. Options include keeping related data on one shard, using a distributed transaction system, or using a workflow with recovery and idempotent retries. Global `COUNT`, sorting, and `LIMIT` also require gathering and merging partial results. Test the actual query pattern before deciding that sharding will help it.

## Try it yourself

1. Why do the two orders in the Python example need more than the local number `101` to identify them globally?
2. Which key keeps a tenant's orders together, and what problem can one very large tenant cause?
3. What must happen before a router sends tenant 42 to a new shard?
4. Why can a time-based UUID fail to show exact commit order?

## References

- [PostgreSQL table partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
- [PostgreSQL UUID functions](https://www.postgresql.org/docs/current/functions-uuid.html)
- [PostgreSQL sequence behavior](https://www.postgresql.org/docs/current/sql-createsequence.html)
- [Apache Cassandra partition keys](https://cassandra.apache.org/doc/stable/cassandra/developing/data-modeling/intro.html)
