# Orphan Employees

An orphan employee has a non-null manager ID that does not match any employee row. Find direct broken manager references. A root employee with no manager is not an orphan.

## Sample data

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL,
  manager_id integer
);
INSERT INTO employees VALUES
  (1, 'Asha', NULL), (2, 'Ben', 1),
  (3, 'Cara', 99), (4, 'Dev', 3);
```

## Solution

```sql
SELECT e.employee_id, e.name, e.manager_id
FROM employees AS e
WHERE e.manager_id IS NOT NULL
  AND NOT EXISTS (
    SELECT 1
    FROM employees AS m
    WHERE m.employee_id = e.manager_id
  )
ORDER BY e.employee_id;
```

The answer is `(3, 'Cara', 99)`. Manager 99 does not exist. Asha is a valid root because her manager ID is null. Dev's direct manager, Cara, exists, so Dev is not a direct orphan even though Cara's chain is broken above her. Finding everyone without a path to a valid head is a different, recursive task.

A foreign key from `manager_id` to `employee_id` would stop this missing-reference problem for new valid writes, while still allowing a null root. It would not by itself detect a cycle such as one employee managing themselves. If the data model allows manager IDs from another system, check that system's records instead of this table.

## Check your understanding

1. Why is Asha not an orphan?
2. Why does Dev not appear?
3. What constraint could prevent a manager ID of 99 when no such employee exists?

## Further reading

- [PostgreSQL EXISTS subqueries](https://www.postgresql.org/docs/current/functions-subquery.html)
- [PostgreSQL foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
