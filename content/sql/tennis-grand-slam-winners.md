# Tennis Grand Slam Winners

Each season row stores the winners of four tournaments. Count how many Grand Slam titles each player won across all seasons. Show only players who won at least once.

## Sample data

```sql
CREATE TEMP TABLE players (player_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE seasons (
  season_year integer PRIMARY KEY,
  australian_open integer,
  french_open integer,
  wimbledon integer,
  us_open integer
);
INSERT INTO players VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara'), (4, 'Dev');
INSERT INTO seasons VALUES
  (2024, 1, 2, 1, 2),
  (2025, 1, 1, 2, 3);
```

## Solution

```sql
WITH wins AS (
  SELECT australian_open AS player_id FROM seasons
  UNION ALL SELECT french_open FROM seasons
  UNION ALL SELECT wimbledon FROM seasons
  UNION ALL SELECT us_open FROM seasons
)
SELECT p.player_id, p.name, COUNT(*) AS titles
FROM wins AS w
JOIN players AS p ON p.player_id = w.player_id
GROUP BY p.player_id, p.name
ORDER BY titles DESC, p.player_id;
```

The result is Ana with 4 titles, Ben with 3, and Cara with 1. `UNION ALL` keeps every tournament win, even when the same player wins several events. Plain `UNION` would collapse repeated player IDs and give the wrong counts. Dev is absent because he won none.

If a season can have an unknown winner, a `NULL` winner will not join to a player. A separate results table with one row per tournament is easier to query and can enforce a unique key for each event and year.

## Check your understanding

1. Why is `UNION ALL` required?
2. Why is Dev absent?
3. How would the data model change if tournaments were stored one per row?

## Further reading

- [PostgreSQL UNION and UNION ALL](https://www.postgresql.org/docs/current/queries-union.html)
- [PostgreSQL WITH queries](https://www.postgresql.org/docs/current/queries-with.html)
