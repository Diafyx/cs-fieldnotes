# Failures, Storage, and Recovery Goals

Recovery is how a database gets back to a usable state after work stops unexpectedly. It has two main jobs. It must keep committed changes that were promised to the client, and it must stop unfinished transactions from appearing as committed work. The answer depends on what failed and which copies of the data still exist.

## What can fail?

| Failure | Example | What recovery needs |
| --- | --- | --- |
| Transaction | A constraint fails, or the application calls `ROLLBACK`. | Undo that transaction's effects without losing other work. |
| Process or server | The database process crashes or power is lost. | Use durable records to bring files back to a consistent state. |
| Storage | A disk loses a database file or returns corrupt data. | Restore sound copies from a backup or another recovery source. |
| Human or application | Someone commits a bad update or drops a table. | Restore an earlier state, or use a carefully planned correction. |
| Whole site | Fire, theft, or loss of the machine and its local backups. | A usable copy stored elsewhere. |

A rollback helps with an uncommitted mistake. It cannot undo a bad transaction after `COMMIT` as though it never happened. Crash recovery also cannot recover a disk whose only copy of the data and log is gone. This is why the recovery method must match the failure.

## Which copy is durable?

A database may have a changed **dirty page** in memory while the older page is still on disk. Memory disappears on a power loss. A disk write can also pass through operating system and device caches before it is truly durable. Databases use a log, careful write ordering, and storage flushes to bridge that gap.

Two buffer choices explain why recovery may need both redo and undo:

| Choice | Meaning | Recovery consequence |
| --- | --- | --- |
| **Steal** | A dirty page may be written before its transaction commits. | Uncommitted data might reach disk, so it must not remain visible after recovery. |
| **No-force** | A commit need not write every changed data page immediately. | Committed data might still be missing from data files, so recovery must be able to redo it. |

These are general database design terms. PostgreSQL uses write-ahead logging and row versions; its exact handling of aborted row versions is different from a simple textbook undo log. The key idea still holds: committed work must be recoverable even when data pages lag behind the log.

## A failure timeline

Suppose an account starts at `100`. Transaction T1 adds `20` and commits. Transaction T2 then subtracts `5` but does not commit. The server crashes. A correct recovered account has `120`. If T1's data page was never written, its committed change must be restored. If T2's tentative change reached disk, it must not count as a committed change.

There is also an awkward case for an application: the connection drops just as `COMMIT` is sent. The client may not know whether the server committed. Blindly repeating a payment could do it twice. Use a unique request ID or another idempotency rule, then check the recorded outcome after reconnecting.

You can safely see a transaction rollback without crashing a server. Run this in PostgreSQL:

```sql
CREATE TEMP TABLE recovery_demo (
    account_id INTEGER PRIMARY KEY,
    balance INTEGER NOT NULL
);
INSERT INTO recovery_demo VALUES (1, 100);

BEGIN;
UPDATE recovery_demo SET balance = balance + 20 WHERE account_id = 1;
SAVEPOINT before_extra_change;
UPDATE recovery_demo SET balance = balance - 5 WHERE account_id = 1;
ROLLBACK TO SAVEPOINT before_extra_change;
COMMIT;

SELECT balance FROM recovery_demo WHERE account_id = 1;
```

The result is `120`. The savepoint discards the second update. This shows transaction rollback, not crash recovery. Crash recovery needs the database's log and storage rules.

## Set a recovery goal

**Recovery point objective** (RPO) is the largest amount of recent data the plan may lose, measured in time. **Recovery time objective** (RTO) is how long service may be unavailable. If backups run every night and there is no other copy of later changes, a failure near the next backup could lose almost a day of work. If WAL is archived continuously, the possible loss can be much smaller, provided the needed WAL was actually saved.

Write down what must be restored: data, users and roles, configuration, application files, and any external files the database refers to. A backup is useful only when it can be restored. Test a restore on a separate system, check the result, and record how long it takes. Replication can help availability, but a mistaken `DELETE` may be copied to the replica too. Keep independent backups.

## Try it yourself

1. Which failure can a plain transaction rollback fix, and which one needs a backup?
2. Why can a committed transaction need redo after a crash?
3. What should an application do if it loses its connection while committing a payment?

## References

- [PostgreSQL reliability](https://www.postgresql.org/docs/current/wal-reliability.html)
- [PostgreSQL write-ahead logging](https://www.postgresql.org/docs/current/wal-intro.html)
- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
- [PostgreSQL transactions and savepoints](https://www.postgresql.org/docs/current/tutorial-transactions.html)
