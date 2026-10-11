# Find Transactions with Maximum Amount Per Day

For each day, return every transaction tied for the highest amount on that day. Keep the transaction ID so two transactions with the same amount stay separate.

## Sample data

```sql
CREATE TEMP TABLE transactions (
  transaction_id integer PRIMARY KEY,
  transaction_day date NOT NULL,
  amount integer NOT NULL
);
INSERT INTO transactions VALUES
  (10, '2026-01-01', 50), (11, '2026-01-01', 50),
  (12, '2026-01-01', 30), (13, '2026-01-02', 70);
```

## Solution

```sql
SELECT t.transaction_id, t.transaction_day, t.amount
FROM transactions AS t
WHERE t.amount = (
  SELECT MAX(t2.amount)
  FROM transactions AS t2
  WHERE t2.transaction_day = t.transaction_day
)
ORDER BY t.transaction_day, t.transaction_id;
```

The answer has transactions 10, 11, and 13. The inner maximum is calculated for the outer transaction's day. Both 10 and 11 equal the January 1 maximum, so both remain. Using `ROW_NUMBER()` would return one tied transaction unless the task asked for one winner.

The sample stores a date directly. If a production table stores timestamps, decide which time zone defines a business day before converting timestamps to dates. An amount can be zero or negative; `MAX` still finds the largest value. If amounts can be `NULL`, define whether null rows should be ignored or reported separately.

## Check your understanding

1. Why are there two rows for January 1?
2. What breaks if the inner day comparison is removed?
3. Why does a timestamp column need a time zone rule for this task?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
