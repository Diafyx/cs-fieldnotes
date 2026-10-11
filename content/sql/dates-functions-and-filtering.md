# Dates: Functions and Filtering

SQL date work starts with choosing the right type. In PostgreSQL, `date` stores a calendar day, `time` stores a time of day, `timestamp` stores a date and time without a time zone, and `timestamp with time zone` represents a point in time. An `interval` represents a span that can include months, days, and time.

## Filter a month

This example uses local timestamps with no time zone:

```sql
CREATE TEMP TABLE events (
  event_id integer PRIMARY KEY,
  happened_at timestamp NOT NULL
);
INSERT INTO events VALUES
  (1, '2026-02-28 23:59:59'),
  (2, '2026-03-01 00:00:00'),
  (3, '2026-03-31 23:59:59'),
  (4, '2026-04-01 00:00:00');
```

```sql
SELECT event_id, happened_at
FROM events
WHERE happened_at >= '2026-03-01 00:00:00'
  AND happened_at < '2026-04-01 00:00:00'
ORDER BY happened_at;
```

The result contains events 2 and 3. The first instant of April is outside the range. This style includes every possible time in March, even if a value has fractions of a second.

## Pick the operation you need

Use `EXTRACT` to read a part such as the year or hour. Use `date_trunc` to round a timestamp down to the start of a month or day. Add or subtract an `interval` to move a timestamp. Subtract two `date` values to get whole days in PostgreSQL. These operations answer different questions; extracting a month number does not tell you how many months passed.

For real events across time zones, store an instant in `timestamp with time zone` and decide which local zone defines a reporting day. PostgreSQL converts that type for display using the session time zone. A plain `timestamp` has no such conversion. A `NULL` date or timestamp does not pass an ordinary range comparison; handle missing values separately if they matter.

## Check your understanding

1. Why is event 3 included but event 4 excluded?
2. Which type should represent one exact event time across time zones?
3. Does `EXTRACT(MONTH FROM ...)` measure elapsed months?

## Further reading

- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
- [PostgreSQL date and time functions](https://www.postgresql.org/docs/current/functions-datetime.html)
