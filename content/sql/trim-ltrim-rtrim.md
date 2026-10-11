# TRIM() / LTRIM() / RTRIM()

These functions remove characters from the edges of text. `TRIM` works on both ends, `LTRIM` on the left, and `RTRIM` on the right. They do not remove characters from the middle.

```sql
SELECT TRIM('  Ada  ') AS both_sides,
       LTRIM('  Ada  ') AS left_side,
       RTRIM('  Ada  ') AS right_side;
```

The results are `Ada`, `Ada  `, and `  Ada`. The spaces inside the quoted results matter.

## Remove chosen edge characters

In PostgreSQL, the second argument to `LTRIM` or `RTRIM` is a set of characters to remove, not one exact prefix or suffix:

```sql
SELECT LTRIM('xxxyCode', 'xy') AS cleaned;
```

The result is `Code`. PostgreSQL removes leading `x` and `y` characters until it reaches `C`. It does not look for the full text `xy` in one piece. Standard `TRIM` can name the side and character set, for example `TRIM(BOTH '.' FROM '...note...')` returns `note`.

Without a character argument, PostgreSQL removes ordinary space characters. It does not automatically remove every kind of whitespace. If tabs or line breaks can appear, define and test a separate cleanup rule.

An empty string stays empty. A `NULL` input returns `NULL`. `TRIM` in a `SELECT` only changes the displayed result, so bad input can keep returning until the stored data is fixed.

## Check your understanding

1. Does `TRIM('a  b')` remove the spaces between `a` and `b`?
2. Why does `LTRIM('xxxyCode', 'xy')` remove four leading characters?
3. Does ordinary `TRIM` remove every tab by default?

## Further reading

- [PostgreSQL string functions](https://www.postgresql.org/docs/current/functions-string.html)
