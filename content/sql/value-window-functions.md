# Value Window Functions

`FIRST_VALUE`, `LAST_VALUE`, and `NTH_VALUE` pick a value from a window frame. The order says which row is first or last. The frame says how far the function may look.

## Use the full group

```sql
WITH readings(group_name, reading_id, value) AS (
  VALUES ('A', 1, 10), ('A', 2, 20), ('A', 3, 30), ('B', 4, 7)
)
SELECT group_name, reading_id, value,
       FIRST_VALUE(value) OVER full_group AS first_value,
       LAST_VALUE(value) OVER full_group AS last_value,
       NTH_VALUE(value, 2) OVER full_group AS second_value
FROM readings
WINDOW full_group AS (
  PARTITION BY group_name ORDER BY reading_id
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
ORDER BY group_name, reading_id;
```

Every A row shows first value `10`, last value `30`, and second value `20`. B has one row, so it shows first and last value `7`, and second value `NULL`. `NTH_VALUE` counts from 1, not 0.

The full frame is important. With the default ordered frame, `LAST_VALUE(value)` often gives the current row's value because the frame usually ends at the current row or its peers. A full-partition frame makes it return the actual last value in that group. Always give the ordering a tie breaker if several rows can share the same sort key.

These functions read nulls as values in PostgreSQL. The SQL standard describes an `IGNORE NULLS` option, but PostgreSQL currently uses `RESPECT NULLS` behavior only. To find the last non-null value, use a query designed for that rule rather than assuming `LAST_VALUE` will skip nulls.

## Check your understanding

1. Why is B's second value null?
2. What can `LAST_VALUE` return with its default frame?
3. Why does the example order by `reading_id`?

## Further reading

- [PostgreSQL value window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL WINDOW clause](https://www.postgresql.org/docs/current/sql-select.html)
