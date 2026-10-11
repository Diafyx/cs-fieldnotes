# Employees Earning More Than Their Manager

An employee table can point back to itself with `manager_id`. Join it to itself to put each employee's salary beside their manager's salary.

## The question

Return the employee name and manager name for employees whose salary is greater than their manager's salary. Sort by employee ID.

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL,
  salary numeric(12, 2) NOT NULL,
  manager_id integer
);

INSERT INTO employees VALUES
  (1, 'Asha', 100000.00, NULL),
  (2, 'Ben', 120000.00, 1),
  (3, 'Cara', 90000.00, 1),
  (4, 'Dev', 130000.00, 2);
```

## A solution

```sql
SELECT e.name AS employee_name, m.name AS manager_name
FROM employees AS e
JOIN employees AS m ON m.employee_id = e.manager_id
WHERE e.salary > m.salary
ORDER BY e.employee_id;
```

The result is `(Ben, Asha)` and `(Dev, Ben)`. Ben earns more than Asha, and Dev earns more than Ben. Cara earns less than Asha. Asha has no manager, so the inner join does not produce a manager row for her.

`e` and `m` are two roles for the same table. The query compares each employee with their *direct* manager, not everyone above them. Equal salaries do not pass the `>` condition. If salaries could be `NULL`, a comparison involving a missing salary would not pass either; the sample rules out missing salaries.

## Check your understanding

1. Why is Asha absent from the result?
2. Would Dev be compared with Asha by this query?
3. What change would include employees with equal salaries?

## Further reading

- [PostgreSQL table aliases and self joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-TABLE-ALIASES)
