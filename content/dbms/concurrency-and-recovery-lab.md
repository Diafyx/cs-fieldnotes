# Concurrency and Recovery Lab

A transaction can be correct when run alone and still break a rule when another transaction runs beside it. Recovery asks a different question: which changes remain after a rollback or crash? This lab makes both questions visible. Use a scratch PostgreSQL database and two separate connections for the concurrency part.

## Set up a shared rule

Two doctors are on call. The rule is that at least one must remain on call. Each doctor may leave only after checking that someone else is still on call. Create this ordinary table once so both connections can see it:

```sql
CREATE TABLE lab_doctors (
    doctor_id INTEGER PRIMARY KEY,
    on_call BOOLEAN NOT NULL
);

INSERT INTO lab_doctors VALUES (1, TRUE), (2, TRUE);
```

The database checks the type and primary key, but the cross-row rule is not in this table definition. A plain `CHECK` constraint examines a row, not a safe count of all rows under concurrent updates.

## Run the two sessions in order

Start two transactions at PostgreSQL's `REPEATABLE READ` level. Run each step in the listed order, switching between connection A and connection B. Do not run all of A before B. For this exercise, each application runs its `UPDATE` only when its own count is at least `2`.

| Step | Connection A | Connection B |
| --- | --- | --- |
| 1 | `BEGIN ISOLATION LEVEL REPEATABLE READ;` | |
| 2 | | `BEGIN ISOLATION LEVEL REPEATABLE READ;` |
| 3 | `SELECT COUNT(*) FROM lab_doctors WHERE on_call;` | |
| 4 | | `SELECT COUNT(*) FROM lab_doctors WHERE on_call;` |
| 5 | `UPDATE lab_doctors SET on_call = FALSE WHERE doctor_id = 1;` | |
| 6 | | `UPDATE lab_doctors SET on_call = FALSE WHERE doctor_id = 2;` |
| 7 | `COMMIT;` | |
| 8 | | `COMMIT;` |

Both counts at steps 3 and 4 are `2`. Each update touches a different row. Under PostgreSQL `REPEATABLE READ`, both transactions can commit, leaving zero on-call doctors. This is **write skew**: a decision depends on several rows, but each transaction changes a different row. A stable snapshot alone does not protect the rule.

Reset both rows with `UPDATE lab_doctors SET on_call = TRUE;` after both transactions end. Repeat the same schedule with `BEGIN ISOLATION LEVEL SERIALIZABLE;` in both connections. PostgreSQL must reject at least one transaction with a serialization failure, possibly when it commits. The application must roll back and retry the **whole** rejected transaction, including the count and the choice of doctor. The retry then sees one on-call doctor, so it skips the `UPDATE` and keeps that doctor on call. Do not retry only the `UPDATE`.

Another design is to lock one shared rule row before either transaction checks the count. All writers must follow that rule, and a lock can reduce concurrency. A check written only in application code is not enough if another writer ignores it. A deadlock is different from write skew: a deadlock is a cycle of waiting for locks, and PostgreSQL aborts one participant.

## See rollback and recovery separately

This single-connection example shows atomic rollback, not a real server crash:

```sql
CREATE TABLE lab_balance (
    account_id INTEGER PRIMARY KEY,
    amount INTEGER NOT NULL
);
INSERT INTO lab_balance VALUES (1, 100);

BEGIN;
UPDATE lab_balance SET amount = 70 WHERE account_id = 1;
ROLLBACK;

SELECT amount FROM lab_balance WHERE account_id = 1;
```

The result is `100`. The update was undone because its transaction did not commit. Remove `lab_balance` after the exercise.

For a crash, imagine committed transaction T1 changed A from `100` to `80`, and uncommitted transaction T2 changed B from `50` to `70`. After recovery, A should be `80` and B should be `50`. The exact redo and undo steps depend on the database recovery method, but the committed effect must remain and the uncommitted effect must not appear as a finished transaction. PostgreSQL uses WAL and crash recovery to restore its data files to a consistent state.

A server crash is not the same as a lost disk or an accidental deletion. Test restores from backups in a separate test instance. For a point-in-time restore, you need a suitable base backup and the required WAL archive up to the target. Record the latest point you can restore to and how long the restore takes. A replica can copy a bad delete; it is not a backup.

## Try it yourself

1. Why can the two `REPEATABLE READ` updates commit even though the final count breaks the rule?
2. Why must the failed serializable transaction repeat its count after retrying?
3. What would the `lab_balance` query return if the transaction committed instead of rolling back?
4. What can a backup restore after an accidental delete that a normal replica may not?

## References

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL serialization failure handling](https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html)
- [PostgreSQL explicit locking and deadlocks](https://www.postgresql.org/docs/current/explicit-locking.html)
- [PostgreSQL backup and point-in-time recovery](https://www.postgresql.org/docs/current/continuous-archiving.html)
