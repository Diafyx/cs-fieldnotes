# B-Trees and B+ Trees

A B-tree is a balanced search tree designed to work well with storage pages. Its keys are sorted, and a search follows a short path from the root to the page containing the wanted key. Database indexes usually use a B-tree family design because a page can hold many keys and point to many child pages.

In the textbook distinction, a **B-tree** may store searchable records in internal and leaf nodes. A **B+ tree** uses internal nodes to guide searches and keeps the data entries at the leaves. Neighboring leaves can be linked, so a range search can read forward after finding its starting key. PostgreSQL calls its ordered index access method a B-tree; its internal pages guide searches and its leaf pages contain index entries. The exact PostgreSQL page rules are more detailed than a classroom drawing.

## Follow a search

Imagine this small B+ tree. Each leaf holds two keys. The internal key `30` separates the ranges:

```text
             root [30]
              /     \
     leaf [10, 20]  leaf [30, 40]
```

A search for `35` chooses the right leaf and finds no match. A search for keys from `20` through `40` starts in the left leaf at `20`, then reads the next leaf. The values in the leaves stand for index entries, not whole PostgreSQL table rows.

Because each internal page can route to many children, the tree stays shallow as it grows. Search cost depends on tree height and on any heap pages needed after the index lookup. For a range query, cost also depends on how many leaf entries and table rows match. A tree does not make every query fast.

## Insert, delete, and duplicate keys

To insert a key, search for its leaf and put it in sorted position. If the page lacks room, the tree splits it and updates parent routing. A split can reach the root and make the tree taller. Deletions and updates also need index maintenance; PostgreSQL can reclaim dead entries and uses vacuum work as part of keeping indexes healthy. Real systems handle concurrent changes, row versions, and page space, so they do not always perform a simple textbook merge after every deletion.

A non-unique B-tree can have several entries for one key. A unique B-tree checks uniqueness under the database's SQL rules. PostgreSQL uses B-tree indexes for primary keys and unique constraints. A B-tree can help equality, range, and some ordered queries, but it does not sort the heap itself and it does not promise query output order without `ORDER BY`.

## Try one range query

```sql
CREATE TEMP TABLE items (
    item_id INTEGER PRIMARY KEY,
    label TEXT NOT NULL
);

INSERT INTO items VALUES
    (40, 'D'),
    (10, 'A'),
    (30, 'C'),
    (20, 'B');

SELECT item_id, label
FROM items
WHERE item_id BETWEEN 15 AND 35
ORDER BY item_id;
```

The result is `(20, B)` and `(30, C)`. The primary key gives PostgreSQL a unique B-tree index it may use for the range. Four rows are so few that a table scan may be cheaper. `BETWEEN` includes both endpoints. The `ORDER BY` makes the displayed order certain.

An index-only scan may avoid some heap visits if all needed columns are in the index and PostgreSQL's visibility map permits it. Otherwise, an index entry leads to a heap row version, whose visibility must be checked. More indexes also make inserts and updates do more work.

## Try it yourself

1. Which leaf in the drawing would be searched for `15`?
2. Why are linked leaves useful for `BETWEEN 20 AND 40`?
3. Does adding the primary key force the example table's heap rows into ID order?

## References

- [PostgreSQL B-tree indexes](https://www.postgresql.org/docs/current/btree.html)
- [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html)
- [MIT Database Systems lecture on access methods](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/1343b2699f7d4c76a768b8f45b1674b1_MIT6_830F10_lec06.pdf)
