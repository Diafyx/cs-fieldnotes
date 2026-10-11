# Employee Work Time Summary

An employee can enter and leave work more than once in a day. To find total time per employee and day, calculate each session's length and add the lengths inside each group.

## The question

`in_min` and `out_min` are minutes after the start of `event_day`. Each session starts and ends on that day, with `out_min > in_min`. Sessions for one employee do not overlap. Return one row per employee and day with `total_minutes`.

```sql
CREATE TEMP TABLE work_sessions (
  emp_id integer NOT NULL,
  event_day date NOT NULL,
  in_min integer NOT NULL,
  out_min integer NOT NULL,
  PRIMARY KEY (emp_id, event_day, in_min),
  CHECK (out_min > in_min)
);

INSERT INTO work_sessions (emp_id, event_day, in_min, out_min) VALUES
  (1, '2026-01-01', 10, 25),
  (1, '2026-01-01', 30, 50),
  (1, '2026-01-02', 100, 130),
  (2, '2026-01-01', 5, 15);
```

## A solution

```sql
SELECT event_day, emp_id,
       SUM(out_min - in_min) AS total_minutes
FROM work_sessions
GROUP BY event_day, emp_id
ORDER BY event_day, emp_id;
```

The output is 35 minutes for employee 1 on January 1, 10 minutes for employee 2 on January 1, and 30 minutes for employee 1 on January 2. The two sessions for employee 1 on January 1 contribute 15 and 20 minutes.

Grouping only by employee would mix different days. Grouping only by day would mix employees. If sessions overlap, this sum double-counts the overlapping minutes. If a session crosses midnight, this table design cannot split it correctly. Those cases need different source data and rules before calculating a daily total.

## Check your understanding

1. Why are both `event_day` and `emp_id` grouping keys?
2. What goes wrong if an employee has overlapping sessions?
3. How many minutes does the first January 1 session contribute?

## Further reading

- [LeetCode Find Total Time Spent by Each Employee](https://leetcode.com/problems/find-total-time-spent-by-each-employee/)
- [PostgreSQL GROUP BY clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-GROUPBY)
