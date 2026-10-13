# Ranking Functions

Ranking functions number rows inside an ordered partition. The key choice is what to do with equal sort values. `ROW_NUMBER` gives every row a different number. `RANK` shares a rank for ties and leaves a gap after them. `DENSE_RANK` shares a rank for ties without a gap.

## See a tie

```sql
WITH scores(player_id, points) AS (
  VALUES (1, 100), (2, 90), (3, 90), (4, 80)
)
SELECT player_id, points,
       ROW_NUMBER() OVER (ORDER BY points DESC, player_id) AS row_number,
       RANK() OVER (ORDER BY points DESC) AS rank_number,
       DENSE_RANK() OVER (ORDER BY points DESC) AS dense_rank_number
FROM scores
ORDER BY points DESC, player_id;
```

The row numbers are `1, 2, 3, 4`. The ranks are `1, 2, 2, 4`. The dense ranks are `1, 2, 2, 3`. Players 2 and 3 tie on points. Their row numbers differ because `player_id` breaks the tie for that one calculation.

Use `ROW_NUMBER <= 3` when you need at most three rows and can choose a tie rule. Use `DENSE_RANK <= 3` when you need the top three distinct score levels and all tied rows. `RANK <= 3` can return fewer than three rank positions after a tie. None of these forms promises one row per group unless the filter and tie rule do so.

For rankings within departments or teams, add `PARTITION BY department_id` or the relevant key inside each `OVER`. Put the ranking in a CTE before filtering it, since PostgreSQL does not allow a window call directly in `WHERE` at the same query level.

## Check your understanding

1. Why does player 4 have rank 4 but dense rank 3?
2. Which function returns exactly one first row after a complete tie rule?
3. Which function would you use for the top three distinct salary levels?

## Further reading

- [PostgreSQL ranking functions](https://www.postgresql.org/docs/current/functions-window.html)
