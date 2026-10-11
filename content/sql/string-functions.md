# String Functions

String functions read or change text values in a query result. They can join words, change letter case, remove edge spaces, take part of a value, or find text inside it. The examples on this page use PostgreSQL.

## A small cleanup query

```sql
SELECT customer_id,
       TRIM(full_name) AS clean_name,
       LOWER(email) AS email_for_display,
       CHAR_LENGTH(note) AS note_characters
FROM customers;
```

`TRIM` removes ordinary spaces from the ends of a name. `LOWER` changes letter case according to the database's locale. `CHAR_LENGTH` counts characters in the note. These expressions do not update the table.

The name `email_for_display` is deliberate. Lowercasing an email for display is different from deciding that two stored email addresses identify the same account. Set a data rule before using case conversion to compare or merge accounts.

## Choose the function by the question

- `CONCAT` joins values. `CONCAT_WS` puts a separator between them.
- `TRIM`, `LTRIM`, and `RTRIM` remove chosen characters at the edges.
- `LEFT`, `RIGHT`, and `SUBSTRING` take part of a string.
- `STRPOS` finds the first position of one string inside another.
- `REPLACE` changes every matching piece of text.
- `LIKE` tests a simple pattern with `%` and `_` wildcards.

If an input is `NULL`, many string functions return `NULL`. PostgreSQL's `CONCAT` and `CONCAT_WS` are exceptions: they skip null values. Empty text `''` is still a value and can produce a different result from `NULL`.

## Keep the stored value and the display value separate

Cleaning data only when reading it can hide inconsistent storage. If names arrive with unwanted spaces, validate or clean them when they enter the system. For a search, be clear whether letter case, accents, and spaces should matter. Those rules affect the results and may affect which indexes the database can use.

## Check your understanding

1. Does the example query change stored names?
2. Which function would find the first position of `@` in an email?
3. Why is an empty string different from a missing string?

## Further reading

- [PostgreSQL string functions](https://www.postgresql.org/docs/current/functions-string.html)
- [PostgreSQL pattern matching](https://www.postgresql.org/docs/current/functions-matching.html)
