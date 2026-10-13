# Situation-7

## The question

Of the customers active in January 2026, how many were active again in February 2026? Return the January customer count, the returning customer count, and the return percentage. A customer may have many activity rows in either month.

```sql
CREATE TEMP TABLE activity (
  activity_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  happened_on date NOT NULL
);

INSERT INTO activity VALUES
  (1, 1, '2026-01-05'), (2, 1, '2026-01-20'), (3, 1, '2026-02-05'),
  (4, 2, '2026-01-07'),
  (5, 3, '2026-01-08'), (6, 3, '2026-02-28'), (7, 3, '2026-02-28'),
  (8, 4, '2026-02-01');
```

The January group has customers 1, 2, and 3. Customers 1 and 3 return in February. The result is 3, 2, and 66.67 percent.

## Work through it

Make one January row per customer. For each of those customers, test whether any February row exists. Then count the flags.

```sql
WITH january AS (
  SELECT DISTINCT customer_id
  FROM activity
  WHERE happened_on >= '2026-01-01'
    AND happened_on < '2026-02-01'
), return_flags AS (
  SELECT j.customer_id,
         CASE WHEN EXISTS (
           SELECT 1 FROM activity AS a
           WHERE a.customer_id = j.customer_id
             AND a.happened_on >= '2026-02-01'
             AND a.happened_on < '2026-03-01'
         ) THEN 1 ELSE 0 END AS returned
  FROM january AS j
)
SELECT COUNT(*) AS january_customers,
       COALESCE(SUM(returned), 0) AS returning_customers,
       ROUND(100.0 * SUM(returned) / NULLIF(COUNT(*), 0), 2) AS return_percent
FROM return_flags;
```

The output is `(3, 2, 66.67)`. Customer 4 does not enter the January group. Customer 3's two February rows still count as one return. A direct join between January and February activity rows could multiply both sides and overcount people.

If January has no customers, the first two results are zero and the percentage is `NULL`. There is no meaningful percentage with a zero denominator. Define what "active" means before using this in a product report. A login, purchase, and page view may produce different groups.

## Check your understanding

1. Why does customer 4 not affect the denominator?
2. Why are duplicate February activity rows harmless with `EXISTS`?
3. What should a report display when the January group is empty?

## Further reading

- [PostgreSQL subquery expressions](https://www.postgresql.org/docs/current/functions-subquery.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
