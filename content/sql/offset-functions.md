# Offset Functions

`LAG` reads a value from an earlier row in the same ordered partition. `LEAD` reads a later row. They are useful for changes, gaps, and comparisons with the next event. They do not remove rows.

## Compare nearby readings

```sql
WITH readings(account_id, reading_id, reading_day, units) AS (
  VALUES (1, 1, '2026-01-01', 10),
         (1, 2, '2026-01-02', 20),
         (1, 3, '2026-01-03', 40),
         (2, 4, '2026-01-01', 5)
)
SELECT account_id, reading_day, units,
       LAG(units) OVER (
         PARTITION BY account_id ORDER BY reading_day, reading_id
       ) AS previous_units,
       LEAD(units) OVER (
         PARTITION BY account_id ORDER BY reading_day, reading_id
       ) AS next_units
FROM readings
ORDER BY account_id, reading_day, reading_id;
```

Account 1 gets `(10, NULL, 20)`, `(20, 10, 40)`, and `(40, 20, NULL)` for current, previous, and next units. Account 2 has no neighbor, so both offset values are `NULL`. `PARTITION BY` stops account 1's last reading from looking into account 2.

`LAG(value, 2)` looks two rows back. `LAG(value, 1, 0)` uses `0` when no earlier row exists. That default does not replace an actual `NULL` stored in the earlier row. PostgreSQL respects null rows; it does not have the SQL standard `IGNORE NULLS` option for these functions.

An offset means another ordered row, not necessarily another calendar day. If a day is missing, `LAG` still returns the previous available row. Add a date check when the question specifically means yesterday. Include a stable tie breaker in `ORDER BY` if events can share a timestamp.

## Check your understanding

1. What is account 1's previous value on January 3?
2. Why does account 2 not see account 1's value 40?
3. Does `LAG(value, 1, 0)` replace an actual null in the previous row?

## Further reading

- [PostgreSQL LAG and LEAD](https://www.postgresql.org/docs/current/functions-window.html)
