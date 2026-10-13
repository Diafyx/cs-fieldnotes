# Zero-Downtime Schema Changes

A live application may have old and new code running at the same time during a deployment. A safe schema change lets both versions work until the rollout is complete. It also keeps locks, table rewrites, and backfills from holding up ordinary requests. No SQL command guarantees zero downtime by itself; the plan needs testing on a table with realistic size and traffic.

## Add a required column in stages

Suppose `accounts` has `display_name`, and the application needs `normalized_name`. Adding a `NOT NULL` column and requiring it immediately could break old code that still inserts accounts. Use these stages instead:

1. Add a nullable column. Deploy code that writes both columns for new and changed accounts. Code that reads the new column should handle old rows where it is still `NULL`.
2. Backfill old rows in small batches. Repeat while writes continue. Watch locks, replication lag, and load.
3. Confirm every row has a value. Add and validate a constraint so future writes cannot leave the column empty.
4. Deploy code that relies on the new column. Remove old reads or writes only after all running code and jobs have moved over.

This small PostgreSQL example shows the data and validation steps. A production backfill would update a limited range of IDs per transaction instead of the whole table at once.

```sql
CREATE TEMP TABLE accounts (
  account_id bigint PRIMARY KEY,
  display_name text NOT NULL
);
INSERT INTO accounts VALUES (1, 'Ada'), (2, 'Lin');

ALTER TABLE accounts ADD COLUMN normalized_name text;
UPDATE accounts
SET normalized_name = lower(display_name)
WHERE normalized_name IS NULL;

ALTER TABLE accounts
ADD CONSTRAINT normalized_name_present
CHECK (normalized_name IS NOT NULL) NOT VALID;
ALTER TABLE accounts VALIDATE CONSTRAINT normalized_name_present;

SELECT account_id, normalized_name FROM accounts ORDER BY account_id;
```

The final query returns `ada` and `lin`. `NOT VALID` skips scanning old rows when the constraint is added, but PostgreSQL checks new or changed rows from that point onward. Validation checks existing rows later. In a real deployment, old application instances must stop writing only `display_name` before adding this constraint. Otherwise their inserts will fail.

## Locks and rollback

Even a quick `ALTER TABLE` needs a lock. Set a short `lock_timeout` for a migration attempt, inspect blocking sessions, and retry at a better time if it cannot get the lock. A change that rewrites a large table can take much longer. PostgreSQL can add a column with a nonvolatile default without rewriting existing rows, but a volatile default or some type changes may still require a rewrite. Check the exact operation in the documentation.

Build large indexes with `CREATE INDEX CONCURRENTLY` when normal writes must continue. It takes longer than a regular index build, cannot run inside a transaction block, and a failed build can leave an invalid index that needs cleanup. Keep that step separate from transactional migration code.

Plan rollback before deployment. During the transition, keep the old column and old read path until you know the new code works. Dropping a column too early makes rollback much harder. Use the same expand, backfill, verify, and remove pattern for renames and type changes when old and new code must overlap.

## Check your understanding

1. Why must the application write `normalized_name` before the constraint is added?
2. What can happen if a large backfill runs in one transaction?
3. Why should an old column remain for a while after new code starts reading its replacement?

## Further reading

- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- [PostgreSQL CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)
- [PostgreSQL explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html)
