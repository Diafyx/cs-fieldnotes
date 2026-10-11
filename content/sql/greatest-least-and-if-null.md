# GREATEST(), LEAST(), and IF NULL()

`GREATEST` and `LEAST` compare values within one row. `IFNULL` is a name used by MySQL and SQLite for choosing a fallback when a value is missing. In PostgreSQL, use `COALESCE` for that fallback.

## Compare values in one row

```sql
SELECT item_id,
       GREATEST(store_price, online_price) AS higher_price,
       LEAST(store_price, online_price) AS lower_price
FROM products;
```

If the prices are 20 and 25, the result is 25 and 20. This is not the same as `MAX(store_price)`, which compares one column across rows.

PostgreSQL ignores `NULL` arguments in `GREATEST` and `LEAST`. `GREATEST(20, NULL)` returns 20. It returns `NULL` when all arguments are `NULL`. Some other databases return `NULL` when any argument is `NULL`, so check the product before moving this query.

## Choose a fallback

```sql
SELECT product_id,
       COALESCE(public_name, internal_name, '(unnamed)') AS name_to_show
FROM products;
```

`COALESCE` returns the first non-null value. An empty string is still present, so it wins over later values. If empty strings also mean missing in your data, use a separate rule such as `NULLIF(public_name, '')` before `COALESCE`.

MySQL writes the two-value form as `IFNULL(public_name, internal_name)`. PostgreSQL does not use that function name. `COALESCE` also accepts more than two values and is standard SQL. The values must be convertible to a common result type.

## Check your understanding

1. What does PostgreSQL return for `LEAST(NULL, 9)`?
2. Why is `GREATEST(a, b)` different from `MAX(a)`?
3. Does `COALESCE('', 'fallback')` return the fallback?

## Further reading

- [PostgreSQL conditional expressions](https://www.postgresql.org/docs/current/functions-conditional.html)
- [MySQL IFNULL reference](https://dev.mysql.com/doc/refman/8.4/en/flow-control-functions.html)
