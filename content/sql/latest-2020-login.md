# Latest 2020 Login

Return each user's latest login during calendar year 2020. Users with no login in that year should not appear. The login column stores a timestamp without a time zone in this example.

## Sample data

```sql
CREATE TEMP TABLE logins (
  user_id integer NOT NULL,
  login_at timestamp NOT NULL
);
INSERT INTO logins VALUES
  (1, '2019-12-31 23:59:00'),
  (1, '2020-01-01 00:00:00'),
  (1, '2020-12-31 23:00:00'),
  (2, '2019-06-01 09:00:00'),
  (2, '2021-01-01 00:00:00'),
  (3, '2020-02-29 08:00:00');
```

## Solution

```sql
SELECT user_id, MAX(login_at) AS latest_login
FROM logins
WHERE login_at >= '2020-01-01 00:00:00'
  AND login_at < '2021-01-01 00:00:00'
GROUP BY user_id
ORDER BY user_id;
```

The result is user 1 at `2020-12-31 23:00:00` and user 3 at `2020-02-29 08:00:00`. User 2 has logins before and after 2020, but none inside it. The half-open range includes every time on December 31. `MAX` finds the latest time after the year filter has removed other years.

If the task also asks for the device used on that login, `MAX(login_at)` alone is not enough. Join to the matching row or rank rows, and decide what to do when two logins share the same latest time. For `timestamp with time zone`, first decide which time zone defines “the year 2020”; local and UTC boundaries may differ.

## Check your understanding

1. Why is user 2 absent?
2. Why does the filter end at the start of 2021 rather than the end of December 31?
3. What extra rule is needed to return one device when latest times tie?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
