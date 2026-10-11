# Date and Time Part Extraction Using YEAR(), MONTH(), DAY(), HOUR(), MINUTE(), and SECOND()

The title names functions used by some SQL systems. In PostgreSQL, use `EXTRACT(part FROM value)` for these parts. The input must contain the part you ask for. A `date` has a year and day, but no hour; a `time` has an hour, but no year.

## Read six parts

```sql
SELECT EXTRACT(YEAR FROM TIMESTAMP '2026-02-03 14:05:09') AS year_number,
       EXTRACT(MONTH FROM TIMESTAMP '2026-02-03 14:05:09') AS month_number,
       EXTRACT(DAY FROM TIMESTAMP '2026-02-03 14:05:09') AS day_number,
       EXTRACT(HOUR FROM TIMESTAMP '2026-02-03 14:05:09') AS hour_number,
       EXTRACT(MINUTE FROM TIMESTAMP '2026-02-03 14:05:09') AS minute_number,
       EXTRACT(SECOND FROM TIMESTAMP '2026-02-03 14:05:09') AS second_number;
```

The six values are `2026`, `2`, `3`, `14`, `5`, and `9`. PostgreSQL returns a numeric result from `EXTRACT`; seconds may include a fraction when the source has one. MySQL supports names such as `YEAR()` and `MONTH()` directly, so copy the syntax for the database you actually use.

## Parts are not durations

`EXTRACT(MONTH FROM DATE '2026-02-03')` returns `2`, which is February. It does not tell you that one month has passed since January 3. `EXTRACT(DAY FROM TIMESTAMP '2026-02-03 14:05:09')` returns the day of the month, not a total number of days. To measure elapsed time, subtract dates or timestamps instead.

When extracting parts from `timestamp with time zone`, PostgreSQL uses the session time zone to show the local date and time. The same instant can be February 3 in one zone and February 4 in another. Set the intended zone before grouping by year, month, or day. To group a whole month, use both year and month or use a month start value; grouping by month number alone merges every February from different years.

## Check your understanding

1. What does the example return for the hour?
2. Why does grouping only by `EXTRACT(MONTH ...)` mix different years?
3. Can a `date` value supply a minute number?

## Further reading

- [PostgreSQL EXTRACT](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT)
- [MySQL date and time functions](https://dev.mysql.com/doc/refman/8.4/en/date-and-time-functions.html)
