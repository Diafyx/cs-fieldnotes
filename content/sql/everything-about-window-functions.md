# Everything about Window Functions

A window function calculates a value using rows related to the current row. Unlike `GROUP BY`, it keeps the input rows in the result. Common uses are ranking, running totals, comparing with a previous row, and finding a total for each group.

## Keep detail and add a group result

```sql
WITH sales(employee_id, department_id, amount) AS (
  VALUES (1, 10, 20), (2, 10, 30), (3, 20, 15)
)
SELECT employee_id, department_id, amount,
       SUM(amount) OVER (PARTITION BY department_id) AS department_total,
       ROW_NUMBER() OVER (
         PARTITION BY department_id ORDER BY amount DESC, employee_id
       ) AS place
FROM sales
ORDER BY employee_id;
```

The rows are `(1, 10, 20, 50, 2)`, `(2, 10, 30, 50, 1)`, and `(3, 20, 15, 15, 1)`. Department 10 keeps both sales rows and shows total 50 on each. `ROW_NUMBER` puts the larger sale first within that department.

## The three parts of a window

`OVER (...)` marks a window call. `PARTITION BY` splits rows into groups for that calculation; without it, the whole selected result is one partition. `ORDER BY` arranges rows inside a partition for functions that need sequence. A frame can narrow an ordered partition to rows near the current row. For example, a running sum uses a frame from the partition start through the current row.

The final `ORDER BY` controls display order. It is separate from the order inside `OVER`. PostgreSQL permits window calls in the `SELECT` list and final `ORDER BY`, not directly in `WHERE`. To keep only rank 1, calculate the rank in a CTE or subquery and filter its output.

Window functions are calculated after row filtering and grouping in the same query level. If a `WHERE` clause removes a sale, that sale is absent from the window calculation. If you need both a grouped result and the original detail, decide which rows should reach the window before writing the query.

## Check your understanding

1. Why does department 10's total appear twice?
2. Does the `ORDER BY` inside `OVER` sort the final output?
3. Why would you need a CTE to return only the highest sale per department?

## Further reading

- [PostgreSQL window tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)
- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
