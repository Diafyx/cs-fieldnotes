# Top Ratings in Feb 2020

Find the movie with the highest average rating from reviews written in February 2020. If averages tie, choose the movie whose title sorts first alphabetically. Return one movie.

## Sample data

```sql
CREATE TEMP TABLE movies (movie_id integer PRIMARY KEY, title text NOT NULL);
CREATE TEMP TABLE reviews (
  review_id integer PRIMARY KEY,
  movie_id integer NOT NULL,
  rating integer NOT NULL,
  rated_at timestamp NOT NULL
);
INSERT INTO movies VALUES (1, 'Alpha'), (2, 'Beta'), (3, 'Gamma');
INSERT INTO reviews VALUES
  (10, 1, 4, '2020-02-01 10:00:00'),
  (11, 1, 5, '2020-02-10 12:00:00'),
  (12, 2, 5, '2020-02-03 09:00:00'),
  (13, 2, 4, '2020-02-20 18:00:00'),
  (14, 3, 4, '2020-02-05 15:00:00'),
  (15, 3, 5, '2020-03-01 00:00:00');
```

## Solution

```sql
WITH february AS (
  SELECT movie_id, AVG(rating) AS average_rating
  FROM reviews
  WHERE rated_at >= '2020-02-01 00:00:00'
    AND rated_at < '2020-03-01 00:00:00'
  GROUP BY movie_id
), ranked AS (
  SELECT m.movie_id, m.title, f.average_rating,
         ROW_NUMBER() OVER (
           ORDER BY f.average_rating DESC, m.title, m.movie_id
         ) AS position
  FROM february AS f
  JOIN movies AS m ON m.movie_id = f.movie_id
)
SELECT movie_id, title, average_rating
FROM ranked
WHERE position = 1;
```

The answer is `(1, 'Alpha', 4.5)`. Alpha and Beta both average 4.5 in February, so Alpha wins the title tie. Gamma's March 1 review is outside the month and does not raise its February average. A movie with no February review is absent because there is no average to rank.

If the task asks for **all** movies tied at the highest average, use `DENSE_RANK() OVER (ORDER BY average_rating DESC)` and keep rank 1. Do not put the title in that rank's order, because doing so would split the average tie. A production report needs a clear time zone if `rated_at` stores instants rather than local timestamps.

## Check your understanding

1. Why does Beta not appear?
2. What would happen if the March 1 review were included?
3. How would you return both Alpha and Beta?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
