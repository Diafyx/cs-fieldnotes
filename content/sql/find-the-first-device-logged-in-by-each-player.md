# Find the First Device Logged In by Each Player

For each player with a login, return the device used on their earliest login. If two logins have the same time, choose the smaller login ID so the answer is stable.

## Sample data

```sql
CREATE TEMP TABLE logins (
  login_id integer PRIMARY KEY,
  player_id integer NOT NULL,
  device text NOT NULL,
  login_at timestamp NOT NULL
);
INSERT INTO logins VALUES
  (10, 1, 'phone', '2026-01-01 09:00:00'),
  (11, 1, 'tablet', '2026-01-01 09:00:00'),
  (12, 1, 'laptop', '2026-01-02 08:00:00'),
  (13, 2, 'browser', '2026-01-03 10:00:00');
```

## Solution

```sql
SELECT player_id, device
FROM (
  SELECT player_id, device,
         ROW_NUMBER() OVER (
           PARTITION BY player_id ORDER BY login_at, login_id
         ) AS position
  FROM logins
) AS ranked
WHERE position = 1
ORDER BY player_id;
```

The answer is `(1, 'phone')` and `(2, 'browser')`. The subquery numbers each player's logins from earliest to latest. The outer query keeps one row per player. `login_id` breaks the tie for player 1. A query that selects `MIN(login_at)` and joins back may return both the phone and tablet rows unless it handles ties.

If the task wants all devices tied at the first instant, use `RANK()` and keep rank 1 instead. A player with no login cannot appear when `logins` is the only source table.

## Check your understanding

1. Why is the tablet not returned?
2. What changes if `RANK()` replaces `ROW_NUMBER()`?
3. How could you include players who have never logged in?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
