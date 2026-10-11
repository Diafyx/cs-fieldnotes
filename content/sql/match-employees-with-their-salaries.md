# Match Employees With Their Salaries

An inner join fits a report that asks only for employees who have a matching current salary row. Both tables use the same employee ID, but they store different facts.

## The question

Return employee ID, name, and salary for employees with a salary row. Sort by employee ID.

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE salaries (
  employee_id integer PRIMARY KEY,
  amount numeric(12, 2) NOT NULL
);

INSERT INTO employees VALUES (1, 'Asha'), (2, 'Ben'), (3, 'Cara');
INSERT INTO salaries VALUES (1, 50000.00), (3, 70000.00);
```

## A solution

```sql
SELECT e.employee_id, e.name, s.amount
FROM employees AS e
JOIN salaries AS s ON s.employee_id = e.employee_id
ORDER BY e.employee_id;
```

The output is `(1, Asha, 50000)` and `(3, Cara, 70000)`. Ben has no salary row, so he is absent. The matching ID connects each amount to the right name. A primary key on `salaries.employee_id` prevents one employee from matching several current salary rows.

This query only reads data. It does not create missing salaries. If payroll needs to find employees *without* salary rows, start from employees with a left join and test `s.employee_id IS NULL`. A foreign key from `salaries.employee_id` to `employees.employee_id` would prevent a salary from referring to a nonexistent employee.

## Check your understanding

1. Why is Ben absent?
2. What table rule keeps at most one current salary row per employee?
3. How could you find employees who are missing a salary row?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL primary keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS)
