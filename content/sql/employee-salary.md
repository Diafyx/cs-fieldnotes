# Employee Salary

This exercise applies a one-time raise to employees in one department. An `UPDATE` can calculate a new salary from the stored salary, while a flag keeps the same raise from being applied twice.

## The question

Give Engineering employees a ten percent raise. Do not change Sales employees. Each row has a `raise_applied` flag that starts false. Return all employees after the change, sorted by ID.

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL,
  department text NOT NULL,
  salary numeric(12, 2) NOT NULL CHECK (salary >= 0),
  raise_applied boolean NOT NULL DEFAULT false
);

INSERT INTO employees (employee_id, name, department, salary) VALUES
  (1, 'Asha', 'Engineering', 50000.00),
  (2, 'Ben', 'Engineering', 60000.00),
  (3, 'Cara', 'Sales', 70000.00);
```

## A solution

```sql
UPDATE employees
SET salary = ROUND(salary * 1.10, 2),
    raise_applied = true
WHERE department = 'Engineering'
  AND raise_applied = false;
```

Both Engineering salaries rise. The Sales salary does not change. The flag and salary change in one statement, so a successful update records that the raise was applied to those rows.

Check the result:

```sql
SELECT employee_id, salary, raise_applied
FROM employees
ORDER BY employee_id;
```

The rows are `(1, 55000.00, true)`, `(2, 66000.00, true)`, and `(3, 70000.00, false)`. Running the update again matches no Engineering rows because their flags are now true. A ten percent raise means multiplying by 1.10; adding 10 would mean ten currency units, which is a different rule.

A single Boolean flag only tracks this one raise. If the business has many raise rounds, store each round with its own ID and record which employees received it. That gives a useful history and prevents one flag from blocking later, valid raises. For a real payroll change, review the candidate rows and rounding rule, then run the write in a transaction.

## Check your understanding

1. Why is Cara's salary unchanged?
2. What would happen if the flag condition were removed and the query ran twice?
3. Why is a single `raise_applied` flag insufficient for yearly raises?

## Further reading

- [PostgreSQL UPDATE](https://www.postgresql.org/docs/current/sql-update.html)
- [PostgreSQL numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html)
