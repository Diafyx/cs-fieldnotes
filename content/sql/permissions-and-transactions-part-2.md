# Permissions and Transactions Part-2

A transaction groups related writes into one unit. Other sessions do not see its uncommitted changes. `COMMIT` keeps the unit; `ROLLBACK` discards it. Permissions still apply to every statement inside the transaction.

## A small transfer

This is a simplified example with two known accounts:

```sql
CREATE TEMP TABLE balances (
  account_id integer PRIMARY KEY,
  balance numeric(12, 2) NOT NULL CHECK (balance >= 0)
);

INSERT INTO balances VALUES (1, 100.00), (2, 50.00);
```

```sql
BEGIN;
UPDATE balances SET balance = balance - 30 WHERE account_id = 1;
UPDATE balances SET balance = balance + 30 WHERE account_id = 2;
COMMIT;
```

Check the result:

```sql
SELECT account_id, balance FROM balances ORDER BY account_id;
```

The rows are `(1, 70.00)` and `(2, 80.00)`. The total stays 150. If a statement fails before commit, roll the transaction back. In a real transfer, the application must also check that both updates matched exactly one account, that the source has enough funds, and that a retry cannot apply the same transfer twice. A transaction alone does not prove those business rules.

## Other sessions can work at the same time

PostgreSQL's default `READ COMMITTED` isolation gives each statement a view of committed data when that statement starts. Two reads in one transaction can see different committed data if another session commits between them. Higher isolation levels change what can be seen and may require retrying a transaction after a conflict.

Row locks can make one writer wait for another. A long open transaction can keep locks longer than expected. Keep transactions focused, handle errors, and finish with a clear `COMMIT` or `ROLLBACK`. A savepoint can undo one later part while keeping earlier work in the same transaction.

## Check your understanding

1. What two balances should remain after the example commits?
2. Why must an application check the number of rows updated?
3. Can two `SELECT` statements in one default PostgreSQL transaction see different committed results?

## Further reading

- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
