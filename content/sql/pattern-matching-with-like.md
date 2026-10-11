# Pattern Matching with LIKE

`LIKE` checks text against a simple pattern. `%` matches zero or more characters. `_` matches exactly one character. The whole text value must fit the pattern.

## Match a prefix or a piece inside text

```sql
SELECT product_id
FROM products
WHERE product_name LIKE 'Book%';
```

This matches `Book` and `Bookcase`, but not `Notebook` under an ordinary case-sensitive collation. To find `Book` anywhere, use `'%Book%'`. A leading `%` often makes an ordinary B-tree index less useful than a fixed prefix pattern.

`LIKE 'A_3'` matches `AB3`, but not `A3`. `_` needs one character; `%` may match none.

## Treat a wildcard as plain text

```sql
SELECT code
FROM products
WHERE code LIKE 'AB!_%' ESCAPE '!';
```

This matches codes beginning with the literal text `AB_`. `!_` is a literal underscore. The final `%` is still a wildcard. Choose an escape character that you can handle in user input.

## Missing values and case

`NULL LIKE 'Book%'` is unknown, so `WHERE` drops the row. PostgreSQL `ILIKE` offers case-insensitive matching according to the active locale. It is a PostgreSQL extension; case rules and collations can change the result. Test the text your users actually enter.

If a pattern comes from a user, pass it as a query parameter. Decide whether the user's `%` and `_` characters are meant as wildcards or plain text. Parameterization keeps input out of SQL code, but it does not escape `LIKE` wildcards for you.

For exclusion rules and more examples, see [LIKE and NOT LIKE](/topics/sql/like-and-not-like.html).

## Check your understanding

1. Does `LIKE 'Book%'` match `Book` with no extra letters?
2. Why does `LIKE 'A_3'` not match `A3`?
3. What does `ESCAPE '!'` change in the code example?

## Further reading

- [PostgreSQL pattern matching](https://www.postgresql.org/docs/current/functions-matching.html)
- [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html)
