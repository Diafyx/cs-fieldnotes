# REPLACE()

`REPLACE` finds every occurrence of one piece of text and substitutes another piece. In a `SELECT`, it makes a new output value. It does not change the stored column.

```sql
SELECT REPLACE('red red', 'red', 'blue') AS changed;
```

The result is `blue blue`. Both occurrences change. If the piece to find is absent, the original text is returned.

## Clean a repeated marker

```sql
SELECT item_id,
       REPLACE(description, '[draft]', '') AS display_description
FROM items;
```

This removes every exact `[draft]` piece from the displayed description. It can also remove that text in the middle of a sentence, even when it was meant literally. Check a few real rows before using a broad replacement rule.

`REPLACE` is not a pattern matcher. `%` and `_` have no wildcard meaning inside its search text. For pattern tests, use `LIKE`; for more complex text changes, PostgreSQL has regular expression functions.

If any required argument is `NULL`, PostgreSQL returns `NULL`. To save a change to the table, an `UPDATE` statement would be needed. Test the `SELECT` version first, especially when replacement could erase useful text.

## Check your understanding

1. Does `REPLACE('red red', 'red', 'blue')` change one or two words?
2. Does the display example update `items.description`?
3. Does `%` work as a wildcard in the search text?

## Further reading

- [PostgreSQL string functions](https://www.postgresql.org/docs/current/functions-string.html)
