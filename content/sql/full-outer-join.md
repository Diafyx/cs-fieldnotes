# FULL OUTER JOIN

A `FULL OUTER JOIN` keeps matching pairs and also keeps rows that match nothing on either side. Missing columns from the other side become `NULL`. It is useful when comparing two lists and seeing what each one lacks.

```sql
WITH planned(item_id, item_name) AS (
  VALUES (1, 'Pen'), (2, 'Book')
), received(item_id, state) AS (
  VALUES (2, 'arrived'), (3, 'unexpected')
)
SELECT COALESCE(p.item_id, r.item_id) AS item_id,
       p.item_name, r.state
FROM planned AS p
FULL OUTER JOIN received AS r ON r.item_id = p.item_id
ORDER BY item_id;
```

The rows are `(1, 'Pen', NULL)`, `(2, 'Book', 'arrived')`, and `(3, NULL, 'unexpected')`. Item 1 was planned but has no receipt. Item 3 was received but was not planned. Item 2 matched. `COALESCE` chooses whichever side has the ID in an unmatched row.

## Decide what a missing side means

An unmatched right side is different from a matched right row whose `state` is itself `NULL`. Test a non-null key such as `r.item_id IS NULL` when you need to identify rows with no right match. The same idea applies to `p.item_id IS NULL` for rows only on the right.

If either input contains several rows with the same ID, every matching pair appears. A full join does not merge repeated IDs into one row. If you need one row per ID, decide which input row represents that ID before joining or group the result under a clear rule.

Some databases do not support `FULL OUTER JOIN` directly. The example uses PostgreSQL. A combination of left and right-only rows can express the same result elsewhere, but it needs care to avoid duplicates.

## Check your understanding

1. Why is item 1 in the result even without a receipt?
2. Which test finds rows that exist only in `received`?
3. What happens if `received` contains two rows with item ID 2?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
