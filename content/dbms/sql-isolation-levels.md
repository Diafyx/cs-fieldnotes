# SQL Isolation Levels

An isolation level sets which concurrent changes a transaction may observe and which outcomes the database must prevent. Stronger isolation can make a rule easier to reason about, but may add waiting, tracking, or retries. The SQL standard names four levels. Their exact behavior differs by database, so these notes use PostgreSQL.

| Level in PostgreSQL | What ordinary reads see | Important limit |
| --- | --- | --- |
| `READ UNCOMMITTED` | Behaves as `READ COMMITTED` in PostgreSQL. | It does not enable dirty reads. |
| `READ COMMITTED` | A fresh snapshot for each statement. This is the default. | Two reads in one transaction may differ. |
| `REPEATABLE READ` | One stable snapshot starting with the first query or data-changing statement. | Serialization anomalies such as write skew can still occur. |
| `SERIALIZABLE` | A stable view plus checks that committed work has a serial meaning. | A transaction may fail and need a full retry. |

A **dirty read** sees uncommitted data. A **nonrepeatable read** sees a changed row on a second read. A **phantom** is a changed set of rows for a repeated condition. PostgreSQL prevents dirty reads at every level. `READ COMMITTED` allows nonrepeatable and phantom reads across statements. PostgreSQL's `REPEATABLE READ` also prevents phantoms, even though the SQL standard permits them at that level. `SERIALIZABLE` rules out serialization anomalies for successfully committed transactions.

## See a changing value

To try this with two PostgreSQL connections, create a shared table in a scratch database:

```sql
CREATE TABLE isolation_lesson (
    id INTEGER PRIMARY KEY,
    value INTEGER NOT NULL
);

INSERT INTO isolation_lesson VALUES (1, 10);
```

In session A, run the first read and pause:

```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT value FROM isolation_lesson WHERE id = 1;
```

It returns `10`. In session B, change and commit the row:

```sql
BEGIN;
UPDATE isolation_lesson SET value = 20 WHERE id = 1;
COMMIT;
```

Now finish session A:

```sql
SELECT value FROM isolation_lesson WHERE id = 1;
COMMIT;
```

The second read returns `20` at `READ COMMITTED`. Reset the value to `10`, then repeat with `SET TRANSACTION ISOLATION LEVEL REPEATABLE READ` before A's first read. Its second read remains `10`, because A keeps its original snapshot. After both sessions end, drop `isolation_lesson`. Use `ORDER BY` only when a query returns several rows whose order matters.

## Choosing a level

`READ COMMITTED` is often enough when each statement enforces its own rule, such as one guarded update of a known row. A read followed by a later decision may need a row lock, a version check, a constraint, or a stronger level. `REPEATABLE READ` gives consistent ordinary reads within a transaction but does not stop every cross-row rule violation. `SERIALIZABLE` checks for results inconsistent with serial execution and may report SQLSTATE `40001`.

When a serialization failure occurs, roll back and retry the **whole transaction**, including its reads and decisions. Retrying only the last SQL statement reuses stale facts. Keep external actions such as payments or emails out of a retry path unless they have a safe deduplication rule. A transaction with no conflicting work may finish without any retry even at `SERIALIZABLE`.

Set the level before the first statement that reads or changes data in that transaction. A setting on one connection does not automatically set other connections in a pool. Check the actual level and test with two real sessions; a single-session example cannot show a concurrent anomaly.

## Try it yourself

1. Why does session A's second read change at `READ COMMITTED` but stay at `10` at `REPEATABLE READ`?
2. Does `READ UNCOMMITTED` permit a dirty read in PostgreSQL?
3. Why must a transaction that receives SQLSTATE `40001` repeat its earlier reads?

## References

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL error codes](https://www.postgresql.org/docs/current/errcodes-appendix.html)
- [PostgreSQL SET TRANSACTION](https://www.postgresql.org/docs/current/sql-set-transaction.html)
- [PostgreSQL MVCC overview](https://www.postgresql.org/docs/current/mvcc-intro.html)
