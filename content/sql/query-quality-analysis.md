# Query Quality Analysis

This exercise gives each named query two measures. Quality is the average of `rating / position`. Poor result percentage is the share of rows with a rating below 3, multiplied by 100.

## The question

Each row in `query_results` is one observed result. Position starts at 1, so division by zero is not possible. Rating is from 1 to 5. Return one row per `query_name` with both measures rounded to two decimal places.

```sql
CREATE TEMP TABLE query_results (
  result_id integer PRIMARY KEY,
  query_name text NOT NULL,
  position integer NOT NULL CHECK (position > 0),
  rating integer NOT NULL CHECK (rating BETWEEN 1 AND 5)
);

INSERT INTO query_results (result_id, query_name, position, rating) VALUES
  (1, 'alpha', 1, 4),
  (2, 'alpha', 2, 2),
  (3, 'alpha', 5, 5),
  (4, 'beta', 4, 2),
  (5, 'beta', 3, 3);
```

## A solution

```sql
SELECT query_name,
       ROUND(AVG(rating * 1.0 / position), 2) AS quality,
       ROUND(
         100.0 * SUM(CASE WHEN rating < 3 THEN 1 ELSE 0 END) / COUNT(*),
         2
       ) AS poor_percentage
FROM query_results
GROUP BY query_name
ORDER BY query_name;
```

For `alpha`, the quality inputs are 4, 1, and 1, so quality is 2.00. One of its three ratings is poor, so the percentage is 33.33. For `beta`, the quality inputs are 0.5 and 1, so quality is 0.75. One of its two ratings is poor, so the percentage is 50.00.

The `1.0` and `100.0` keep fractional results in PostgreSQL. Integer division can lose them. `ELSE 0` makes a non-poor row count as zero rather than disappear from the sum. The sample has no missing ratings or positions. If those can be missing in real data, define whether they should count in either measure.

## Check your understanding

1. Why is `rating / position` calculated for each row before taking `AVG`?
2. What would happen if `ELSE 0` were omitted from the poor count?
3. Why is `position > 0` part of the table rule?

## Further reading

- [LeetCode Queries Quality and Percentage](https://leetcode.com/problems/queries-quality-and-percentage/)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL mathematical functions](https://www.postgresql.org/docs/current/functions-math.html)
