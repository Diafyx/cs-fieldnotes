# File Organization

File organization is the way records are placed in a table's storage pages. It affects how the database finds rows, adds rows, and reads a large range of rows. The physical layout of a table is separate from the logical columns and keys you declare.

## Common layouts

| Layout | Basic idea | Good at | Cost or limit |
| --- | --- | --- | --- |
| Heap file | Put a row where free space is available. | Inserts and full scans. | Finding one row often needs an index or a scan. |
| Sorted file | Keep records in key order. | Ordered and range reads. | Inserts may need movement or extra space. |
| Hash file | Use a hash of a key to choose a bucket. | Equality lookup. | No useful key order for ranges. |
| Index-organized table | Store full rows in a key structure. | Key lookups without a separate heap visit. | Layout and update costs depend on the database. |

These are general storage choices, not four commands that every database supports. PostgreSQL's ordinary table access method is a heap. Rows are not kept in primary key order. Its indexes are separate relations that point toward heap row versions. A heap can use a free space map to find a page with room for an insert.

PostgreSQL's `CLUSTER` command can rewrite a table in the order of an index at that moment. Later writes do not maintain that order automatically. An index is therefore useful for finding rows, but it does not turn an ordinary PostgreSQL heap into an always-sorted file.

## A table can be read in several ways

The same table may be read by a sequential scan, an index scan, a bitmap heap scan, or another plan. A sequential scan walks table pages and tests rows. An index scan first looks up index entries, then visits matching heap rows when needed. When many rows match, scanning pages in order may cost less than many scattered heap visits. The planner chooses based on estimates, not the mere presence of an index.

```sql
CREATE TEMP TABLE file_demo (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO file_demo VALUES
    (30, 'C'),
    (10, 'A'),
    (20, 'B');

SELECT id, name
FROM file_demo
ORDER BY id;
```

The query returns `(10, A)`, `(20, B)`, and `(30, C)`. That order comes from `ORDER BY`, not from the primary key rearranging the heap. A different query without `ORDER BY` has no promised result order, even if its chosen plan happens to visit rows in a familiar sequence.

## Row versions and large values

PostgreSQL uses multiple row versions for concurrency. An update normally creates a new version rather than editing the old version in place. If indexed columns do not change and there is room on the same page, a heap-only tuple, or HOT update, can avoid new entries in ordinary indexes. Old versions need cleanup when no active transaction can see them.

Very large column values may be compressed or moved to a TOAST table. A table also has free space and visibility maps. These details mean a table's physical size is more than the sum of its visible values, and a row may not be stored entirely in one ordinary heap tuple.

Partitioning is a different choice: it divides a logical table into separate physical tables by a rule such as date range. Each partition still has its own file organization and indexes. A partition key does not replace an index on every query pattern.

## Try it yourself

1. Why does the example's primary key fail to promise output order without `ORDER BY`?
2. When might a sequential scan beat an index scan?
3. What changes after running `CLUSTER` and then inserting many new rows?

## References

- [PostgreSQL database file layout](https://www.postgresql.org/docs/current/storage-file-layout.html)
- [PostgreSQL CLUSTER](https://www.postgresql.org/docs/current/sql-cluster.html)
- [PostgreSQL heap-only tuples](https://www.postgresql.org/docs/current/storage-hot.html)
- [PostgreSQL TOAST](https://www.postgresql.org/docs/current/storage-toast.html)
