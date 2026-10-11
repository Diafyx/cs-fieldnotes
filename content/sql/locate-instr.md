# LOCATE() / INSTR()

`LOCATE` and `INSTR` find where a smaller string first appears inside a larger one in MySQL. PostgreSQL uses `STRPOS` or `POSITION` for the same basic task. The argument order is easy to mix up.

## PostgreSQL forms

```sql
SELECT STRPOS('concatenate', 'cat') AS position_one,
       POSITION('cat' IN 'concatenate') AS position_two;
```

Both return 4. The first `cat` starts at the fourth character. If the text is absent, the result is 0. A missing input returns `NULL`.

## MySQL forms

```sql
SELECT LOCATE('cat', 'concatenate') AS from_locate,
       INSTR('concatenate', 'cat') AS from_instr;
```

These MySQL expressions also return 4. `LOCATE` takes the piece to find first. `INSTR` takes the full string first. PostgreSQL `STRPOS` uses the same argument order as `INSTR`. MySQL `LOCATE` can also take a third argument for the starting position.

## A position is not a pattern match

These functions search for a literal substring. `%` and `_` are ordinary characters here, not `LIKE` wildcards. To ask whether text begins with a piece, `STRPOS(code, 'AB') = 1` can work, but `LIKE 'AB%'` may express the rule more clearly. A zero result means no match, not the first character: positions start at 1.

## Check your understanding

1. What does PostgreSQL `STRPOS('abc', 'x')` return?
2. Which MySQL function puts the substring first?
3. Does `%` act as a wildcard inside `STRPOS`?

## Further reading

- [PostgreSQL string functions](https://www.postgresql.org/docs/current/functions-string.html)
- [MySQL string functions](https://dev.mysql.com/doc/refman/8.4/en/string-functions.html)
