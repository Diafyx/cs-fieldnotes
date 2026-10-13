# JSON Updates

An `UPDATE` can replace a whole JSON document or change one part of it. PostgreSQL's `jsonb_set` writes at a path. Other operators merge top-level objects, remove keys, and append to arrays. Each update still writes a new value for the column.

## Change one nested field

```sql
CREATE TEMP TABLE user_settings (
  user_id integer PRIMARY KEY,
  settings jsonb NOT NULL
);

INSERT INTO user_settings (user_id, settings)
VALUES (1, '{"theme":"light","alerts":{"email":true},"tags":["new"]}'::jsonb);

UPDATE user_settings
SET settings = jsonb_set(settings, '{alerts,email}', 'false'::jsonb)
WHERE user_id = 1;

SELECT settings
FROM user_settings
WHERE user_id = 1;
```

The result still has theme `light` and tag `new`, but `alerts.email` is now JSON `false`. The last argument of `jsonb_set` must be JSON. For a string value, use `to_jsonb('dark'::text)` or a quoted JSON string such as `'"dark"'::jsonb`.

## Add, append, and remove

Run these statements after the setup above:

```sql
UPDATE user_settings
SET settings = jsonb_set(settings, '{theme}', to_jsonb('dark'::text))
WHERE user_id = 1;

UPDATE user_settings
SET settings = jsonb_set(
  settings, '{tags}',
  COALESCE(settings -> 'tags', '[]'::jsonb) || jsonb_build_array('saved')
)
WHERE user_id = 1;

UPDATE user_settings
SET settings = settings #- '{alerts,email}'
WHERE user_id = 1;

SELECT settings
FROM user_settings
WHERE user_id = 1;
```

The final document has theme `dark`, tags `new` and `saved`, and an empty `alerts` object. `#-` removes a value at a path. `settings - 'theme'` would remove a top-level key. The `||` operator appends array values or merges top-level objects; it does not merge nested objects. If you run the append a second time, `saved` appears twice. Add a condition or rebuild the array when duplicates are not allowed.

`jsonb_set` can create a missing final key by default, but every earlier path step must already exist. For example, `jsonb_set('{}'::jsonb, '{alerts,email}', 'true'::jsonb)` leaves `{}` unchanged because `alerts` does not exist. If `tags` holds a scalar instead of an array, the append expression may not give the shape you expect. Check the type before editing documents from mixed sources.

## Check your understanding

1. What remains under `alerts` after the remove step?
2. Why can the append step add `saved` twice?
3. Why is `settings || '{"alerts":{"sms":true}}'::jsonb` risky if `alerts.email` must stay?

## Further reading

- [PostgreSQL JSON update functions and operators](https://www.postgresql.org/docs/current/functions-json.html)
- [PostgreSQL jsonb subscripting](https://www.postgresql.org/docs/current/datatype-json.html)
