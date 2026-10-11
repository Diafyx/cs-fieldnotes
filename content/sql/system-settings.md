# System Settings

This exercise stores one value per setting key. A new key should be added. An existing key should receive the new value. A primary key and an upsert make both cases part of one SQL statement.

## The question

The table starts with two settings. Save `theme = dark` and `email_alerts = on`. Keep `page_size` unchanged. Return the final settings sorted by key.

```sql
CREATE TEMP TABLE system_settings (
  setting_key text PRIMARY KEY,
  setting_value text NOT NULL
);

INSERT INTO system_settings (setting_key, setting_value) VALUES
  ('theme', 'light'),
  ('page_size', '20');
```

## A solution

```sql
INSERT INTO system_settings (setting_key, setting_value) VALUES
  ('theme', 'dark'),
  ('email_alerts', 'on')
ON CONFLICT (setting_key)
DO UPDATE SET setting_value = EXCLUDED.setting_value;
```

`theme` already exists, so its value becomes `dark`. `email_alerts` is new, so it is inserted. The statement does not mention `page_size`, so its value stays `20`. `EXCLUDED.setting_value` means the value proposed by the insert.

Check the table:

```sql
SELECT setting_key, setting_value
FROM system_settings
ORDER BY setting_key;
```

The rows are `('email_alerts', 'on')`, `('page_size', '20')`, and `('theme', 'dark')`. Running the same upsert again leaves these values the same, though PostgreSQL may still perform an update on the existing `theme` row. A conditional `DO UPDATE ... WHERE` can avoid that extra work when the value has not changed.

This table accepts any text as a key or value. A real settings system may need checks for allowed keys, value types, and who may change each setting. Those rules are separate from the upsert itself.

## Check your understanding

1. What makes `theme` a conflict but not `email_alerts`?
2. Why is `page_size` still present after the statement?
3. How would `DO NOTHING` change the result for `theme`?

## Further reading

- [PostgreSQL INSERT and ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT)
- [PostgreSQL primary keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS)
