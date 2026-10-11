# Employees and Their Departments

An employee may have a department ID, while the department name lives in another table. A left join can show every employee, including someone whose department has not been assigned.

## The question

Return each employee's ID and name with their department name. Keep employees with no department. Sort by employee ID.

```sql
CREATE TEMP TABLE departments (
  department_id integer PRIMARY KEY,
  department_name text NOT NULL
);
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL,
  department_id integer
);

INSERT INTO departments VALUES (10, 'Engineering'), (20, 'Sales');
INSERT INTO employees VALUES
  (1, 'Asha', 10), (2, 'Ben', 20), (3, 'Cara', NULL);
```

## A solution

```sql
SELECT e.employee_id, e.name, d.department_name
FROM employees AS e
LEFT JOIN departments AS d
  ON d.department_id = e.department_id
ORDER BY e.employee_id;
```

The rows are `(1, Asha, Engineering)`, `(2, Ben, Sales)`, and `(3, Cara, NULL)`. Cara stays because `employees` is on the left. Her missing department ID cannot match a department row. An inner join would omit her.

The department ID is unique in `departments`, so each employee can match at most one department. If the table allowed repeated department IDs, the same employee could appear several times. A foreign key could stop a non-null department ID from pointing to a missing department, but it would still allow `NULL` unless the employee column were also `NOT NULL`.

## Check your understanding

1. Why does Cara appear with a missing department name?
2. What would change if `LEFT JOIN` became `INNER JOIN`?
3. Which rule would stop an employee from naming department 99 when it does not exist?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
