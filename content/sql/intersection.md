# Intersection

An intersection keeps rows that appear in both query results. In PostgreSQL, the operator is `INTERSECT`. Like `UNION`, it removes duplicate complete rows unless you ask for `ALL`.

```sql
WITH team_a(person_id) AS (
  VALUES (1), (2), (2), (3)
), team_b(person_id) AS (
  VALUES (2), (2), (4)
)
SELECT person_id FROM team_a
INTERSECT
SELECT person_id FROM team_b
ORDER BY person_id;
```

The result is one row containing `2`. Person 2 appears in both lists. `INTERSECT ALL` would return two rows containing `2`, because each input has two copies. With `ALL`, a row appears as many times as the smaller count in the two inputs.

## Compare the whole row

If each query selects `(person_id, status)`, both values must match for a row to be in the intersection. To find shared IDs even when statuses differ, select only `person_id`. Rows with `NULL` in matching positions can be treated as the same row by this set operation, unlike a normal `NULL = NULL` comparison.

`INTERSECT` can answer a shared-membership question without a join. A join is better when you need columns from both sources or need to express a match between different column names. A join can also multiply rows when either side has repeated keys; plain `INTERSECT` gives distinct matching result rows.

## Mixing set operations

In PostgreSQL, `INTERSECT` is evaluated before an unparenthesized `UNION` or `EXCEPT`. Use parentheses when combining them so the intended grouping is visible. A final `ORDER BY` sorts the full result. As with other set operations, the input queries must return the same number of compatible columns.

## Check your understanding

1. Why does the example return only person 2?
2. How many rows would `INTERSECT ALL` return for person 2?
3. What should each side select if only matching IDs matter and statuses can differ?

## Further reading

- [PostgreSQL combining queries](https://www.postgresql.org/docs/current/queries-union.html)
- [PostgreSQL INTERSECT clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-INTERSECT)
