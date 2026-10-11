# Restaurant Payment Trends

For each day with a full seven-day history, show the total paid across that day and the six days before it, plus the average paid per day. This example has at least one payment on every calendar day. Several customers can pay on the same day.

## Sample data

```sql
CREATE TEMP TABLE payments (
  payment_id integer PRIMARY KEY,
  paid_on date NOT NULL,
  amount integer NOT NULL
);
INSERT INTO payments VALUES
  (1, '2026-01-01', 10), (2, '2026-01-02', 20),
  (3, '2026-01-03', 30), (4, '2026-01-04', 10),
  (5, '2026-01-04', 30), (6, '2026-01-05', 50),
  (7, '2026-01-06', 60), (8, '2026-01-07', 70),
  (9, '2026-01-08', 80);
```

## Solution

```sql
WITH daily AS (
  SELECT paid_on, SUM(amount) AS day_amount
  FROM payments
  GROUP BY paid_on
), rolling AS (
  SELECT paid_on,
         SUM(day_amount) OVER (
           ORDER BY paid_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
         ) AS seven_day_amount,
         COUNT(*) OVER (
           ORDER BY paid_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
         ) AS days_seen
  FROM daily
)
SELECT paid_on, seven_day_amount,
       ROUND(seven_day_amount / 7.0, 2) AS average_per_day
FROM rolling
WHERE days_seen = 7
ORDER BY paid_on;
```

January 7 has a seven-day total of `280` and average `40`. January 8 has a total of `350` and average `50`. The first CTE combines the two January 4 payments into `40`. The window then works over daily rows, not individual payments. `days_seen = 7` removes the first six days because they have no full history yet.

`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` means seven rows, not automatically seven calendar days. It works here because every date is present exactly once after `daily` groups the payments. If days can have no payments, build a calendar of dates and join daily totals onto it, filling missing days with zero before using this window. A missing day otherwise makes the window reach farther back than six days.

## Check your understanding

1. Why must payments be grouped by day before the window calculation?
2. Why does January 6 not appear in the output?
3. What breaks if January 3 has no row in `daily`?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL window frames](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)
