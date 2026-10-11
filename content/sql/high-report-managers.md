# High-Report Managers

Find managers with at least three direct reports. A direct report points to the manager's employee ID. Reports further down the chain do not count for this question.

## Sample data

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL,
  manager_id integer
);
INSERT INTO employees VALUES
  (1, 'Asha', NULL), (2, 'Ben', 1), (3, 'Cara', 1), (4, 'Dev', 1),
  (5, 'Ema', 2), (6, 'Fay', 2), (7, 'Gia', 2), (8, 'Hari', 3);
```

## Solution

```sql
SELECT m.employee_id, m.name
FROM employees AS m
WHERE m.employee_id IN (
  SELECT e.manager_id
  FROM employees AS e
  WHERE e.manager_id IS NOT NULL
  GROUP BY e.manager_id
  HAVING COUNT(*) >= 3
)
ORDER BY m.employee_id;
```

The result is Asha and Ben. Three rows name Asha as manager, and three name Ben. Hari reports to Cara, so Cara has only one direct report. The inner query returns qualifying manager IDs; the outer query supplies their names. `manager_id IS NOT NULL` keeps the root employee out of the grouped IDs.

If the task asks for all people below a manager at any depth, this query is too narrow. A recursive query is needed for the full reporting tree. If manager IDs can point to a missing employee, the outer query will not return that missing manager.

## Check your understanding

1. Why does Cara not qualify?
2. Does Ema count as Asha's direct report?
3. Which part of the query gives the result names?

## Further reading

- [PostgreSQL grouping and HAVING](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP)
- [PostgreSQL IN subqueries](https://www.postgresql.org/docs/current/functions-subquery.html)
