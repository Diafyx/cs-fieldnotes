# Situation-14

## The question

Several workers take jobs from one PostgreSQL table. Two workers must not claim the same ready job at the same time. A worker may crash after claiming a job, so another worker must be able to try it later. Show how to claim one job and how to stop an old worker from marking a reclaimed job as done.

```sql
CREATE TEMP TABLE jobs (
  job_id integer PRIMARY KEY,
  status text NOT NULL CHECK (status IN ('ready', 'running', 'done')),
  attempts integer NOT NULL DEFAULT 0 CHECK (attempts >= 0),
  lease_until timestamptz
);

INSERT INTO jobs (job_id, status) VALUES (1, 'ready'), (2, 'ready');
```

## Claim one job

Choose a ready job, or a running job whose lease has expired. Lock it while changing its status. `SKIP LOCKED` lets another worker move past a row that is already locked by a worker claiming it.

```sql
WITH picked AS (
  SELECT job_id
  FROM jobs
  WHERE status = 'ready'
     OR (status = 'running' AND lease_until < CURRENT_TIMESTAMP)
  ORDER BY job_id
  FOR UPDATE SKIP LOCKED
  LIMIT 1
)
UPDATE jobs AS j
SET status = 'running',
    attempts = j.attempts + 1,
    lease_until = CURRENT_TIMESTAMP + INTERVAL '5 minutes'
FROM picked AS p
WHERE j.job_id = p.job_id
RETURNING j.job_id, j.attempts;
```

For the sample data, the first claim returns `(1, 1)`. After it commits, a second claim would return `(2, 1)`. If no eligible job is available, the statement returns no row. Keep the claim transaction short; do the job after committing the claim. A row lock by itself cannot protect a job during a long task, because the lock ends when the transaction commits.

## Finish with the claim number

The `attempts` value identifies the current claim for this job. Worker 1 can finish its first attempt with:

```sql
UPDATE jobs
SET status = 'done', lease_until = NULL
WHERE job_id = 1 AND status = 'running' AND attempts = 1
RETURNING job_id;
```

With no other claim, this returns `1`. If the lease expired and another worker claimed job 1, its attempt number would be 2. The old worker's update would return no row, so it could not mark the new claim as done. A long-running worker must renew its lease before expiry with the same attempt check.

This queue gives work another chance after a crash. It cannot promise that the work happens only once. A worker may perform an external action and crash before marking the job done. The next worker may perform the action again. Make the action idempotent, or give the receiving system a unique operation key. `SKIP LOCKED` can process jobs out of strict ID order and is meant for queue-like work, not for an ordinary report that needs a consistent view.

## Check your understanding

1. What happens if every eligible job is locked by another worker?
2. Why does the completion update check `attempts`?
3. How could a job's external effect happen twice even when only one worker claims it at a time?

## Further reading

- [PostgreSQL SELECT locking clauses](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE)
- [PostgreSQL UPDATE](https://www.postgresql.org/docs/current/sql-update.html)
