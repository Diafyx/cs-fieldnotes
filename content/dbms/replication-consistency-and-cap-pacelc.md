# Replication, Consistency, and CAP/PACELC

Replication keeps copies of data on several machines. A copy can help with availability and read load, but copies do not update at the same instant. A database design must say when a write is accepted and what a later read is allowed to see.

## What a copy has received

With **asynchronous replication**, a primary can confirm a commit before a replica receives it. A read from that replica may be stale. If the primary is lost before the change reaches a safe replica, failover may lose that acknowledged write. With **synchronous replication**, a commit waits for a chosen remote acknowledgment. This can improve durability but adds network time and may block commits when the required replica is unavailable.

The word *acknowledged* needs care. A replica may have received bytes, flushed them to durable storage, or replayed them so queries can see them. PostgreSQL's synchronous modes distinguish these stages. `remote_apply` waits until selected synchronous standbys have replayed a commit. It does not promise that every other replica or cache is current.

Physical replication copies PostgreSQL's WAL changes for a whole cluster. Logical replication publishes selected table changes to subscribers. Both need monitoring, failover plans, and backups. Replication can copy an accidental deletion too.

## Name the read guarantee

| Guarantee | What the reader gets | Example risk without it |
| --- | --- | --- |
| Eventual convergence | Copies can differ now but converge if writes stop and delivery succeeds. | A profile page briefly shows an old name. |
| Read your writes | A client sees its own completed change on later reads. | A user saves a form, then sees the old value. |
| Monotonic reads | One client does not move backward to an older version. | Page one shows version 5; page two shows version 4. |
| Linearizability | Each operation appears to take effect at one instant between its call and reply, respecting real-time order. | A read started after a confirmed write returns the prior value. |

These are different from **serializability**, which asks whether whole transactions behave like some serial order. A system can offer serializable transactions without a real-time ordering guarantee across all clients. SQL's ACID word *consistency* means preserving declared data rules; CAP uses *consistency* in the strong single-object sense, usually linearizability. State the exact guarantee instead of saying only “strong consistency.”

## What CAP says during a partition

Imagine three replicas A, B, and C. The network separates A from B and C. A client can still reach A, while another client can reach B and C. Both sides want to write the same key.

| Choice during the split | What happens | Cost |
| --- | --- | --- |
| Require agreement from two of three replicas. | B and C can accept a write; A cannot confirm one alone. | The client reaching only A cannot complete that write. |
| Let each side accept a write without agreement. | A and B/C can both reply. | The copies can disagree and need conflict handling later. |

CAP says a distributed system cannot guarantee both linearizable answers and a response to every request at reachable, nonfailed nodes when communication is partitioned. The “P” is a failure condition the design must face, not a feature to switch off. CAP does not say a database simply picks any two letters for normal operation. A quorum of two in this example overlaps another quorum of two, but overlap alone is not a full proof of correct reads; version and membership rules matter too.

PACELC adds a normal-operation question. **If there is a partition**, the design trades availability against consistency. **Else**, it may trade lower latency against stronger consistency, because waiting for remote copies takes time. This is a way to ask better questions about each operation, not a permanent two-letter label for an entire product. Some reads may use a local replica while payments use a stricter path.

## Choose the promise for the feature

For a public count that can be a minute old, an asynchronous replica may be fine. For a permission check or payment confirmation, use a path that provides the required freshness. Reading from the primary is a common simple choice. A fixed sleep after writing is not a correctness rule: lag can exceed the sleep. Monitor replay lag and test failover, including what happens to writes whose result the client received just before the failure.

## Try it yourself

1. During the A versus B/C split, why must the two sides disagree or refuse some requests if both try to write the same key?
2. Why can a synchronous remote flush still leave a standby read behind its primary?
3. Which read guarantee prevents one client from seeing version 5 and then version 4?
4. What extra question does PACELC ask when the network is healthy?

## References

- [Gilbert and Lynch on the CAP theorem](https://dspace.mit.edu/entities/publication/dfcb6512-af44-4fc9-8e8b-1a8f28f1b53a)
- [Abadi's PACELC paper](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf)
- [PostgreSQL streaming and synchronous replication](https://www.postgresql.org/docs/current/warm-standby.html)
- [PostgreSQL logical replication](https://www.postgresql.org/docs/current/logical-replication.html)
