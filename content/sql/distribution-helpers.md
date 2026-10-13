# Distribution Helpers

`PERCENT_RANK`, `CUME_DIST`, and `NTILE` describe where a row sits in an ordered partition. They answer different questions. A percent rank is based on rank positions, cumulative distribution counts rows at or before a peer group, and `NTILE` divides ordered rows into numbered buckets.

## Compare the three results

```sql
WITH scores(player_id, points) AS (
  VALUES (1, 100), (2, 90), (3, 90), (4, 70)
)
SELECT player_id, points,
       PERCENT_RANK() OVER (ORDER BY points DESC) AS percent_rank,
       CUME_DIST() OVER (ORDER BY points DESC) AS cumulative_share,
       NTILE(2) OVER (ORDER BY points DESC, player_id) AS bucket
FROM scores
ORDER BY points DESC, player_id;
```

The percent ranks are `0`, about `0.3333`, about `0.3333`, and `1`. The cumulative shares are `0.25`, `0.75`, `0.75`, and `1`. The two players with 90 points are peers for the first two functions. The bucket numbers are `1, 1, 2, 2`; a bucket boundary can split a score tie because `NTILE` divides rows, not score levels.

`PERCENT_RANK` is `(rank - 1) / (row_count - 1)` when there is more than one row. It returns 0 for a one-row partition. `CUME_DIST` is the number of rows at or ahead of the current peer group divided by the number of rows in the partition. Its first value can be above zero. `NTILE(2)` tries to make two buckets as even as possible. The number of buckets must be a positive integer.

Use `PARTITION BY` when each department, team, or other group needs its own distribution. Add a stable tie breaker when assigning exact rows to buckets. Do not treat a bucket number as a percentile: it is a row grouping and can divide equal values.

## Check your understanding

1. Why do the two 90-point rows share percent rank and cumulative share?
2. Why can those same rows land in different buckets?
3. Does the first row always have cumulative share 0?

## Further reading

- [PostgreSQL distribution window functions](https://www.postgresql.org/docs/current/functions-window.html)
