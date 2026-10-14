# Log-Based Recovery and Write-Ahead Logging

A write-ahead log (WAL) records changes before the matching data pages are allowed to reach durable storage. This gives recovery a history to replay after a crash. The word **ahead** describes the order of durable writes, not the order of SQL statements in an application.

## The two ordering rules

1. Before a changed data page is written to durable storage, the log records needed to describe that change must be durable.
2. Before a normal synchronous commit reports success, the commit record and the log it depends on must be durable. The changed data pages can be written later.

The first rule protects against an uncommitted page reaching disk without a way to identify or repair it. The second rule protects a committed change whose data page has not yet been written. PostgreSQL follows the WAL rule and normally flushes WAL at commit. Its `synchronous_commit = off` option relaxes the point at which success is reported, so a crash can lose a recently reported commit. Turning `fsync` off is more dangerous because it can leave the database inconsistent after a crash.

WAL records have increasing **log sequence numbers** (LSNs). An LSN identifies a location in the log. A data page can record the LSN of the latest change applied to it, letting a recovery method skip work that the page already contains. A log may record changed bytes, an operation, a full page image, or other information. It is not simply a readable list of SQL commands.

## Work through a crash

This is a small textbook model with one value per page. The initial durable state is `A = 100` and `B = 50`.

| Log order | Transaction | Action |
| --- | --- | --- |
| 10 | T1 | Set A from `100` to `80`. |
| 20 | T1 | Set B from `50` to `70`. |
| 30 | T1 | Commit. |
| 40 | T2 | Set A from `80` to `89`. |
| Crash | | The page for A has reached disk with `89`; the page for B still has `50`. |

Assume all three update records and T1's commit record have reached durable WAL before the crash. Recovery must keep T1's transfer and reject T2's unfinished change. In a textbook redo and undo scheme, redo restores the logged state up to the crash, then undo removes T2's change. The final values are `A = 80` and `B = 70`. Starting from only the disk pages would give the wrong answer. The disk has T2's uncommitted value for A and lacks T1's committed value for B.

In a system that never writes uncommitted pages, undo of a disk page might not be needed. In a system that forces all changed pages at commit, redo might be reduced. These policies have costs, which is why many systems allow dirty pages to be written later or earlier and rely on a log for recovery.

## PostgreSQL and the textbook model

PostgreSQL stores WAL in `pg_wal` and uses it to redo missing changes after a crash. It does not recover by running a simple before-image undo on every uncommitted row update. Its multi-version storage and transaction status decide which row versions are visible, and cleanup can remove dead versions later. Do not apply the textbook's physical undo step literally to PostgreSQL's heap files.

PostgreSQL can put a full page image in WAL on the first change to a page after a checkpoint. This helps repair a page whose disk write was interrupted. WAL is also useful for replication and point-in-time recovery when the needed records are kept or archived.

If you have PostgreSQL access, these read-only queries show three different WAL positions:

```sql
SELECT pg_current_wal_insert_lsn() AS inserted,
       pg_current_wal_lsn() AS written,
       pg_current_wal_flush_lsn() AS flushed;
```

`inserted` is the end of records placed in WAL buffers. `written` has reached the operating system. `flushed` is the last location PostgreSQL knows was made durable. The exact values change as other sessions work. These positions do not by themselves prove that a particular backup is valid.

## Common mistakes

- WAL is not a backup of the whole database. Old WAL segments can be recycled, and a lost base data set cannot generally be rebuilt from only recent WAL.
- A commit does not mean every table page was written at that moment. A durable WAL record can carry the work until those pages are written.
- A file-system journal does not replace the database's transaction log.
- A log record being **written** and being **flushed** are different durability steps.

## Try it yourself

1. In the crash example, why is the disk value `A = 89` unsafe to keep?
2. What would happen if B's changed page were lost after T1 committed and there were no durable WAL record for it?
3. Why does PostgreSQL distinguish WAL insert, write, and flush positions?

## References

- [PostgreSQL WAL overview](https://www.postgresql.org/docs/current/wal-intro.html)
- [PostgreSQL WAL internals](https://www.postgresql.org/docs/current/wal-internals.html)
- [PostgreSQL WAL settings](https://www.postgresql.org/docs/current/runtime-config-wal.html)
- [PostgreSQL WAL position functions](https://www.postgresql.org/docs/current/functions-admin.html)
