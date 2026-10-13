# Top 3 Salaries per Department

Return employees whose salaries are in the top three distinct salary levels in their department. Keep every employee tied at a qualifying salary. This can return more than three people from a department.

## Sample data

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  department_id integer NOT NULL,
  salary integer NOT NULL
);
INSERT INTO employees VALUES
  (1, 10, 100), (2, 10, 90), (3, 10, 90),
  (4, 10, 80), (5, 10, 70),
  (6, 20, 50), (7, 20, 40), (8, 20, 30), (9, 20, 20);
```

## Solution

```sql
SELECT department_id, employee_id, salary
FROM (
  SELECT e.department_id, e.employee_id, e.salary,
         DENSE_RANK() OVER (
           PARTITION BY e.department_id ORDER BY e.salary DESC
         ) AS salary_level
  FROM employees AS e
) AS ranked
WHERE salary_level <= 3
ORDER BY department_id, salary DESC, employee_id;
```

Department 10 returns employees 1, 2, 3, and 4, with salaries 100, 90, 90, and 80. Department 20 returns employees 6, 7, and 8, with salaries 50, 40, and 30. `DENSE_RANK` gives both 90 salaries level 2 and the 80 salary level 3. A `ROW_NUMBER <= 3` filter would drop one of the tied 90 or the 80, depending on its tie order.

The filter is outside the subquery because a window result cannot be used directly in the same query level's `WHERE`. If the requirement is exactly three employees per department, use `ROW_NUMBER` with a stated tie breaker. If salary can be null, define whether missing salaries rank at all before relying on the database's null sort order.

## Check your understanding

1. Why are four people returned from department 10?
2. Which salary level does 80 receive there?
3. How would the query change if the task asked for exactly three people?

## Further reading

- [PostgreSQL ranking functions](https://www.postgresql.org/docs/current/functions-window.html)
