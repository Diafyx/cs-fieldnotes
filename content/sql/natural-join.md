# NATURAL JOIN

A `NATURAL JOIN` automatically matches on every column name shared by its two inputs. That can make a short query, but it can also match on a column you did not mean to use.

```sql
WITH employees(employee_id, department_id, status) AS (
  VALUES (1, 10, 'active')
), departments(department_id, department_name, status) AS (
  VALUES (10, 'Sales', 'open')
)
SELECT employee_id, department_name
FROM employees NATURAL JOIN departments;
```

This returns no rows. `NATURAL JOIN` matches both `department_id` and `status`, since both names appear in both tables. The IDs match, but `active` and `open` do not. Those status fields describe different things.

Write the intended relationship explicitly:

```sql
WITH employees(employee_id, department_id, status) AS (
  VALUES (1, 10, 'active')
), departments(department_id, department_name, status) AS (
  VALUES (10, 'Sales', 'open')
)
SELECT e.employee_id, d.department_name
FROM employees AS e
JOIN departments AS d ON d.department_id = e.department_id;
```

This returns `(1, 'Sales')`. `JOIN ... USING (department_id)` is another explicit option when the key has the same name on both sides. `USING` lists the shared columns to match; `NATURAL` chooses all shared names automatically.

Adding a same-named column to either table can silently change a natural join's meaning later. If there are no shared column names at all, PostgreSQL treats it like a cross join. For study, understand what it does. In code that must keep working as schemas change, name the join keys.

## Check your understanding

1. Why does the first query return no rows despite matching department IDs?
2. Which shared column should this relationship actually use?
3. What happens if a new same-named column is added to both tables later?

## Further reading

- [PostgreSQL NATURAL and USING joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
