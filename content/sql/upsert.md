# UPSERT

An upsert adds a row when its key is new and changes an existing row when that key is already present. PostgreSQL writes this as `INSERT ... ON CONFLICT DO UPDATE`. A primary key or unique index tells PostgreSQL what counts as a conflict.

## Add or replace one setting

```sql
CREATE TABLE app_settings (
  setting_key text PRIMARY KEY,
  setting_value text NOT NULL
);

INSERT INTO app_settings (setting_key, setting_value)
VALUES ('theme', 'light')
ON CONFLICT (setting_key)
DO UPDATE SET setting_value = EXCLUDED.setting_value
RETURNING setting_key, setting_value;
```

The first run inserts `('theme', 'light')`. If the row already exists, the command changes its value to `light`. `EXCLUDED.setting_value` is the value the insert tried to use. The existing row can be read using the target table name, as in `app_settings.setting_value`. `RETURNING` shows a row when the insert or update happens.

`ON CONFLICT (setting_key) DO NOTHING` would leave an existing setting alone. With `DO NOTHING`, `RETURNING` returns no row for the skipped insert. Choose between leaving old data and replacing it before writing the query.

## Keep updates within a stated rule

```sql
INSERT INTO app_settings (setting_key, setting_value)
VALUES ('theme', 'dark')
ON CONFLICT (setting_key)
DO UPDATE SET setting_value = EXCLUDED.setting_value
WHERE app_settings.setting_value IS DISTINCT FROM EXCLUDED.setting_value
RETURNING setting_key, setting_value;
```

This updates only when the value differs. If `theme` is already `dark`, no row is returned. It avoids an unnecessary update. The `WHERE` here controls the conflict update; it does not filter the proposed insert.

PostgreSQL makes the insert-or-update choice atomically under concurrent writes. A separate `SELECT`, followed by `INSERT` or `UPDATE` in application code, can race with another session. An upsert still needs a suitable unique rule. If a batch contains the same conflict key twice, PostgreSQL can reject the statement because one target row cannot be updated twice by that command.

## Check your understanding

1. What must exist on `setting_key` for the conflict target to work?
2. What is the difference between `DO NOTHING` and `DO UPDATE`?
3. Why can checking for a row in application code before inserting it be unsafe under concurrent writes?

## Further reading

- [PostgreSQL INSERT and ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT)
- [PostgreSQL comparison predicates](https://www.postgresql.org/docs/current/functions-comparison.html)
