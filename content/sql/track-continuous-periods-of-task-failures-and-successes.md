# Track Continuous Periods of Task Failures and Successes

Group each task's daily results into runs. A run continues only when the next recorded day is the next calendar day and the status stays the same. A missing day starts a new run even if the status is unchanged.

## Sample data

```sql
CREATE TEMP TABLE task_log (
  task_id integer NOT NULL,
  log_day date NOT NULL,
  status text NOT NULL,
  PRIMARY KEY (task_id, log_day)
);
INSERT INTO task_log VALUES
  (1, '2026-01-01', 'failed'), (1, '2026-01-02', 'failed'),
  (1, '2026-01-03', 'succeeded'), (1, '2026-01-04', 'succeeded'),
  (1, '2026-01-06', 'succeeded'), (1, '2026-01-07', 'failed'),
  (2, '2026-01-02', 'succeeded');
```

## PostgreSQL solution

```sql
WITH ordered AS (
  SELECT task_id, log_day, status,
         LAG(log_day) OVER (PARTITION BY task_id ORDER BY log_day) AS previous_day,
         LAG(status) OVER (PARTITION BY task_id ORDER BY log_day) AS previous_status
  FROM task_log
), starts AS (
  SELECT task_id, log_day, status,
         CASE WHEN previous_status = status AND log_day = previous_day + 1
              THEN 0 ELSE 1 END AS new_run
  FROM ordered
), numbered AS (
  SELECT task_id, log_day, status,
         SUM(new_run) OVER (
           PARTITION BY task_id ORDER BY log_day
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
         ) AS run_number
  FROM starts
)
SELECT task_id, status, MIN(log_day) AS start_day, MAX(log_day) AS end_day
FROM numbered
GROUP BY task_id, status, run_number
ORDER BY task_id, start_day;
```

Task 1 has four runs: failed on January 1 to 2, succeeded on January 3 to 4, succeeded on January 6 alone, and failed on January 7 alone. Task 2 has one succeeded run on January 2. The `LAG` calls inspect the prior row for that task. `new_run` marks status changes and date gaps. Its running sum gives every run a number.

The primary key makes one status per task per day. If a task can have several events on a day, first decide how to turn them into one daily status. Without that rule, two same-day rows would create confusing runs. Keep the date comparison: looking only at status would incorrectly join January 4 and 6.

## Check your understanding

1. Why does January 6 start a new succeeded run?
2. What makes the first row of every task start a run?
3. Why is daily aggregation needed if a task can emit several status events per day?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL date arithmetic](https://www.postgresql.org/docs/current/functions-datetime.html)
