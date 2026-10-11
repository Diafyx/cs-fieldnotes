# LOWER() / UPPER()

`LOWER` changes letters to lower case. `UPPER` changes them to upper case. They return text; they do not update the stored column when used in a `SELECT`.

```sql
SELECT LOWER('Hello') AS lower_text,
       UPPER('Hello') AS upper_text;
```

The results are `hello` and `HELLO`.

## Compare text without case for a stated rule

```sql
SELECT product_id
FROM products
WHERE LOWER(category_name) = LOWER('Books');
```

This can match `Books` and `books` under a suitable locale. It is not a complete rule for every language or every kind of text. PostgreSQL's case conversion depends on the active collation and locale. Test the characters your application stores.

If the input is `NULL`, `LOWER` and `UPPER` return `NULL`. A missing category does not pass the equality test. Add `IS NULL` only if missing categories should be included.

## Think about search and storage

Applying `LOWER` to a column in a filter may prevent a plain index on that column from serving the comparison. PostgreSQL can use an expression index such as an index on `LOWER(category_name)` when this search is common. Other options include a case-insensitive collation or a normalized search column. Choose based on the data rule and the queries you run.

Do not lowercase every value by habit. Display names may need their original spelling. Email addresses and identifiers can have their own comparison rules.

## Check your understanding

1. Does `SELECT LOWER(name)` change stored names?
2. Why does `LOWER(NULL) = 'books'` not pass `WHERE`?
3. What index might help if a query often filters by `LOWER(category_name)`?

## Further reading

- [PostgreSQL string functions](https://www.postgresql.org/docs/current/functions-string.html)
- [PostgreSQL expression indexes](https://www.postgresql.org/docs/current/indexes-expressional.html)
- [PostgreSQL collations](https://www.postgresql.org/docs/current/collation.html)
