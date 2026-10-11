# Find All Employees Reporting to the Head of the Company

Find every employee below the company head, at any depth. The head has employee ID 1. Do not include the head in the result.

## Sample data

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL,
  manager_id integer
);
INSERT INTO employees VALUES
  (1, 'Asha', NULL), (2, 'Ben', 1), (3, 'Cara', 2),
  (4, 'Dev', 1), (5, 'Ema', 4), (6, 'Fay', NULL);
```

## Solution

```sql
WITH RECURSIVE reports(employee_id, name) AS (
  SELECT e.employee_id, e.name
  FROM employees AS e
  WHERE e.manager_id = 1
  UNION ALL
  SELECT e.employee_id, e.name
  FROM employees AS e
  JOIN reports AS r ON e.manager_id = r.employee_id
)
SELECT employee_id, name
FROM reports
ORDER BY employee_id;
```

The answer is Ben, Cara, Dev, and Ema. The first query finds the head's direct reports. The recursive query then finds reports of each person already found. Fay is outside this reporting tree. A simple self join only reaches a fixed number of levels; recursion keeps going until no new rows are found.

This assumes each employee has at most one manager and the hierarchy has no cycles. A cycle such as A manages B and B manages A can make `UNION ALL` keep producing rows. Real data needs a rule that prevents cycles or a recursive query that tracks visited IDs. The head ID should come from trusted input or a table, not be guessed from a missing manager value if several roots exist.

## Check your understanding

1. Why does Cara appear though she does not report directly to Asha?
2. Why is Fay absent?
3. What data error can make this query repeat indefinitely?

## Further reading

- [PostgreSQL recursive WITH queries](https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-RECURSIVE)
