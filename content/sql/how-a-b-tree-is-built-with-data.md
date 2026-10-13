# How a B+ Tree Is Built with Data

A B-tree index keeps keys in order so PostgreSQL can find one key, a range of keys, or the first rows in a matching order. Many database lessons call the layout a B+ tree: internal pages guide the search, while leaf pages hold entries that lead to table rows. PostgreSQL uses its own B-tree implementation, so a small drawing is only a model of the search path.

## A small ordered example

Imagine leaf pages that can hold only two keys. After inserting `10`, `20`, `30`, and `40`, a toy tree might look like this:

```text
             root: [30]
              /       \
leaf: [10, 20]       leaf: [30, 40]
```

To find `35`, the root sends the search to the right leaf, where no matching key is found. To find values from `20` through `40`, the search starts at 20 and reads forward through the leaf entries. Real page capacities, split points, and layout are chosen by PostgreSQL and will not look exactly like this four-key drawing.

## Let PostgreSQL build the index

```sql
CREATE TEMP TABLE catalog_items (
  item_id integer PRIMARY KEY,
  name text NOT NULL
);

INSERT INTO catalog_items VALUES
  (40, 'D'), (10, 'A'), (30, 'C'), (20, 'B');

SELECT item_id, name
FROM catalog_items
WHERE item_id BETWEEN 15 AND 35
ORDER BY item_id;
```

The query returns `(20, B)` and `(30, C)`. The primary key creates a unique B-tree index on `item_id`, even though the rows were inserted in another order. `BETWEEN` includes both endpoints. The final `ORDER BY` guarantees the displayed order. The index helps PostgreSQL consider an ordered range scan, but four rows may be faster to scan directly.

An index entry uses the key to lead to a heap row version. Internal pages route a search toward the right leaf page. Leaf pages hold sorted entries and links for moving through nearby keys. When a page has no room for a new entry, PostgreSQL can split it and update routing information above it. This keeps lookup depth small as more rows are added. An index is not a copy of the entire table row unless selected columns happen to be available in it, and visibility checks can still require heap access.

A unique B-tree rejects a second equal key. A non-unique B-tree can hold several rows with the same key, and PostgreSQL can sometimes store repeated keys more compactly. New inserts and updates must maintain the index, so more indexes can make writes slower. Use `EXPLAIN` on a realistic table to see whether a range query uses the index.

## Check your understanding

1. Which leaf would the toy tree search for key 35?
2. Why do the inserted row order and query output order differ?
3. What extra work does an insert do when an indexed leaf page is full?

## Further reading

- [PostgreSQL B-tree indexes](https://www.postgresql.org/docs/current/btree.html)
- [PostgreSQL index-only scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
