# Filtering with Date Ranges

A date range needs clear start and end rules. For timestamps, a half-open range is often the easiest choice: include the start with `>=` and exclude the next period's start with `<`.

## Include a whole month

```sql
CREATE TEMP TABLE payments (
  payment_id integer PRIMARY KEY,
  paid_at timestamp NOT NULL
);
INSERT INTO payments VALUES
  (1, '2026-01-01 00:00:00'),
  (2, '2026-01-31 23:59:59.999'),
  (3, '2026-02-01 00:00:00'),
  (4, '2025-12-31 23:59:59');
```

```sql
SELECT payment_id
FROM payments
WHERE paid_at >= '2026-01-01 00:00:00'
  AND paid_at < '2026-02-01 00:00:00'
ORDER BY payment_id;
```

The answer is IDs 1 and 2. The range includes every January timestamp, including values more precise than a whole second. ID 3 is the first instant of February. ID 4 is before January.

`BETWEEN` includes both ends. `paid_at BETWEEN '2026-01-01' AND '2026-01-31'` would usually stop at midnight at the start of January 31, missing payments later that day. For a `date` column with no time of day, an inclusive last date can be fine, but the same half-open pattern also works.

Avoid applying `DATE(paid_at)` or `EXTRACT(YEAR FROM paid_at)` to every row just to filter a time range. Direct range comparisons can use an ordinary index on `paid_at` more naturally. Check the actual plan when performance matters. For `timestamp with time zone`, convert business-day boundaries from the intended local zone to instants before filtering; a UTC day and a local day can select different rows.

## Check your understanding

1. Why does the query include ID 2?
2. What is the first excluded timestamp after January?
3. Why is an inclusive end date risky for a timestamp column?

## Further reading

- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
- [PostgreSQL comparison operators](https://www.postgresql.org/docs/current/functions-comparison.html)
