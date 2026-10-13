# Situation-12

## The question

Move 30.00 from account 1 to account 2. Account 1 starts with 100.00 and account 2 with 20.00. The transfer must not leave only one account changed. A retry with the same request ID must not move the money again.

```sql
CREATE TEMP TABLE accounts (
  account_id integer PRIMARY KEY,
  balance numeric(12, 2) NOT NULL CHECK (balance >= 0)
);
CREATE TEMP TABLE transfers (
  request_id text PRIMARY KEY,
  from_account integer NOT NULL REFERENCES accounts(account_id),
  to_account integer NOT NULL REFERENCES accounts(account_id),
  amount numeric(12, 2) NOT NULL CHECK (amount > 0),
  CHECK (from_account <> to_account)
);

INSERT INTO accounts VALUES (1, 100.00), (2, 20.00);
```

## Work through it

One database transaction groups the request record and both balance changes. The following statements show a successful first request. Run them one at a time from application code, check each result, and roll back if a required row is missing. Pasting the whole block without those checks is unsafe.

```sql
BEGIN;

INSERT INTO transfers VALUES ('move-1', 1, 2, 30.00)
ON CONFLICT (request_id) DO NOTHING
RETURNING request_id;
-- If no row was returned, stop here and roll back.

SELECT account_id, balance FROM accounts WHERE account_id = 1 FOR UPDATE;
SELECT account_id, balance FROM accounts WHERE account_id = 2 FOR UPDATE;

UPDATE accounts
SET balance = balance - 30.00
WHERE account_id = 1 AND balance >= 30.00
RETURNING balance;
-- If no row was returned, roll back.

UPDATE accounts
SET balance = balance + 30.00
WHERE account_id = 2
RETURNING balance;
-- If no row was returned, roll back.

COMMIT;
```

The insert returns `move-1` on the first attempt. The account read returns balances 100.00 and 20.00. The debit returns 70.00 and the credit returns 50.00. The sum stays 120.00. If any required insert or update returns no row, the application must issue `ROLLBACK` instead of continuing to `COMMIT`.

On a retry, the unique `request_id` makes the insert return no row. The application must stop before changing either balance, read the stored transfer row, and report that the first request succeeded. A request ID must always refer to the same source, destination, and amount; if a client reuses it with different details, report an error. A row in `transfers` that has committed with this transaction means the balance changes committed too.

All transfer paths should lock account rows in a consistent account ID order to reduce deadlocks. PostgreSQL can still abort a transaction because of a deadlock or serialization failure. Retry the whole transaction with the same request ID, not only the last SQL statement. Keep the transaction short. For a full financial system, use an immutable ledger of debits and credits as the audit record and reconcile it with stored balances.

## Check your understanding

1. Why must the application roll back when the debit returns no row?
2. What stops a repeated `move-1` request from moving another 30.00?
3. What should be retried after a deadlock aborts this transaction?

## Further reading

- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [PostgreSQL INSERT and ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html)
- [PostgreSQL explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html)
