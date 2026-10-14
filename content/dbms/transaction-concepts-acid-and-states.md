# Transaction Concepts, ACID, and States

A transaction groups database work into one unit. Either its changes are kept with `COMMIT`, or they are undone with `ROLLBACK`. This matters when one real action needs several statements, such as moving money between two accounts.

## What ACID means

| Property | Meaning | What it does not promise |
| --- | --- | --- |
| Atomicity | A transaction's changes are committed together or rolled back together. | The application checked every business rule. |
| Consistency | A committed state satisfies the rules the database enforces. | Every important rule was declared or coded correctly. |
| Isolation | Concurrent work sees results according to the chosen isolation level. | Every isolation level behaves as if work ran one transaction at a time. |
| Durability | Committed changes survive a crash under the database's durability settings. | Data can never be lost through hardware failure or bad operations. |

PostgreSQL uses a write-ahead log, or WAL, for crash recovery. It records changes in the log before changed table pages need to be written to their final files. Durability still depends on configuration and storage behavior. A backup is needed for failures such as accidental deletion that a committed transaction correctly recorded.

## A small transfer

```sql
CREATE TEMP TABLE balances (
    account_id INTEGER PRIMARY KEY,
    balance INTEGER NOT NULL CHECK (balance >= 0)
);

INSERT INTO balances VALUES (1, 100), (2, 50);

BEGIN;
UPDATE balances SET balance = balance - 30 WHERE account_id = 1;
UPDATE balances SET balance = balance + 30 WHERE account_id = 2;
COMMIT;

SELECT account_id, balance
FROM balances
ORDER BY account_id;
```

The result is `(1, 70)` and `(2, 80)`. The total stays `150`. If the second update fails, the application must roll back the transaction instead of treating the first update as a completed transfer. It must also check that both account IDs exist and that each `UPDATE` affected exactly one row. The `CHECK` stops a negative balance, but a transaction alone does not stop a transfer from being repeated twice.

In PostgreSQL, a statement error inside an explicit transaction leaves it in a failed state. Use `ROLLBACK`, or roll back to a savepoint created before the failing work. A savepoint undoes part of a transaction; it does not commit the earlier part by itself.

## Transaction states

Textbooks often describe these states:

| State | Meaning |
| --- | --- |
| Active | Statements are running or the transaction is waiting for more work. |
| Partially committed | The last statement has finished, but commit is not yet secured. |
| Committed | The database accepted the commit. |
| Failed | An error or conflict means the current work cannot finish as planned. |
| Aborted | The transaction's changes have been rolled back. |

These are a model for reasoning, not five SQL commands. In an application, end each transaction clearly. Leaving it open can hold locks and old row versions longer than needed. A single statement outside an explicit `BEGIN` also runs in a transaction when the client uses the usual autocommit behavior.

Some effects are outside the transaction. An email sent before `COMMIT` cannot be rolled back by the database. In PostgreSQL, sequence values consumed by `nextval` are not put back by a rollback. Use a separate design for external work that must happen only after a successful commit.

## Try it yourself

1. If the second `UPDATE` affects zero rows, which ACID property notices the missing account?
2. What should the application do after a failed statement in an explicit PostgreSQL transaction?
3. Why does a database rollback not undo an email already sent?

## References

- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [PostgreSQL savepoints](https://www.postgresql.org/docs/current/sql-savepoint.html)
- [PostgreSQL write-ahead logging](https://www.postgresql.org/docs/current/wal-intro.html)
- [PostgreSQL isolation and sequence behavior](https://www.postgresql.org/docs/current/transaction-iso.html)
