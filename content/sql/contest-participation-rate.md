# Contest Participation Rate

For each contest, find the percentage of users who registered. Count a user once per contest. Include contests with no registrations.

## Sample data

```sql
CREATE TEMP TABLE users (user_id integer PRIMARY KEY);
CREATE TEMP TABLE contests (contest_id integer PRIMARY KEY);
CREATE TEMP TABLE registrations (contest_id integer, user_id integer);
INSERT INTO users VALUES (1), (2), (3), (4);
INSERT INTO contests VALUES (10), (20), (30);
INSERT INTO registrations VALUES (10, 1), (10, 2), (20, 1), (20, 3), (20, 4);
```

## Solution

```sql
SELECT c.contest_id,
       ROUND(100.0 * COUNT(DISTINCT r.user_id) /
             NULLIF((SELECT COUNT(*) FROM users), 0), 2) AS percentage
FROM contests AS c
LEFT JOIN registrations AS r ON r.contest_id = c.contest_id
GROUP BY c.contest_id
ORDER BY percentage DESC, c.contest_id;
```

The rows are `(20, 75)`, `(10, 50)`, and `(30, 0)`. The scalar subquery counts all four users. The left join keeps contest 30. `COUNT(DISTINCT r.user_id)` ignores the null from its unmatched row and avoids double counting a duplicate registration. `100.0` makes the division numeric. `NULLIF` avoids division by zero if the user table is empty; in that case the percentage is unknown rather than zero.

In a real schema, a unique key on `(contest_id, user_id)` should prevent repeated registration. If the question asks only for contests with registrations, an inner join would have a different result.

## Check your understanding

1. Why is contest 30 present?
2. What would a duplicate `(20, 1)` do without `DISTINCT`?
3. Why is an empty user table handled with `NULLIF`?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
