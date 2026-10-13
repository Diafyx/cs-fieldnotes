# Core Mental Model (OVER, PARTITION BY, ORDER BY)

Read a window call as a calculation for each current row. `OVER` says which other rows the calculation may use. `PARTITION BY` chooses its group. `ORDER BY` gives that group a sequence. The calculation still returns one value for each input row.

## Two windows over the same rows

```sql
WITH scores(player_id, team, points) AS (
  VALUES (1, 'A', 10), (2, 'A', 20), (3, 'B', 5), (4, 'B', 7)
)
SELECT player_id, team, points,
       COUNT(*) OVER (PARTITION BY team) AS team_size,
       ROW_NUMBER() OVER (
         PARTITION BY team ORDER BY points DESC, player_id
       ) AS team_position
FROM scores
ORDER BY team, player_id;
```

Both teams have size 2. Player 2 is position 1 in team A; player 4 is position 1 in team B. The count needs a partition but no order because it asks for the whole team. The row number needs an order to say which player comes first. `player_id` settles any tie in points.

If `PARTITION BY team` is removed from `ROW_NUMBER`, there is one ranking across all four players. If the final `ORDER BY` is removed, the query still computes the same window values, but row display order is not promised. If a `WHERE` clause keeps only team A, both windows see only the surviving A rows.

The word “window” can mean a full partition or a smaller frame within it. Ranking functions use the partition and ordering. Running aggregates and `first_value`, `last_value`, and `nth_value` can also depend on the frame. Ask which rows each call is meant to see before choosing a frame.

## Check your understanding

1. Why does `COUNT(*) OVER (PARTITION BY team)` return 2 on every row?
2. What changes if the partition is removed from the row number?
3. Which `ORDER BY` controls the final row display?

## Further reading

- [PostgreSQL window tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)
- [PostgreSQL window syntax](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)
