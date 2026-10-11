# Find Missing Subtasks for Each Task

Each task expects subtask numbers from 1 through its `subtasks_count`. Return the task and subtask numbers that do not appear in the executed list. A task with zero expected subtasks has nothing missing.

## Sample data

```sql
CREATE TEMP TABLE tasks (
  task_id integer PRIMARY KEY,
  subtasks_count integer NOT NULL CHECK (subtasks_count >= 0)
);
CREATE TEMP TABLE executed (
  task_id integer NOT NULL,
  subtask_id integer NOT NULL,
  PRIMARY KEY (task_id, subtask_id)
);
INSERT INTO tasks VALUES (1, 3), (2, 2), (3, 1), (4, 0);
INSERT INTO executed VALUES (1, 1), (1, 3), (2, 2), (3, 1);
```

## Solution

```sql
WITH RECURSIVE needed(task_id, subtask_id, last_id) AS (
  SELECT task_id, 1, subtasks_count
  FROM tasks
  WHERE subtasks_count >= 1
  UNION ALL
  SELECT task_id, subtask_id + 1, last_id
  FROM needed
  WHERE subtask_id < last_id
)
SELECT n.task_id, n.subtask_id
FROM needed AS n
WHERE NOT EXISTS (
  SELECT 1
  FROM executed AS e
  WHERE e.task_id = n.task_id AND e.subtask_id = n.subtask_id
)
ORDER BY n.task_id, n.subtask_id;
```

The result is `(1, 2)` and `(2, 1)`. The anchor creates subtask 1 for every task that expects at least one. The recursive step adds numbers until it reaches that task's count. `NOT EXISTS` removes those already executed. Task 3 is complete. Task 4 creates no expected rows.

PostgreSQL also has `generate_series`, which is shorter for this job:

```sql
SELECT t.task_id, g.subtask_id
FROM tasks AS t
CROSS JOIN LATERAL generate_series(1, t.subtasks_count) AS g(subtask_id)
WHERE NOT EXISTS (
  SELECT 1
  FROM executed AS e
  WHERE e.task_id = t.task_id AND e.subtask_id = g.subtask_id
)
ORDER BY t.task_id, g.subtask_id;
```

The second query is PostgreSQL-specific. Both queries describe the same missing pairs. A primary key on `executed(task_id, subtask_id)` prevents duplicate completion records. An executed subtask outside the expected range is a separate data error; neither query reports it as a missing expected subtask.

## Check your understanding

1. Why is task 4 absent?
2. What stops the recursive query from generating subtask 4 for task 1?
3. Why must the `NOT EXISTS` condition compare both IDs?

## Further reading

- [PostgreSQL recursive WITH queries](https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-RECURSIVE)
- [PostgreSQL generate_series](https://www.postgresql.org/docs/current/functions-srf.html)
