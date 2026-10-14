# Deadlock Handling

A deadlock happens when transactions form a circle of waits. Each holds something another needs, so none can finish without help. A long wait is not always a deadlock. If one transaction is still doing work and will release its lock, the other transaction can eventually continue.

## Follow the wait cycle

Suppose two accounts are stored as separate rows:

| Step | Session A | Session B |
| --- | --- | --- |
| 1 | Locks account 1. | |
| 2 | | Locks account 2. |
| 3 | Tries account 2 and waits for B. | |
| 4 | | Tries account 1 and waits for A. |

The **wait-for graph** has `A -> B` and `B -> A`. That cycle is the deadlock. PostgreSQL detects it and aborts one transaction. Do not assume which one will lose. The other can continue after the aborted transaction releases its locks.

To observe this in PostgreSQL, use two connections to a scratch database. Create the shared table once:

```sql
CREATE TABLE deadlock_lesson_accounts (
    account_id INTEGER PRIMARY KEY,
    balance INTEGER NOT NULL
);

INSERT INTO deadlock_lesson_accounts VALUES (1, 100), (2, 100);
```

Run the first `UPDATE` in A, then the first `UPDATE` in B. Run A's second `UPDATE`, which waits. Then run B's second `UPDATE` to complete the cycle.

```sql
-- Session A
BEGIN;
UPDATE deadlock_lesson_accounts SET balance = balance + 1 WHERE account_id = 1;
UPDATE deadlock_lesson_accounts SET balance = balance + 1 WHERE account_id = 2;
```

```sql
-- Session B
BEGIN;
UPDATE deadlock_lesson_accounts SET balance = balance + 1 WHERE account_id = 2;
UPDATE deadlock_lesson_accounts SET balance = balance + 1 WHERE account_id = 1;
```

The four update lines must be interleaved in the order above. After the error, roll back the failed transaction. The surviving transaction can then finish and commit. Drop `deadlock_lesson_accounts` after both sessions have ended. This example deliberately creates a deadlock, so keep it in a scratch database.

## Prevent, detect, and recover

| Method | Idea | Limit |
| --- | --- | --- |
| Consistent lock order | Every transaction locks shared resources in the same order. | Every code path must follow it. |
| Acquire all needed locks first | Wait before changing anything when a required lock is unavailable. | The full lock set may be unknown. |
| Timestamp-based prevention | Let an older or younger transaction wait or abort according to a fixed rule. | Aborts and retries can still cost work. |
| Detection | Find a cycle in the wait-for graph and abort one participant. | Some work must be repeated. |
| Timeout | Stop a wait after a limit. | A slow wait is not proof of a cycle. |

PostgreSQL detects deadlocks and reports SQLSTATE `40P01`. The application should roll back and retry the **whole transaction** when the operation is safe to repeat. A retry should not send the same external payment or email twice. Keep transactions short and acquire rows in a consistent order to reduce how often this happens.

`lock_timeout` can limit time spent waiting for a lock, but it is not a deadlock detector. `NOWAIT` and `SKIP LOCKED` can avoid some waits for specific queue-like designs, but they change what a query returns or whether it errors. Use them only when that behavior fits the task.

## Try it yourself

1. Why is step 3 alone only a wait, while step 4 creates a deadlock?
2. How would changing B to update account 1 before account 2 prevent this cycle?
3. Why must the retry include the first update as well as the second?

## References

- [PostgreSQL deadlocks and explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-DEADLOCKS)
- [PostgreSQL error codes](https://www.postgresql.org/docs/current/errcodes-appendix.html)
- [PostgreSQL lock timeout](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-LOCK-TIMEOUT)
- [MIT lecture on transactions and locking](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/10b223dc3daf6fda4001272799b153a0_MIT6_830F10_lec10.pdf)
