# Where Rows Actually Live

In PostgreSQL, a normal table uses heap pages. A page is usually 8 KB, though a server can be built with another size. Each page has a header, item pointers, free space, and row data. A row's physical position can change as the table is updated or rebuilt. Its primary key is the lasting name your application should use.

## See a row version's location

```sql
CREATE TEMP TABLE notes (
  note_id integer PRIMARY KEY,
  body text NOT NULL
);

INSERT INTO notes VALUES (1, 'first text'), (2, 'other text');

CREATE TEMP TABLE before_update AS
SELECT note_id, ctid AS old_ctid
FROM notes;

UPDATE notes SET body = 'revised text' WHERE note_id = 1;

SELECT n.note_id, n.body, b.old_ctid, n.ctid AS current_ctid,
       b.old_ctid <> n.ctid AS location_changed
FROM notes AS n
JOIN before_update AS b ON b.note_id = n.note_id
ORDER BY n.note_id;
```

The result has note 1 with `revised text` and `location_changed = true`. Note 2 keeps `other text` and has `location_changed = false`. The exact `ctid` values depend on the database, so do not put them in application URLs or foreign keys. `ctid` names a physical row version, not a stable logical row.

## Why updates leave more than one version

PostgreSQL uses multiversion concurrency control. An `UPDATE` creates a new row version so transactions can see the version appropriate to their snapshot. Older versions can remain until they are no longer needed; vacuum and page cleanup later make their space reusable. This is why a table may occupy more space than the latest visible rows alone suggest.

Some updates can use a heap-only tuple, or HOT, path. If no indexed column changes and the page has enough free space, PostgreSQL can keep the new version on the same heap page without adding new entries to ordinary indexes. Adding an index on a frequently changed column may remove that chance. HOT is an optimization, not a rule that every unchanged key gets it.

Very large text, JSONB, or other variable-length values may be compressed or stored out of line by TOAST. A heap row can then hold a reference instead of the whole value. This is one reason `SELECT *` can do more work than selecting a few needed columns. PostgreSQL also keeps a visibility map and free space map for the heap; they help index-only scans and future inserts find usable pages.

If you need to inspect size, `pg_table_size('notes'::regclass)` counts table storage including related TOAST and auxiliary data, while `pg_total_relation_size('notes'::regclass)` also includes indexes. These numbers depend on page allocation and may not change by exactly the size of one inserted row.

## Check your understanding

1. Why did note 1 get a new `ctid` after the update?
2. Why is `note_id` safe for an application reference while `ctid` is not?
3. Which two conditions let an update use HOT?

## Further reading

- [PostgreSQL page layout](https://www.postgresql.org/docs/current/storage-page-layout.html)
- [PostgreSQL system columns](https://www.postgresql.org/docs/current/ddl-system-columns.html)
- [PostgreSQL HOT updates](https://www.postgresql.org/docs/current/storage-hot.html)
- [PostgreSQL TOAST storage](https://www.postgresql.org/docs/current/storage-toast.html)
