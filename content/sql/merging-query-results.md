# Merging Query Results

Sometimes the rows you need come from two queries. Set operations combine their results into one result. `UNION` and `UNION ALL` collect rows from either query. `INTERSECT` keeps rows found in both. `EXCEPT` keeps rows from the first query that are absent from the second.

## Match the columns first

Both queries must return the same number of columns. Each column must have a compatible type with the column in the same position on the other side. SQL matches by position, not by column name.

```sql
SELECT user_id, email FROM active_users
UNION ALL
SELECT user_id, email FROM archived_users;
```

This can combine two user lists. If the second query selected `email, user_id`, it would put values in the wrong positions and might fail because the types do not match. Name the columns in the intended order. Avoid `SELECT *` when tables may have different or changing column layouts. The final column names come from the first query.

## Pick the right operation

Use `UNION ALL` when every input row matters, such as event or sales records. Use `UNION` when repeated *whole result rows* should appear once. A repeated user ID with a different email is not a duplicate of the full `(user_id, email)` row. Use `INTERSECT` to find complete rows shared by both results. Use `EXCEPT` to find complete rows on the left but not the right.

These operations stack rows. A join instead connects columns from related rows. For example, use a join to put a user's department beside their name; use a union to make one list from current and archived users.

## Sort the combined result

Neither the first query's order nor the second query's order guarantees the final order. Put `ORDER BY` after the set operation:

```sql
SELECT user_id FROM active_users
UNION
SELECT user_id FROM archived_users
ORDER BY user_id;
```

Parentheses make mixed set operations easier to read and control. In PostgreSQL, `INTERSECT` binds more tightly than `UNION` or `EXCEPT`. A `LIMIT` at the end applies to the combined result unless an input query is put in parentheses with its own limit.

## Check your understanding

1. Why can selecting the same two columns in a different order break a union?
2. Which operation keeps two identical sales records?
3. Why does a user ID repeated with two different emails survive a `UNION` of both columns?

## Further reading

- [PostgreSQL combining queries](https://www.postgresql.org/docs/current/queries-union.html)
- [PostgreSQL SELECT](https://www.postgresql.org/docs/current/sql-select.html)
