# SELF JOIN

A self join uses the same table twice in one query. Each use needs its own alias so SQL can tell which role a column has. A common example is an employee table that stores each employee's manager ID.

```sql
WITH employees(employee_id, name, manager_id) AS (
  VALUES (1, 'Asha', NULL),
         (2, 'Ben', 1),
         (3, 'Cara', 1)
)
SELECT e.name AS employee_name,
       m.name AS manager_name
FROM employees AS e
LEFT JOIN employees AS m ON m.employee_id = e.manager_id
ORDER BY e.employee_id;
```

The result is `(Asha, NULL)`, `(Ben, Asha)`, and `(Cara, Asha)`. `e` means the employee row. `m` means the row that is that employee's manager. Asha stays because the left join keeps employees even when `manager_id` is `NULL`.

Use an inner self join if the question asks only for employees with a known manager. A self join can also compare pairs from one table, such as two points or two users. When finding unordered pairs, use a rule like `a.id < b.id` so `(a, b)` appears once and a row is not paired with itself.

An employee with a manager ID that points to no row gets a missing manager name in a left join. A foreign key can prevent that invalid reference. A self join does not check whether the management structure has a cycle; it only matches the IDs you give it.

## Check your understanding

1. Why does the query need both `e` and `m` aliases?
2. Why does Asha remain in the result?
3. What condition avoids returning both `(a, b)` and `(b, a)` when comparing pairs?

## Further reading

- [PostgreSQL table aliases and self joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-TABLE-ALIASES)
