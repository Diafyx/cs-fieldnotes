# Warmer Days

Return the IDs of days that were warmer than the actual previous calendar day. A missing day does not let the query compare with the most recent older row.

## Sample data

```sql
CREATE TEMP TABLE weather (
  weather_id integer PRIMARY KEY,
  record_date date NOT NULL UNIQUE,
  temperature integer NOT NULL
);
INSERT INTO weather VALUES
  (1, '2026-01-01', 10),
  (2, '2026-01-02', 15),
  (3, '2026-01-04', 18),
  (4, '2026-01-05', 17),
  (5, '2026-01-06', 20);
```

## PostgreSQL solution

```sql
SELECT today.weather_id, today.record_date
FROM weather AS today
JOIN weather AS yesterday
  ON today.record_date = yesterday.record_date + 1
WHERE today.temperature > yesterday.temperature
ORDER BY today.record_date;
```

The result is IDs 2 and 5. January 2 is warmer than January 1. January 6 is warmer than January 5. January 4 has no January 3 row, so it is not compared with January 2. PostgreSQL adds one calendar day when an integer is added to a `date`.

Using `LAG(temperature)` without checking dates would compare January 4 with January 2 and could answer the wrong question. If there can be several readings per day, decide whether to compare daily average, maximum, or a specific reading before joining. The unique date in this sample makes one reading per day explicit.

## Check your understanding

1. Why is January 4 absent even though 18 is above 15?
2. What does `yesterday.record_date + 1` produce in PostgreSQL?
3. What rule would you need if there were many temperature readings per day?

## Further reading

- [PostgreSQL date arithmetic](https://www.postgresql.org/docs/current/functions-datetime.html)
- [PostgreSQL joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
