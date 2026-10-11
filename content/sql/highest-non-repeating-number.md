# Highest Non-Repeating Number

Return the largest number that appears exactly once. If every number repeats, return `NULL`.

## Sample data

```sql
CREATE TEMP TABLE numbers (num integer NOT NULL);
INSERT INTO numbers VALUES (3), (3), (4), (5), (5), (8);
```

## Solution

```sql
SELECT MAX(num) AS highest_unique
FROM (
  SELECT num
  FROM numbers
  GROUP BY num
  HAVING COUNT(*) = 1
) AS singles;
```

The inner query leaves `4` and `8`. The outer `MAX` returns `8`. If the inner query is empty, `MAX` returns `NULL`, so the query still returns one row. `ORDER BY num DESC LIMIT 1` inside the outer query could find a largest value, but without an aggregate it would return no row when there is no unique number.

This definition counts rows. If the source has an event ID and duplicate events should be ignored, decide what makes an event distinct before grouping. A `NULL` number is excluded by the sample schema; allowing it would make `GROUP BY` place nulls in one group, and `MAX` would ignore that group even if it appeared once.

## Check your understanding

1. Why is 5 not the answer?
2. What does the outer aggregate return when all numbers repeat?
3. Why is the sample column marked `NOT NULL`?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL grouping](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP)
