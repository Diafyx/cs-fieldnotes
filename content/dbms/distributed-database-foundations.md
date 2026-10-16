# Distributed Database Foundations

A distributed database keeps data or copies of data on more than one machine. The machines communicate over a network. This can spread work, place data near users, and keep service running when a machine fails. It also means one request may depend on several machines that cannot always talk to each other.

## The pieces of a request

| Piece | Job | Question to ask |
| --- | --- | --- |
| Client | Sends a read or write. | Can it safely retry after a timeout? |
| Router or coordinator | Finds the machines needed for the request. | Does it know the current data placement? |
| Data node | Stores a partition, a replica, or both. | Is its copy current enough for this read? |
| Metadata or membership service | Tracks nodes, leaders, or placement. | What happens if its view is stale? |
| Network | Carries requests, responses, and replication data. | What happens when messages are delayed or lost? |

**Partitioning** divides different rows among machines. **Replication** keeps copies of the same rows on several machines. A system may do both: shard orders by customer, then keep three replicas of each shard. A cache is another copy, but it may follow different freshness and expiry rules.

## Failure is only partly visible

If a client times out, it does not know whether the server failed before the write, committed the write but lost the reply, or is merely slow. Retrying an insert or payment without a request ID can duplicate work. A useful design stores a unique request ID with the result, then lets a retry fetch that result or safely complete the missing work.

Consider a generic order service with one primary and two asynchronous replicas:

| Time | Primary | Replica B | Replica C |
| --- | --- | --- | --- |
| 1 | Order 41 does not exist. | Same state. | Same state. |
| 2 | Commits order 41 and replies. | Has not received it yet. | Has not received it yet. |
| 3 | Has order 41. | Receives the change. | Still behind. |

A read from C at time 3 may say the order is missing. A read from the primary can show it. If the primary is lost before either replica has a safe copy, the replied-to order may be lost during failover. This is an example of **asynchronous** replication; a system that waits for remote acknowledgments has different durability and latency costs. Even a remote acknowledgment can mean received, flushed, or applied, depending on the setting. State which one the application needs.

## Clocks and ownership

Two machines can have clocks that differ, and network messages can arrive out of order. A wall-clock timestamp alone is not proof of the order in which transactions committed. Systems use log positions, version numbers, or agreement protocols when an order must be established. If two machines may both accept writes for the same key, the design also needs a conflict rule. Last-write-wins can silently discard one change when clocks or delivery order differ.

A leader can give one place authority to accept writes for a partition. When it fails, a replacement must be chosen and the old leader must stop accepting writes. Otherwise two leaders can both report success for conflicting writes. A consensus protocol can help a group agree on a leader or log entry, but it adds messages and requires enough reachable members. A lease also depends on careful time assumptions. These mechanisms should be supplied and tested by the database or its cluster manager, not guessed by a client from a short timeout.

## Plan the whole system

More nodes do not automatically mean faster queries. A request that touches one shard can be quick; a query that asks every shard must wait for several nodes and merge results. A slow or failed dependency can dominate the response. Plan for rebalancing, schema changes, backups, monitoring, and recovery on every node. Keep replicas in separate failure domains when the goal is to survive a machine or site loss.

Start with the actual guarantee the user needs. A shopping cart badge may tolerate a short delay. A payment confirmation may need a read that sees the committed payment. Then choose routing, replication, and failure behavior to meet those needs. A replica is not a backup: it can copy a mistaken delete.

## Try it yourself

1. At time 3, which copies can answer that order 41 exists?
2. Why does a timeout after a payment leave the client unsure of the outcome?
3. What could happen if the old leader keeps accepting writes after a new leader is chosen?
4. Why is a report across all shards different from a lookup for one customer?

## References

- [PostgreSQL high availability and replication](https://www.postgresql.org/docs/current/high-availability.html)
- [PostgreSQL standby behavior](https://www.postgresql.org/docs/current/warm-standby.html)
- [MIT lab on a replicated key-value service](https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html)
