# Timestamp Ordering, Optimistic Control, and MVCC

Databases need a rule for concurrent reads and writes. Timestamp ordering, optimistic concurrency control, and multi-version concurrency control are three related ideas. They solve different parts of the problem and can be combined in one system.

## Timestamp ordering

In a basic timestamp-ordering protocol, each transaction gets a timestamp that defines its intended serial order. The database tracks the latest read and write timestamps for an item. If an older transaction tries an operation that would break that order, it aborts and may restart with a new timestamp. This can avoid lock waits, but a busy transaction may have to retry repeatedly.

For example, if T2 has already written `X` and has a later timestamp than T1, letting T1 now read T2's value would contradict the order T1 before T2. The protocol rejects that read. A real implementation needs rules for writes, deletes, and recovery too. The timestamp here is a logical ordering tool, not necessarily a wall-clock time shown to a user.

## Optimistic control

Optimistic concurrency control, or OCC, works well when conflicts are uncommon. A transaction reads and prepares work, validates that the facts it relied on have not changed, then writes if validation succeeds. The common phases are **read**, **validate**, and **write**. A failed validation means the whole decision must be made again using fresh data.

A version column can give an application a simple check for one row. Suppose the application read `version = 0` and `available = 1` for a seat:

```sql
CREATE TEMP TABLE seats (
    seat_id INTEGER PRIMARY KEY,
    available INTEGER NOT NULL CHECK (available IN (0, 1)),
    version INTEGER NOT NULL
);

INSERT INTO seats VALUES (1, 1, 0);

UPDATE seats
SET available = 0, version = version + 1
WHERE seat_id = 1 AND available = 1 AND version = 0;

SELECT seat_id, available, version FROM seats;
```

The `UPDATE` changes one row, and the query returns `(1, 0, 1)`. If another transaction had changed that row first, the old version condition would match zero rows. The application must check the affected-row count, then read fresh values before retrying. All writers must follow the version rule for it to protect the row. A row version check alone does not protect a rule across several rows, such as "at least one doctor remains on call."

## Multiple versions and snapshots

MVCC keeps more than one physical version of a logical row. A reader uses a snapshot to choose which committed version it may see. This lets ordinary PostgreSQL reads proceed without waiting for many concurrent writes. An update creates a new row version; old versions need cleanup once no relevant transaction can see them. Writers can still block one another on the same row.

PostgreSQL uses MVCC with different snapshot rules at different isolation levels. At `READ COMMITTED`, each statement normally gets a new snapshot. At `REPEATABLE READ`, a transaction uses a stable snapshot for ordinary reads. Neither MVCC nor a stable snapshot alone proves that all committed transactions have a serial order. PostgreSQL's `SERIALIZABLE` level adds checks for dangerous dependencies and can abort work that must be retried.

Timestamp ordering, OCC, and MVCC are not three exclusive SQL settings. An MVCC database can use timestamps to label versions and validation or locks to decide which writers may commit. When choosing an application technique, state the business rule first, then test how conflicting transactions behave.

## Try it yourself

1. What does the seat `UPDATE` do if `version` has already become `1`?
2. Why does a stable snapshot still allow the two-doctor write skew example?
3. Why can a reader continue while a writer creates a newer row version?

## References

- [CMU notes on optimistic concurrency control](https://15721.courses.cs.cmu.edu/spring2018/notes/04-occ.pdf)
- [PostgreSQL MVCC overview](https://www.postgresql.org/docs/current/mvcc-intro.html)
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL heap-only tuples and row versions](https://www.postgresql.org/docs/current/storage-hot.html)
