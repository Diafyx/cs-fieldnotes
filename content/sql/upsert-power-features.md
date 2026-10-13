# Upsert Power Features

An upsert inserts a row when its unique key is new and updates the existing row when that key already exists. PostgreSQL uses `INSERT ... ON CONFLICT`. With JSONB, you must also decide whether an incoming document replaces the old one or merges with it.

## Keep the newer version of a profile

```sql
CREATE TEMP TABLE profiles (
  user_id integer PRIMARY KEY,
  version integer NOT NULL,
  profile jsonb NOT NULL
);

INSERT INTO profiles (user_id, version, profile)
VALUES (1, 1, '{"name":"Ada","theme":"light"}'::jsonb);

INSERT INTO profiles (user_id, version, profile)
VALUES (1, 2, '{"theme":"dark"}'::jsonb)
ON CONFLICT (user_id) DO UPDATE
SET version = EXCLUDED.version,
    profile = profiles.profile || EXCLUDED.profile
WHERE EXCLUDED.version > profiles.version
RETURNING user_id, version, profile;
```

The `user_id` primary key is the conflict target. `EXCLUDED` is the row that was proposed for insertion. The returned profile has `name` set to `Ada` and `theme` set to `dark`, with version `2`. For two JSON objects, `||` keeps old keys that the incoming object does not have and takes the incoming value for matching top-level keys.

The `WHERE` clause stops an older or equal version from overwriting a newer row. If it stops an update, `RETURNING` returns no row for that input. `ON CONFLICT DO NOTHING` is useful when a duplicate should simply be skipped. A conflict target must match a suitable unique constraint or unique index; an ordinary index is not enough.

This merge is shallow. If the profile contains `{"settings":{"email":true,"theme":"light"}}` and the incoming document contains `{"settings":{"theme":"dark"}}`, the old `email` key is lost. For nested updates, use `jsonb_set` with a merge of the nested objects, or store fields that change independently in separate columns. A JSON `null` in an incoming top-level key overwrites the old value; it does not mean "leave this key alone."

PostgreSQL makes the insert or update choice atomic for a conflict on the chosen unique key. It may still wait for another transaction, and unrelated constraint failures can still stop the statement. Do not send two proposed rows with the same conflict key in one `ON CONFLICT DO UPDATE` statement; PostgreSQL will not update the same target row twice in that statement. Decide how to combine duplicates before loading a batch.

## Check your understanding

1. Why does the first upsert keep Ada's name?
2. What happens when the incoming version is `1` after version `2` is stored?
3. Why can a top-level JSONB merge remove a nested key?

## Further reading

- [PostgreSQL INSERT and ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html)
- [PostgreSQL JSONB merge operator](https://www.postgresql.org/docs/current/functions-json.html)
