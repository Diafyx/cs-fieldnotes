# Find Continuous Ranges in Logs

Combine consecutive integer log IDs into ranges. Each range starts after a gap and ends before the next gap. The IDs are unique in this example.

## Sample data

```sql
CREATE TEMP TABLE logs (log_id integer PRIMARY KEY);
INSERT INTO logs VALUES (1), (2), (3), (5), (7), (8);
```

## Solution

```sql
WITH numbered AS (
  SELECT log_id,
         ROW_NUMBER() OVER (ORDER BY log_id) AS position
  FROM logs
)
SELECT MIN(log_id) AS start_id, MAX(log_id) AS end_id
FROM numbered
GROUP BY log_id - position
ORDER BY start_id;
```

The ranges are `(1, 3)`, `(5, 5)`, and `(7, 8)`. Within a consecutive run, both `log_id` and `position` rise by one, so their difference stays the same. After a missing ID, `log_id` jumps but `position` rises by one, giving a new group value.

This pattern assumes integers with a step of one and no duplicate IDs. A primary key enforces uniqueness here. If IDs can repeat, remove duplicates before numbering. If the data is dates rather than IDs, use date arithmetic and decide whether a missing calendar day should split a run. A missing log ID does not always mean a missing event in a real system, since IDs may be skipped by rollbacks or other processes.

## Check your understanding

1. Why do IDs 7 and 8 share a group value?
2. Why is ID 5 a range by itself?
3. What input rule makes `log_id - position` safe for this problem?

## Further reading

- [PostgreSQL ROW_NUMBER](https://www.postgresql.org/docs/current/functions-window.html)
