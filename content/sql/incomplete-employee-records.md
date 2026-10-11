# Incomplete Employee Records

An employee record is incomplete when its ID appears in the employee table but not the salary table, or in the salary table but not the employee table. Return each incomplete ID once.

## Sample data

```sql
CREATE TEMP TABLE employees (employee_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE salaries (employee_id integer PRIMARY KEY, salary integer NOT NULL);
INSERT INTO employees VALUES (1, 'Ana'), (2, 'Ben'), (4, 'Dev');
INSERT INTO salaries VALUES (1, 50), (3, 60), (4, 70);
```

## Solution

```sql
SELECT e.employee_id
FROM employees AS e
WHERE NOT EXISTS (
  SELECT 1 FROM salaries AS s WHERE s.employee_id = e.employee_id
)
UNION
SELECT s.employee_id
FROM salaries AS s
WHERE NOT EXISTS (
  SELECT 1 FROM employees AS e WHERE e.employee_id = s.employee_id
)
ORDER BY employee_id;
```

The result is `2` and `3`. Ben lacks a salary row. Salary ID 3 lacks an employee row. IDs 1 and 4 are present in both tables. `UNION` combines the two directions and removes duplicates. With the primary keys shown, the two halves cannot overlap, but `UNION` still states that the output is a set of IDs.

A foreign key from `salaries.employee_id` to `employees.employee_id` would prevent the second kind of missing record in a well-maintained database. A left join in only one direction would miss that case. This query checks missing rows, not missing salary values inside an existing row.

## Check your understanding

1. Why does ID 3 appear?
2. What would a one-way left join miss?
3. Would a salary row with a `NULL` salary count as missing under this definition?

## Further reading

- [PostgreSQL EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html#FUNCTIONS-SUBQUERY-EXISTS)
- [PostgreSQL UNION](https://www.postgresql.org/docs/current/queries-union.html)
