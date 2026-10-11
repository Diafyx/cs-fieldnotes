# Updated Bank Balances

An account has an opening balance. Each transaction adds a signed change: deposits are positive and withdrawals are negative. Join transactions to accounts and add the changes per account.

## The question

Return every account ID and its balance after the listed transactions. Show accounts with no transactions. Sort by account ID.

```sql
CREATE TEMP TABLE accounts (
  account_id integer PRIMARY KEY,
  opening_balance numeric(12, 2) NOT NULL
);
CREATE TEMP TABLE bank_transactions (
  transaction_id integer PRIMARY KEY,
  account_id integer NOT NULL,
  change_amount numeric(12, 2) NOT NULL
);

INSERT INTO accounts VALUES (1, 100.00), (2, 50.00), (3, 0.00);
INSERT INTO bank_transactions VALUES
  (10, 1, 25.00),
  (11, 1, -40.00),
  (12, 2, -10.00);
```

## A solution

```sql
SELECT a.account_id,
       a.opening_balance + COALESCE(SUM(t.change_amount), 0)
         AS updated_balance
FROM accounts AS a
LEFT JOIN bank_transactions AS t ON t.account_id = a.account_id
GROUP BY a.account_id, a.opening_balance
ORDER BY a.account_id;
```

The result is account 1 with 85, account 2 with 40, and account 3 with 0. Account 1 starts at 100, receives 25, then loses 40. Account 3 stays in the result because of the left join. Its sum is `NULL` before `COALESCE` supplies zero change.

This query calculates a report value. It does not update `accounts.opening_balance`. Each transaction must appear once. Joining transactions to another table with several rows per transaction before summing could repeat amounts. A real bank system also needs rules for pending entries, currency, reversals, and concurrent writes.

## Check your understanding

1. Why is account 1's result 85?
2. Does the query change the stored opening balance?
3. How could another one-to-many join make the balance wrong?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
