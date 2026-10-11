# Correlated Subqueries

A correlated subquery refers to a value from the outer query. It answers a question for each outer row, such as “is this employee above the average salary in their own department?”

## Compare within a group

```sql
WITH employees(employee_id, department_id, salary) AS (
  VALUES (1, 10, 40), (2, 10, 80), (3, 20, 30), (4, 20, 50)
)
SELECT e.employee_id, e.department_id, e.salary
FROM employees AS e
WHERE e.salary > (
  SELECT AVG(e2.salary)
  FROM employees AS e2
  WHERE e2.department_id = e.department_id
)
ORDER BY e.employee_id;
```

The result is employees 2 and 4. Department 10 has average salary 60; department 20 has average 40. The reference to `e.department_id` connects each inner average to the current outer employee.

## Common mistakes

Without the inner `WHERE`, the query compares everyone with the company-wide average. Without aliases, a column name may bind to the wrong query level, especially after the schema changes. Qualify outer and inner references explicitly.

This example's scalar inner query always returns one row because `AVG` without `GROUP BY` returns one result, even when there are no matching employees. Its value would then be `NULL`, and the comparison would not pass `WHERE`. A correlated query does not promise that PostgreSQL will run the inner text from scratch for every row. The planner can choose another way to get the same answer. For large tables, inspect a real query plan and relevant indexes if performance matters.

## Check your understanding

1. Why are employees 2 and 4 returned?
2. How would removing the inner department condition change the question?
3. What does a comparison with a `NULL` inner average do in `WHERE`?

## Further reading

- [PostgreSQL scalar subqueries](https://www.postgresql.org/docs/current/sql-expressions.html#SQL-SYNTAX-SCALAR-SUBQUERIES)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
