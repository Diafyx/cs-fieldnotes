# Follow-up Game Activity

Find the fraction of players who logged in on the calendar day immediately after their first login. Count each player once. A login much later does not count as the required follow-up.

## Sample data

```sql
CREATE TEMP TABLE activity (
  player_id integer NOT NULL,
  login_day date NOT NULL,
  PRIMARY KEY (player_id, login_day)
);
INSERT INTO activity VALUES
  (1, '2026-01-01'), (1, '2026-01-02'),
  (2, '2026-01-01'), (2, '2026-01-03'),
  (3, '2026-01-04'),
  (4, '2026-01-04'), (4, '2026-01-05');
```

## PostgreSQL solution

```sql
WITH first_days AS (
  SELECT player_id, MIN(login_day) AS first_day
  FROM activity
  GROUP BY player_id
), returned AS (
  SELECT f.player_id,
         CASE WHEN EXISTS (
           SELECT 1
           FROM activity AS a
           WHERE a.player_id = f.player_id
             AND a.login_day = f.first_day + 1
         ) THEN 1 ELSE 0 END AS came_back
  FROM first_days AS f
)
SELECT ROUND(SUM(came_back) * 1.0 / NULLIF(COUNT(*), 0), 2) AS fraction
FROM returned;
```

The result is `0.50`. Players 1 and 4 came back the next day, so two of four players qualify. Player 2's January 3 visit is too late after a January 1 first login. PostgreSQL adds one calendar day with `date + 1`. The `NULLIF` avoids division by zero if there are no player rows.

The denominator is players who have at least one activity row. If your product has registered players who never logged in and they belong in the denominator, start from a player table and state that rule. An activity table with many rows on one day should still count a player once; the `first_days` CTE makes that clear.

## Check your understanding

1. Why does player 2 not qualify?
2. What is the denominator in this query?
3. Which table would you need to include registered players who never logged in?

## Further reading

- [PostgreSQL date arithmetic](https://www.postgresql.org/docs/current/functions-datetime.html)
- [PostgreSQL EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html)
