# Employees With or Without Salary Records

A salary report may need to show every employee, even before a salary record has been entered. A left join keeps the employees who have no match.

## The question

Return each employee ID, name, and salary amount. Use `NULL` when no salary record exists. Sort by employee ID.

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE current_salaries (
  employee_id integer PRIMARY KEY,
  amount numeric(12, 2) NOT NULL
);

INSERT INTO employees VALUES (1, 'Asha'), (2, 'Ben'), (3, 'Cara');
INSERT INTO current_salaries VALUES (1, 50000.00), (2, 60000.00);
```

## A solution

```sql
SELECT e.employee_id, e.name, s.amount
FROM employees AS e
LEFT JOIN current_salaries AS s
  ON s.employee_id = e.employee_id
ORDER BY e.employee_id;
```

The result has Asha with 50000, Ben with 60000, and Cara with `NULL`. Cara's missing salary record is not a salary of zero. Keeping `NULL` makes the missing record visible instead of inventing a number.

The salary table has one row per employee because `employee_id` is its primary key. Without that rule, two salary rows for one employee would make two result rows. A `WHERE s.amount > 0` condition would remove Cara after the join. If you need to filter which salary records match while keeping all employees, put that condition in `ON`.

## Check your understanding

1. Why does Cara still appear?
2. Why should her salary not automatically become zero?
3. What would happen if the salary table held two rows for Asha?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
