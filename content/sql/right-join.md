# RIGHT JOIN

A `RIGHT JOIN` keeps every row from the table written on the right. It adds matching values from the table on the left. When no left row matches, the left columns are `NULL`.

```sql
WITH departments(department_id, department_name) AS (
  VALUES (10, 'Sales'), (20, 'Support')
), employees(employee_id, department_id) AS (
  VALUES (1, 10), (2, 99)
)
SELECT e.employee_id, d.department_name
FROM departments AS d
RIGHT JOIN employees AS e
  ON d.department_id = e.department_id
ORDER BY e.employee_id;
```

The result is `(1, 'Sales')` and `(2, NULL)`. Employee 2 remains even though department 99 is absent. Department 20 does not appear because it has no matching employee and it is on the left. A nullable department ID would also leave an employee in the result with no match.

You can write the same relationship by swapping the tables and using `LEFT JOIN`:

```sql
WITH departments(department_id, department_name) AS (
  VALUES (10, 'Sales'), (20, 'Support')
), employees(employee_id, department_id) AS (
  VALUES (1, 10), (2, 99)
)
SELECT e.employee_id, d.department_name
FROM employees AS e
LEFT JOIN departments AS d
  ON d.department_id = e.department_id
ORDER BY e.employee_id;
```

Choose the form that makes the table you must keep easiest to see. If several employees share a department, the department name appears once per employee. If you filter `d.department_name` in `WHERE`, employee 2 may disappear; put a filter in `ON` when you want to keep unmatched employees.

## Check your understanding

1. Why does employee 2 appear with a missing department name?
2. Why does Support not appear in the result?
3. Which table should be on the left if you rewrite this as a `LEFT JOIN`?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
