# Employees with the Highest Salary in Each Department

Return every employee whose salary equals the highest salary in their department. If two people tie for first, return both.

## Sample data

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL,
  department_id integer NOT NULL,
  salary integer NOT NULL
);
INSERT INTO employees VALUES
  (1, 'Ana', 10, 50), (2, 'Ben', 10, 70), (3, 'Cara', 10, 70),
  (4, 'Dev', 20, 40), (5, 'Ema', 20, 60);
```

## Solution

```sql
SELECT e.department_id, e.employee_id, e.name, e.salary
FROM employees AS e
WHERE e.salary = (
  SELECT MAX(e2.salary)
  FROM employees AS e2
  WHERE e2.department_id = e.department_id
)
ORDER BY e.department_id, e.employee_id;
```

The rows are Ben and Cara from department 10, then Ema from department 20. The inner query finds one maximum for the current employee's department. Equality keeps every tied employee. `ROW_NUMBER() = 1` would choose only one person and answer a different question.

The sample makes salaries non-null. If every salary in a department were `NULL`, `MAX` would be `NULL` and `salary = NULL` would not be true, so no employee from that department would appear. Decide how missing salaries should be handled before changing the query.

## Check your understanding

1. Why do both Ben and Cara appear?
2. What changes if the inner department condition is removed?
3. Why would `ROW_NUMBER() = 1` lose a tied winner?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL scalar subqueries](https://www.postgresql.org/docs/current/sql-expressions.html#SQL-SYNTAX-SCALAR-SUBQUERIES)
