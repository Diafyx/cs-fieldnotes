# Football Team Scores

Build a table of points and goals scored by each team. A win gives 3 points, a draw 1, and a loss 0. Show teams that have not played, with zero points and goals.

## Sample data

```sql
CREATE TEMP TABLE teams (team_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE games (
  home_team integer, away_team integer,
  home_goals integer NOT NULL, away_goals integer NOT NULL
);
INSERT INTO teams VALUES (1, 'Lions'), (2, 'Bears'), (3, 'Owls'), (4, 'Foxes');
INSERT INTO games VALUES (1, 2, 2, 0), (2, 3, 1, 1), (3, 1, 3, 2);
```

## Solution

```sql
WITH results AS (
  SELECT home_team AS team_id, home_goals AS goals,
         CASE WHEN home_goals > away_goals THEN 3
              WHEN home_goals = away_goals THEN 1 ELSE 0 END AS points
  FROM games
  UNION ALL
  SELECT away_team, away_goals,
         CASE WHEN away_goals > home_goals THEN 3
              WHEN away_goals = home_goals THEN 1 ELSE 0 END
  FROM games
)
SELECT t.team_id, t.name,
       COALESCE(SUM(r.points), 0) AS points,
       COALESCE(SUM(r.goals), 0) AS goals_scored
FROM teams AS t
LEFT JOIN results AS r ON r.team_id = t.team_id
GROUP BY t.team_id, t.name
ORDER BY points DESC, t.team_id;
```

The rows are Owls `(4, 4)`, Lions `(3, 4)`, Bears `(1, 1)`, and Foxes `(0, 0)`, with points then goals in each pair. The inner query turns each game into one row for each side. `UNION ALL` keeps both rows even if their values match. The left join keeps Foxes, and `COALESCE` turns its missing sums into zero.

The sample gives goals scored, not goal difference. Add goals conceded if the standings rule needs it. A real league may use more tie breakers; the shown `ORDER BY` uses team ID only for a stable display order among equal point totals.

## Check your understanding

1. Why does each game make two `results` rows?
2. Why does Foxes get zero rather than `NULL`?
3. What extra values would you need for goal difference?

## Further reading

- [PostgreSQL WITH queries](https://www.postgresql.org/docs/current/queries-with.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
