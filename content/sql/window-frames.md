# Window Frames

A partition is the full group of rows available to a window function. A frame is the part of that partition used for a calculation at the current row. Running totals and value functions can change when the frame changes.

## Rows and peers give different running totals

```sql
WITH sales(sale_id, sale_day, amount) AS (
  VALUES (1, '2026-01-01', 10),
         (2, '2026-01-01', 20),
         (3, '2026-01-02', 5)
)
SELECT sale_id, sale_day, amount,
       SUM(amount) OVER (ORDER BY sale_day) AS default_total,
       SUM(amount) OVER (
         ORDER BY sale_day, sale_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS row_total
FROM sales
ORDER BY sale_id;
```

The results for sales 1, 2, and 3 are `(30, 10)`, `(30, 30)`, and `(35, 35)` for the two totals. PostgreSQL's default ordered frame is `RANGE` from the partition start through the current row's last peer. Sales 1 and 2 share the same day, so the default frame includes both at once. The explicit `ROWS` frame follows individual rows. The added `sale_id` makes its order stable.

## Choose a frame on purpose

`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` means up to three rows, including the current one. `RANGE` uses the ordered value and includes its peers; with an offset it can mean a numeric or date/time distance. `GROUPS` counts peer groups. `UNBOUNDED PRECEDING` starts at the partition's first row, and `UNBOUNDED FOLLOWING` reaches its last row. PostgreSQL also supports `EXCLUDE` choices to remove the current row or peers from an otherwise chosen frame.

At a partition edge, a frame may hold fewer rows than requested. `ROWS 6 PRECEDING` is not automatically six calendar days if dates are missing. Ranking functions use the partition order, while aggregate windows and `first_value`, `last_value`, and `nth_value` can depend on the frame. A common mistake is using `last_value` with the default frame and getting the current row instead of the partition's last row.

## Check your understanding

1. Why does sale 1's default total already include sale 2?
2. When can a three-row frame contain fewer than three rows?
3. What is the difference between `ROWS 2 PRECEDING` and a two-day date range?

## Further reading

- [PostgreSQL window frame syntax](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)
- [PostgreSQL window function behavior](https://www.postgresql.org/docs/current/functions-window.html)
