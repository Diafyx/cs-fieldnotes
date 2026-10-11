# First Login Analysis

Find the first recorded login date for each player. This is a `MIN` problem: the earliest date is the smallest date in each player's group.

## The question

Each row in `activity` records a player login on one date. Return `player_id` and `first_login`. Sort by player ID.

```sql
CREATE TEMP TABLE activity (
  player_id integer NOT NULL,
  event_date date NOT NULL,
  device_id integer NOT NULL,
  PRIMARY KEY (player_id, event_date)
);

INSERT INTO activity (player_id, event_date, device_id) VALUES
  (1, '2026-02-10', 4),
  (1, '2026-01-03', 2),
  (2, '2026-03-05', 1),
  (3, '2026-02-01', 3),
  (3, '2026-02-09', 3);
```

## A solution

```sql
SELECT player_id, MIN(event_date) AS first_login
FROM activity
GROUP BY player_id
ORDER BY player_id;
```

The output is `(1, 2026-01-03)`, `(2, 2026-03-05)`, and `(3, 2026-02-01)`. Each group contains one player's dates. `MIN` chooses the earliest date in that group. `device_id` is not needed because the question does not ask which device was used first.

If the table stored login timestamps, use `MIN(login_at)` to find the first instant. Converting timestamps to dates before taking `MIN` would lose the time within a day. Players with no activity do not appear because there is no row to group; showing them needs a player table and a join.

## Check your understanding

1. Why is `GROUP BY player_id` needed?
2. Would `MIN(device_id)` tell you which device was used on the first date?
3. How would the result change if the source stored timestamps instead of dates?

## Further reading

- [LeetCode Game Play Analysis I](https://leetcode.com/problems/game-play-analysis-i/)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
