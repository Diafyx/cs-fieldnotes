# Kid-Friendly Movies in Last Month

Find the unique kid-friendly movies streamed in the previous calendar month. For this worked example, assume the report runs on April 15, 2026, so “last month” means March 1 through March 31. A title streamed several times should appear once.

## Sample data

```sql
CREATE TEMP TABLE content (
  content_id integer PRIMARY KEY,
  title text NOT NULL,
  content_type text NOT NULL,
  is_kid_friendly integer NOT NULL
);
CREATE TEMP TABLE streams (
  stream_id integer PRIMARY KEY,
  content_id integer NOT NULL,
  streamed_at timestamp NOT NULL
);
INSERT INTO content VALUES
  (10, 'Sky', 'movie', 1), (11, 'River', 'movie', 1),
  (12, 'Forest', 'series', 1), (13, 'Night', 'movie', 0);
INSERT INTO streams VALUES
  (1, 10, '2026-03-03 10:00:00'), (2, 10, '2026-03-20 20:00:00'),
  (3, 11, '2026-03-31 23:30:00'), (4, 11, '2026-04-01 00:00:00'),
  (5, 12, '2026-03-10 12:00:00'), (6, 13, '2026-03-20 21:00:00'),
  (7, 10, '2026-02-28 22:00:00');
```

## Solution

```sql
SELECT DISTINCT c.content_id, c.title
FROM content AS c
JOIN streams AS s ON s.content_id = c.content_id
WHERE c.content_type = 'movie'
  AND c.is_kid_friendly = 1
  AND s.streamed_at >= '2026-03-01 00:00:00'
  AND s.streamed_at < '2026-04-01 00:00:00'
ORDER BY c.content_id;
```

The answer is Sky and River. Sky was streamed twice in March, but `DISTINCT` keeps one title row. Forest is a series, Night is not kid-friendly, and the April 1 stream is outside the range. There are two unique qualifying movies.

If the report asks for the **number** of unique titles instead, count distinct content IDs with the same filters:

```sql
SELECT COUNT(DISTINCT c.content_id) AS unique_movie_count
FROM content AS c
JOIN streams AS s ON s.content_id = c.content_id
WHERE c.content_type = 'movie'
  AND c.is_kid_friendly = 1
  AND s.streamed_at >= '2026-03-01 00:00:00'
  AND s.streamed_at < '2026-04-01 00:00:00';
```

This query returns `2`. Counting stream rows would return `3` because Sky was streamed twice in March.

For a live PostgreSQL report, the previous month starts at `date_trunc('month', CURRENT_DATE) - INTERVAL '1 month'` and ends at `date_trunc('month', CURRENT_DATE)`. This is a calendar month, not the last 30 days. Choose the reporting time zone before applying those boundaries to a `timestamp with time zone` column.

## Check your understanding

1. Why does Sky appear once?
2. Does the April 1 stream of River count for this report?
3. Why does `COUNT(DISTINCT c.content_id)` return 2 rather than 3?
4. How would a rolling 30-day report differ from a previous-calendar-month report?

## Further reading

- [PostgreSQL date_trunc](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-TRUNC)
- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
