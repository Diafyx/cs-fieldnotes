# LIKE and NOT LIKE

`LIKE` matches text against a simple pattern. `%` stands for zero or more characters. `_` stands for exactly one character. `NOT LIKE` keeps text that does not match. These examples use PostgreSQL.

## Match the whole value or part of it

```sql
SELECT product_id, product_name
FROM products
WHERE product_name LIKE 'Book%';
```

This matches `Book`, `Books`, and `Bookcase` under an ordinary case-sensitive collation. It does not match `Notebook`. `LIKE` checks the whole string, so `%book%` is needed to find `book` anywhere inside it.

`_` matches one character:

```sql
WHERE code LIKE 'A_3'
```

This matches `AB3`, but not `A3` or `ABX3`. `%` may match an empty string, while `_` may not.

## Exclude a pattern

```sql
SELECT product_id
FROM products
WHERE product_name NOT LIKE 'Test%';
```

Rows with a `NULL` product name are not returned. `NULL NOT LIKE 'Test%'` is unknown, not true. Add `OR product_name IS NULL` only if missing names should count as not matching.

## Match a literal percent or underscore

Choose an escape character and put it before a wildcard that should be read literally:

```sql
SELECT code
FROM products
WHERE code LIKE 'SAVE!_%' ESCAPE '!';
```

This matches a code that starts with the literal text `SAVE_`. The final `%` is still a wildcard. A literal percent sign would be written `!%` with this escape character.

If a user types a search term, pass it as a parameter. Decide whether `%` and `_` in that term are meant as patterns or plain text. Escape them when they should be plain text. A parameter prevents SQL injection, but it does not turn pattern wildcards into literal characters by itself.

## Letter case

PostgreSQL offers `ILIKE` for case-insensitive matching according to the active locale. It is a PostgreSQL extension. Behavior can also depend on collation. Test the characters your application accepts, especially outside basic English letters.

## Check your understanding

1. Does `'Book' LIKE 'Book%'` return true?
2. Why does `LIKE '%book%'` cost more work than a simple prefix search in many index setups?
3. Does `NOT LIKE` include a missing text value?

## Further reading

- [PostgreSQL pattern matching](https://www.postgresql.org/docs/current/functions-matching.html)
- [PostgreSQL collations](https://www.postgresql.org/docs/current/collation.html)
