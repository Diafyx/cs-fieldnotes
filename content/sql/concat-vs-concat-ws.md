# CONCAT() vs. CONCAT_WS()

`CONCAT` joins values with nothing between them. `CONCAT_WS` joins values with a separator. In PostgreSQL, both skip `NULL` values, but neither skips an empty string.

## Join words directly

```sql
SELECT CONCAT('Post', 'gres') AS joined;
```

The result is `Postgres`. PostgreSQL converts supported non-text arguments to text, so `CONCAT('item-', 7)` returns `item-7`. Write an explicit format when the display of dates or decimal values matters.

## Put a separator between present values

```sql
SELECT CONCAT_WS(' ', first_name, middle_name, last_name) AS full_name
FROM people;
```

If `middle_name` is `NULL`, the result joins only first and last name with one space. If `middle_name` is `''`, it is still present and can create an extra space. Use `NULLIF(middle_name, '')` when an empty middle name should be skipped.

`CONCAT_WS` means "concatenate with separator." Its first argument is the separator. PostgreSQL expects a non-null separator. `CONCAT_WS('-', 'a', 'b')` returns `a-b`.

## NULL behavior differs across databases

PostgreSQL `CONCAT('a', NULL, 'b')` returns `ab`. PostgreSQL `'a' || NULL` returns `NULL`. MySQL `CONCAT` returns `NULL` when an argument is `NULL`. Do not move a query between products without checking this detail. `CONCAT_WS` skips null values in both PostgreSQL and MySQL.

## Check your understanding

1. What does PostgreSQL `CONCAT_WS('-', 'a', NULL, 'b')` return?
2. Why can an empty middle name leave two spaces in a full name?
3. How does PostgreSQL's `||` differ from PostgreSQL's `CONCAT` with `NULL`?

## Further reading

- [PostgreSQL string functions](https://www.postgresql.org/docs/current/functions-string.html)
- [MySQL string functions](https://dev.mysql.com/doc/refman/8.4/en/string-functions.html)
