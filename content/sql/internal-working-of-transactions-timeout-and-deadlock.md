# Internal Working of Transactions, Timeout and Deadlock

A transaction lets several statements succeed or fail as one unit. PostgreSQL uses snapshots, locks, and a write-ahead log to make that work when many sessions use the database at once.

The usual four transaction properties are called ACID. **Atomicity** means the group commits or rolls back together. **Consistency** means each committed state must satisfy the database's constraints; application rules still need correct code. **Isolation** controls what concurrent transactions can observe. **Durability** means committed data survives a crash under the database's durability settings. These are separate promises. A transaction can be atomic while an application still makes a wrong business decision.

## Snapshots and isolation

PostgreSQL keeps row versions through multi-version concurrency control, or MVCC. A reader can see a consistent set of committed rows without waiting for every writer. An uncommitted update is visible to the transaction that made it, but not to other transactions.

The default isolation level is `READ COMMITTED`. Each statement gets a fresh view of committed data when it starts. If another transaction commits between two `SELECT` statements, the second query can see the new result. `REPEATABLE READ` keeps one transaction snapshot for ordinary reads. `SERIALIZABLE` also checks for outcomes that could not happen if transactions ran one at a time; it may abort a transaction that the application must retry. Isolation does not remove the need for clear business rules and constraints.

## Locks and deadlocks

Writes to the same row may conflict. One transaction can wait until another finishes. A deadlock happens when transactions wait in a circle. For example:

1. Session A updates account 1 and holds its row lock.
2. Session B updates account 2 and holds its row lock.
3. A tries to update account 2, while B tries to update account 1.

Neither can move forward. PostgreSQL detects the deadlock and cancels one transaction. The other can then continue. Update shared rows in a consistent order, keep transactions short, and retry the entire canceled transaction when a retry is safe. A retry must account for any work done outside the database.

Waiting for a lock is not always a deadlock. A transaction may simply be waiting for another to commit. A deadlock forms only when there is a cycle of waits. `lock_timeout` can end a long wait, while PostgreSQL's deadlock detector handles a cycle. Neither setting makes the canceled work commit.

## The write-ahead log

PostgreSQL records changes in its write-ahead log before writing changed data pages to their final files. If the server crashes, it can replay the log during recovery. A successful `COMMIT` normally means the transaction's log records have been made durable before success is reported. Durability can change with settings such as `synchronous_commit`, so check those settings when a system needs a specific guarantee.

## Timeouts

Timeouts stop work that takes too long, but they answer different questions:

| Setting | What it limits |
| --- | --- |
| `statement_timeout` | Time spent running a statement |
| `lock_timeout` | Time spent waiting to acquire a lock |
| `idle_in_transaction_session_timeout` | Time a session sits idle while a transaction remains open |

Set short limits for one transaction when a request has a known deadline:

```sql
BEGIN;
SET LOCAL lock_timeout = '2s';
SET LOCAL statement_timeout = '5s';
UPDATE accounts SET balance = balance - 10 WHERE account_id = 1;
COMMIT;
```

`SET LOCAL` lasts only until this transaction ends. These values are examples, not universal defaults. If a statement times out in a PostgreSQL transaction, the transaction is left in a failed state. Roll it back, or roll back to an earlier savepoint if that is part of the design. An idle transaction timeout ends the session, so the application must be ready to reconnect. PostgreSQL also has `transaction_timeout` for a limit on the whole transaction in versions that support it.

## Check your understanding

1. Why can two reads in one default transaction return different committed values?
2. What happens when two transactions wait on each other's row locks?
3. Which timeout applies to waiting for a lock, and which applies to a session left idle in a transaction?
4. Why should a deadlock retry restart the whole transaction?

## Further reading

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL MVCC](https://www.postgresql.org/docs/current/mvcc-intro.html)
- [PostgreSQL explicit locking and deadlocks](https://www.postgresql.org/docs/current/explicit-locking.html)
- [PostgreSQL write-ahead log](https://www.postgresql.org/docs/current/wal-intro.html)
- [PostgreSQL client connection settings](https://www.postgresql.org/docs/current/runtime-config-client.html)
