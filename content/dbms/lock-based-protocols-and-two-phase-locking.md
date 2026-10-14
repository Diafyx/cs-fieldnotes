# Lock-Based Protocols and Two-Phase Locking

A lock makes a transaction wait when another transaction is using the same data in a conflicting way. Locking can protect a read followed by a write, stop two writers from changing the same row at once, and keep a transaction's work safe until it finishes. The database may lock rows, tables, or other resources depending on the operation.

## Shared and exclusive locks

In the textbook model, a **shared** lock, often called `S`, permits reading. Several transactions can hold S locks on one item. An **exclusive** lock, called `X`, permits writing and conflicts with another transaction's S or X lock on that item.

| Requested lock | Existing S | Existing X |
| --- | --- | --- |
| S | Allowed | Wait |
| X | Wait | Wait |

This simple table is a model. PostgreSQL has several row and table lock modes with more specific rules. Ordinary PostgreSQL reads normally use MVCC snapshots and do not need a row-level S lock that blocks writers. `SELECT ... FOR UPDATE` is an explicit way to lock selected rows for a later change.

## Two-phase locking

**Two-phase locking**, or 2PL, has a growing phase and a shrinking phase. A transaction can acquire locks during the growing phase. Once it releases its first lock, it cannot acquire another. Following this rule gives conflict-serializable schedules. It can still deadlock when transactions wait on each other.

Basic 2PL may release an X lock before commit. Another transaction could then read a value that is later rolled back. **Strict 2PL** holds X locks until the transaction commits or aborts, preventing dirty reads and dirty writes of those values. **Rigorous 2PL** holds both S and X locks until the end. A **conservative** variant gets all needed locks before doing work, which can avoid deadlocks but is hard when the needed rows are not known in advance.

The phases refer to lock acquisition and release, not to two-phase **commit**, which is a separate protocol used to coordinate commits across participants.

## Lock a row for a change

This PostgreSQL example uses a temporary table so it can be tried safely in one session:

```sql
CREATE TEMP TABLE stock (
    sku TEXT PRIMARY KEY,
    quantity INTEGER NOT NULL CHECK (quantity >= 0)
);

INSERT INTO stock VALUES ('PEN', 5);

BEGIN;
SELECT quantity FROM stock WHERE sku = 'PEN' FOR UPDATE;
UPDATE stock
SET quantity = quantity - 1
WHERE sku = 'PEN' AND quantity > 0;
COMMIT;

SELECT sku, quantity FROM stock;
```

The first `SELECT` returns `5`; the final query returns `(PEN, 4)`. `FOR UPDATE` holds a row lock until transaction end. The `quantity > 0` condition and `CHECK` give separate safeguards. A temporary table belongs to one session, so this example does not show another session waiting. Use a shared table in a scratch database to observe that behavior.

If the application only needs to decrement one known row, a single guarded `UPDATE ... WHERE quantity > 0` can be simpler than reading, then locking, then updating. Check how many rows it changed. A row lock on existing rows does not by itself protect a rule about rows that might be inserted later. A unique constraint or serializable transaction may be needed for such a rule.

## Costs and mistakes

Locks held for a long time make other work wait. Changing from an S lock to an X lock is called an upgrade; two transactions trying to upgrade the same item can deadlock. Acquire resources in a consistent order, keep transactions short, and retry an aborted transaction from its start when safe. PostgreSQL's MVCC plus locks is not simply a textbook 2PL implementation, so use its documented isolation rules when designing real SQL transactions.

## Try it yourself

1. Why can two S locks coexist while an X lock must wait?
2. What rule does 2PL impose after the first lock is released?
3. Why does a temporary table fail to demonstrate cross-session lock waiting?

## References

- [MIT lecture on transactions and locking](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/10b223dc3daf6fda4001272799b153a0_MIT6_830F10_lec10.pdf)
- [PostgreSQL explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html)
- [PostgreSQL MVCC overview](https://www.postgresql.org/docs/current/mvcc-intro.html)
