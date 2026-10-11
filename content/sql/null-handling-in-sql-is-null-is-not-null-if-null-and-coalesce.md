# NULL Handling in SQL: IS NULL, IS NOT NULL, IF NULL(), and COALESCE()

`NULL` means a value is missing or unknown. It is not zero, false, or an empty string. A useful query first asks whether the value is missing, then decides whether a fallback is valid for the task.

## Test for missing values

```sql
SELECT order_id
FROM orders
WHERE shipped_at IS NULL;
```

Use `IS NOT NULL` to find present values. `shipped_at = NULL` cannot find missing values because an ordinary comparison with `NULL` is unknown. `WHERE` keeps only conditions that are true.

## Choose a display value

```sql
SELECT customer_id,
       COALESCE(nickname, full_name, '(name missing)') AS label
FROM customers;
```

This uses the first non-null value. It changes only the query result. It does not fill the stored column. `COALESCE` may be useful for display, but a made-up value can be misleading in an average or a financial total. Use a fallback only when the report's rule says it is right.

## Empty, zero, and NULL have different meanings

`COALESCE('', 'unknown')` returns the empty string. `COALESCE(0, 99)` returns zero. If old data uses `''` to mean a missing name, `COALESCE(NULLIF(name, ''), '(missing)')` can make that rule explicit in a query. A long-term fix is to make the storage rule consistent.

## Database names differ

In MySQL and SQLite, `IFNULL(a, b)` chooses `b` when `a` is `NULL`. PostgreSQL uses `COALESCE(a, b)`. `COALESCE` is standard SQL and can check more than two values. Its arguments need compatible types.

If you want a comparison that treats two missing values as equal, PostgreSQL offers `IS NOT DISTINCT FROM`. It answers a different question from `COALESCE`: it compares values rather than replacing one.

## Check your understanding

1. Why does `WHERE shipped_at = NULL` find no rows?
2. Does `COALESCE(0, 99)` return 99?
3. When could replacing a missing amount with zero make a report misleading?

## Further reading

- [PostgreSQL comparison predicates](https://www.postgresql.org/docs/current/functions-comparison.html)
- [PostgreSQL COALESCE and NULLIF](https://www.postgresql.org/docs/current/functions-conditional.html)
- [MySQL IFNULL reference](https://dev.mysql.com/doc/refman/8.4/en/flow-control-functions.html)
