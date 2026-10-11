# Combine Active and Archived Users

This exercise asks for one list of user IDs found in either the active table or the archive. A user can appear in both places, but their ID should appear once in the result.

## The question

Return every distinct `user_id` from the two tables, sorted by ID. The names are included to show why selecting the right columns matters.

```sql
CREATE TEMP TABLE active_users (
  user_id integer PRIMARY KEY,
  name text NOT NULL
);

CREATE TEMP TABLE archived_users (
  user_id integer PRIMARY KEY,
  name text NOT NULL
);

INSERT INTO active_users (user_id, name) VALUES
  (1, 'Ana'),
  (2, 'Ben New');

INSERT INTO archived_users (user_id, name) VALUES
  (2, 'Ben Old'),
  (3, 'Cara');
```

## A solution

```sql
SELECT user_id FROM active_users
UNION
SELECT user_id FROM archived_users
ORDER BY user_id;
```

The answer is `1, 2, 3`. ID 2 appears in both tables, and `UNION` keeps one copy because the selected row contains only that ID.

If we selected both `user_id` and `name`, the two ID 2 rows would stay. `(2, 'Ben New')` and `(2, 'Ben Old')` are different complete rows. To return one full profile per user, first decide whether active data wins or whether the newest record wins. `UNION` alone cannot choose between different records that share an ID.

If the task needed a row for every occurrence in both tables, `UNION ALL` would be the right operation. Here the word *distinct* makes `UNION` a direct fit.

## Check your understanding

1. Why does ID 2 appear once in the answer?
2. What changes if the query selects `user_id, name`?
3. What extra rule is needed to return one complete profile for ID 2?

## Further reading

- [PostgreSQL combining queries](https://www.postgresql.org/docs/current/queries-union.html)
