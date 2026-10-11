# DELETE vs. TRUNCATE vs. DROP

All three commands can leave you with no usable rows, but they do different work. In PostgreSQL, `DELETE` removes selected rows, `TRUNCATE` clears all rows, and `DROP TABLE` removes the table itself.

## Choose by what must remain

```sql
DELETE FROM logs WHERE created_at < DATE '2025-01-01';
TRUNCATE TABLE import_staging;
DROP TABLE old_import_staging;
```

The first command keeps recent logs and the `logs` table. The second leaves `import_staging` empty but keeps its definition. The third removes `old_import_staging`, including its definition. A later query against a dropped table fails unless the table is created again.

`DELETE FROM logs;` without `WHERE` also removes every log row, but it still works row by row. It can fire row-level delete triggers and obeys the table's foreign-key delete rules. `TRUNCATE` does not fire `ON DELETE` triggers and cannot filter rows. It has its own foreign-key restrictions and can fire `ON TRUNCATE` triggers. `DROP TABLE` may be blocked by dependent objects; `CASCADE` can remove those dependencies too.

## Transactions and storage

In PostgreSQL, all three commands can be rolled back when run inside a transaction that has not committed. Do not rely on this across every database product. A committed change needs a backup or other recovery plan if the data must be restored.

Deleting rows does not necessarily make the table file shrink at once. PostgreSQL later reuses or cleans dead row space through its maintenance process. Truncating a table reclaims its table storage more directly. Dropping a table removes the table as an object. These differences matter on large tables, but the data rule should come first.

For a production change, write down which rows or objects should disappear. Review dependent tables and triggers. Run the command in a transaction when practical, inspect its result, and commit only after checking it. `TRUNCATE` and `DROP TABLE` take strong locks, so schedule large changes with other users of the database in mind.

## Check your understanding

1. Which command removes old rows but keeps recent rows?
2. Which command leaves the table definition in place while clearing every row?
3. Why can `DROP TABLE ... CASCADE` remove more than one object?

## Further reading

- [PostgreSQL DELETE](https://www.postgresql.org/docs/current/sql-delete.html)
- [PostgreSQL TRUNCATE](https://www.postgresql.org/docs/current/sql-truncate.html)
- [PostgreSQL DROP TABLE](https://www.postgresql.org/docs/current/sql-droptable.html)
