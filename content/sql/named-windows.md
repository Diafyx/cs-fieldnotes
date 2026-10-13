# Named Windows

The `WINDOW` clause gives a name to a window definition. Several functions in one `SELECT` can use the same partition, order, or frame without copying the full `OVER (...)` text each time. The name exists only in that query.

## Name a team window

```sql
WITH scores(player_id, team, points) AS (
  VALUES (1, 'A', 10), (2, 'A', 20), (3, 'B', 5), (4, 'B', 7)
)
SELECT player_id, team, points,
       SUM(points) OVER by_team AS team_points,
       COUNT(*) OVER by_team AS team_size,
       ROW_NUMBER() OVER team_order AS place
FROM scores
WINDOW by_team AS (PARTITION BY team),
       team_order AS (PARTITION BY team ORDER BY points DESC, player_id)
ORDER BY team, player_id;
```

Team A has total points 30 and size 2 on both of its rows. Team B has total 12 and size 2. Player 2 is first in A, and player 4 is first in B. `by_team` has no order, so its aggregates see the whole team. `team_order` adds an order for `ROW_NUMBER`.

The `WINDOW` clause comes after `FROM`, `WHERE`, `GROUP BY`, and `HAVING`, and before the final `ORDER BY` in a `SELECT`. A named window can also copy parts of an earlier named window, subject to PostgreSQL's rules for adding an order or frame. Use a simple separate name when that is easier to read.

Naming a window does not make its result a stored table and does not guarantee that a query runs faster. It saves repeated definitions and helps prevent one function from accidentally using a different partition or order. Each function still returns a value for each row it processes.

## Check your understanding

1. Why does `team_points` repeat on both A rows?
2. Which named window gives a row order?
3. Can a later SQL statement refer to `by_team`?

## Further reading

- [PostgreSQL WINDOW clause](https://www.postgresql.org/docs/current/sql-select.html)
- [PostgreSQL window syntax](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)
