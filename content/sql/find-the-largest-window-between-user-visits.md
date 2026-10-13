# Find the Largest Window Between User Visits

For each user, find the largest number of days from one visit to the next. For the last visit, use January 1, 2021 as the end. This fixed date is part of the question, so the answer does not change when the query is rerun later.

## Sample data

```sql
CREATE TEMP TABLE visits (user_id integer NOT NULL, visit_date date NOT NULL);
INSERT INTO visits VALUES
  (1, '2020-12-20'), (1, '2020-12-28'),
  (2, '2020-12-31'),
  (3, '2020-11-01'), (3, '2020-11-03'), (3, '2020-12-01');
```

## PostgreSQL solution

```sql
WITH unique_visits AS (
  SELECT DISTINCT user_id, visit_date
  FROM visits
  WHERE visit_date < '2021-01-01'
), next_visits AS (
  SELECT user_id, visit_date,
         LEAD(visit_date) OVER (
           PARTITION BY user_id ORDER BY visit_date
         ) AS next_day
  FROM unique_visits
)
SELECT user_id,
       MAX(COALESCE(next_day, '2021-01-01') - visit_date) AS largest_gap_days
FROM next_visits
GROUP BY user_id
ORDER BY user_id;
```

The answer is `(1, 8)`, `(2, 1)`, and `(3, 31)`. User 1's longest gap is December 20 to 28. User 2 has one visit, so the only window is December 31 to January 1. User 3's longest gap is December 1 to January 1. `LEAD` supplies the next visit and `COALESCE` supplies the fixed end when there is no next visit.

`SELECT DISTINCT` treats several visits on one day as one visit date. If the task instead measures time between individual visits, keep timestamps and do not deduplicate. PostgreSQL date subtraction returns whole days. Visits on or after the fixed end are excluded here; a real report should state its cutoff clearly.

## Check your understanding

1. Why does user 2 still have a window?
2. Why does user 3's answer include the fixed report date?
3. What would change if several visits on one day were meant to count separately?

## Further reading

- [PostgreSQL LEAD](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL date subtraction](https://www.postgresql.org/docs/current/functions-datetime.html)
