# LENGTH() vs CHAR_LENGTH()

In PostgreSQL, `LENGTH(text)` and `CHAR_LENGTH(text)` both count characters. `OCTET_LENGTH(text)` counts bytes. These are different numbers when text contains characters that use more than one byte in the database encoding.

## Count characters and bytes

With a UTF-8 PostgreSQL database:

```sql
SELECT LENGTH('café') AS length_result,
       CHAR_LENGTH('café') AS character_count,
       OCTET_LENGTH('café') AS byte_count;
```

The results are 4, 4, and 5. The final letter uses two bytes in UTF-8. With an ASCII word such as `cafe`, all three results are 4.

Do not assume a character count always equals what a person sees as one symbol. Some visible symbols use more than one Unicode character. If a product has a user-facing text limit, check its exact rule before using a database function to enforce it.

## Different products use LENGTH differently

MySQL `LENGTH` counts bytes, while MySQL `CHAR_LENGTH` counts characters. A PostgreSQL query that uses `LENGTH` for a character limit may change meaning if it is moved to MySQL. PostgreSQL `OCTET_LENGTH` is the direct byte-count form.

For a `NULL` input, these functions return `NULL`. An empty string has length zero, which is different from a missing string. A `WHERE CHAR_LENGTH(content) > 15` filter does not include missing content.

## Check your understanding

1. Why is the UTF-8 byte count of `café` greater than its character count?
2. Which PostgreSQL function checks bytes?
3. What does `CHAR_LENGTH('')` return?

## Further reading

- [PostgreSQL string functions](https://www.postgresql.org/docs/current/functions-string.html)
- [MySQL string functions](https://dev.mysql.com/doc/refman/8.4/en/string-functions.html)
