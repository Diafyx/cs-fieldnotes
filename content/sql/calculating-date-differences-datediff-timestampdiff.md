# Calculating Date Differences (DATEDIFF, TIMESTAMPDIFF)

`DATEDIFF` and `TIMESTAMPDIFF` are names used in MySQL. PostgreSQL uses subtraction and intervals. Decide first whether you need calendar-day difference, elapsed hours, or a human-style age in years and months. Those are different results.

## Two PostgreSQL calculations

```sql
SELECT DATE '2026-03-05' - DATE '2026-03-01' AS days_apart,
       EXTRACT(EPOCH FROM (
         TIMESTAMP '2026-03-01 13:30:00'
         - TIMESTAMP '2026-03-01 10:00:00'
       )) / 3600 AS hours_apart;
```

The result is `4` days and `3.5` hours. Subtracting two `date` values returns an integer number of days. Subtracting two timestamps returns an `interval`. `EXTRACT(EPOCH FROM interval)` converts that interval to seconds; dividing by 3600 gives hours, including a fraction.

In MySQL, `DATEDIFF(later, earlier)` uses the date parts and returns days. `TIMESTAMPDIFF(unit, earlier, later)` returns an integer count in the chosen unit. In PostgreSQL, use `later_date - earlier_date` for days or timestamp subtraction for a duration. Keep the argument order clear: reversing the two values makes a negative result.

`age(later_timestamp, earlier_timestamp)` gives a symbolic interval with years, months, and days. It is useful for a calendar age, not for an exact number of elapsed seconds. Months have different lengths. For `timestamp with time zone`, subtracting two values measures elapsed time between instants; a local day near a daylight-saving change can be 23 or 25 hours. Define the time zone and the unit before calling a duration “one day.”

## Check your understanding

1. Why does the example return 3.5 hours rather than 3?
2. What type does PostgreSQL return when two timestamps are subtracted?
3. Why is `age` not a direct replacement for an exact elapsed-seconds calculation?

## Further reading

- [PostgreSQL date and time operators](https://www.postgresql.org/docs/current/functions-datetime.html)
- [MySQL date and time functions](https://dev.mysql.com/doc/refman/8.4/en/date-and-time-functions.html)
