# LEFT() / RIGHT() / SUBSTRING()

These functions take part of a string. `LEFT` starts at the beginning. `RIGHT` starts at the end. `SUBSTRING` starts at a chosen position. In PostgreSQL, positions start at 1.

```sql
SELECT LEFT('abcdef', 2) AS first_two,
       RIGHT('abcdef', 2) AS last_two,
       SUBSTRING('abcdef' FROM 2 FOR 3) AS middle_three;
```

The results are `ab`, `ef`, and `bcd`. Position 2 is `b`, and the count 3 takes `b`, `c`, and `d`.

## Use a slice for a stated format

```sql
SELECT product_id,
       LEFT(product_code, 3) AS code_prefix
FROM products;
```

This works if the first three characters are truly the product prefix. If code lengths or formats vary, validate them before slicing. A short code returns the available characters; a missing code returns `NULL`.

`SUBSTRING(product_code FROM 4)` takes from the fourth character to the end. PostgreSQL also accepts a function form with comma-separated arguments, but the `FROM` and `FOR` form makes the start and count easy to see.

## Characters are not always visible symbols

These functions count text characters, not bytes. A visible symbol can sometimes use more than one Unicode character, so cutting in the middle of such a sequence may produce awkward text. For user-visible text limits, test the kinds of text people can enter.

## Check your understanding

1. What does `SUBSTRING('abcdef' FROM 1 FOR 2)` return?
2. Is the first PostgreSQL string position 0 or 1?
3. Why might a fixed three-character prefix be wrong for some product codes?

## Further reading

- [PostgreSQL string functions](https://www.postgresql.org/docs/current/functions-string.html)
