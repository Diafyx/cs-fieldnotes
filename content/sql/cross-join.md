# CROSS JOIN

A `CROSS JOIN` makes every possible pair of rows from two inputs. It has no `ON` condition. If the left side has two rows and the right side has three, the result has six rows.

```sql
WITH colors(color) AS (VALUES ('blue'), ('red')),
     sizes(size_name) AS (VALUES ('S'), ('M'), ('L'))
SELECT c.color, s.size_name
FROM colors AS c
CROSS JOIN sizes AS s
ORDER BY c.color, s.size_name;
```

The six rows are blue with L, M, and S, then red with L, M, and S. The order shown comes from `ORDER BY`; the join itself does not set an order.

## Use all pairs for a real question

A cross join can build a grid of every user and category, every product and size, or every date and store. After making the grid, a left join can attach observed data and reveal missing combinations. Be careful with size: 10,000 users times 1,000 categories makes 10 million pairs before later filters.

If you meant to connect rows by a key, use a qualified join with `ON`. An accidental cross join can multiply totals. A comma-separated `FROM a, b` also makes all pairs unless a later `WHERE` condition filters them, but `CROSS JOIN` states the intent more clearly.

An empty input gives an empty cross-join result. There are no pairs if one side has no rows.

## Check your understanding

1. How many rows would five colors and four sizes produce?
2. Why can a missing join condition make a report total much too large?
3. What happens if the sizes input is empty?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
