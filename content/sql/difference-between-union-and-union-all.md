# Difference Between UNION and UNION ALL

Both operations combine rows from compatible queries. `UNION` removes repeated complete rows. `UNION ALL` keeps them. That difference can change counts and totals.

```sql
WITH a(value) AS (VALUES (1), (1), (2)),
     b(value) AS (VALUES (2), (3))
SELECT value FROM a
UNION
SELECT value FROM b
ORDER BY value;
```

This returns `1, 2, 3`. Change `UNION` to `UNION ALL` and it returns `1, 1, 2, 2, 3`. Both queries have the same five input rows. Only the first removes repeats.

## Decide what a duplicate means

If two sources each report the same country name and the goal is a country list, `UNION` fits. If each row is a purchase, two identical purchases may still be two real purchases. `UNION ALL` keeps both. A `UNION` over `(user_id, email)` removes rows only when *both* values match. It does not promise one row per user ID.

When deduplication is needed by one key, decide which record wins before writing SQL. Perhaps the most recent update wins, or perhaps the active record wins over an archive record. `UNION` alone cannot apply that rule to rows with different details.

## Cost and order

`UNION` must identify duplicates. `UNION ALL` does not, so it usually avoids that extra work. The best choice still comes from the required result. Neither operation promises row order. Add an `ORDER BY` after the combined query when you need one.

Both sides need the same number of compatible columns. PostgreSQL takes the combined output names from the first query. A `NULL` in a result row can still be part of a duplicate row for `UNION`; duplicate removal does not use `= NULL` as a normal filter would.

## Check your understanding

1. How many rows does each version of the example return?
2. Why might `UNION` undercount purchases?
3. Can `UNION` choose the newest profile when two rows share an ID but have different emails?

## Further reading

- [PostgreSQL combining queries](https://www.postgresql.org/docs/current/queries-union.html)
- [PostgreSQL SELECT processing](https://www.postgresql.org/docs/current/sql-select.html)
