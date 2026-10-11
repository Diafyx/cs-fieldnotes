# Recursive CTEs for Hierarchies

A recursive CTE starts with known rows, then repeatedly finds rows connected to them. This is useful for an employee tree, category tree, or any path where the number of levels is not fixed in advance.

## Walk down a reporting tree

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL,
  manager_id integer
);
INSERT INTO employees VALUES
  (1, 'Asha', NULL), (2, 'Ben', 1),
  (3, 'Cara', 2), (4, 'Dev', 1), (5, 'Ema', NULL);
```

```sql
WITH RECURSIVE tree(employee_id, name, depth) AS (
  SELECT e.employee_id, e.name, 0
  FROM employees AS e
  WHERE e.employee_id = 1
  UNION ALL
  SELECT child.employee_id, child.name, parent.depth + 1
  FROM employees AS child
  JOIN tree AS parent ON child.manager_id = parent.employee_id
)
SELECT employee_id, name, depth
FROM tree
ORDER BY depth, employee_id;
```

The rows are Asha at depth 0, Ben and Dev at depth 1, and Cara at depth 2. Ema is outside Asha's tree. The first `SELECT` is the anchor. The second is the recursive step. It runs against newly found rows until it finds no more. `UNION ALL` keeps every row produced by the tree walk.

## Avoid loops and unclear order

This example assumes one manager per employee and no cycles. A bad cycle can make recursion keep producing rows. PostgreSQL has a `CYCLE` clause that tracks visited values; a path column can do the same job by hand. Simply using `UNION` instead of `UNION ALL` may not help when the output includes a changing depth.

The order in which recursive rows are produced is not a display guarantee. Use an outer `ORDER BY`. A depth number supports a level-based display; a path supports a tree-like display. If the table can be very large, make sure the parent lookup has a useful index and inspect the query plan.

## Check your understanding

1. Which query part finds Asha?
2. Why is Cara at depth 2?
3. Why might `UNION` fail to stop a cycle when `depth` is in the output?

## Further reading

- [PostgreSQL recursive WITH queries](https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-RECURSIVE)
- [PostgreSQL cycle detection](https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-CYCLE)
