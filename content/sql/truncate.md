# TRUNCATE

`TRUNCATE` removes all rows from a table. It has no `WHERE` clause. The table, its columns, and its constraints remain. In PostgreSQL, it is often faster than deleting every row one by one, especially for a large table.

```sql
TRUNCATE TABLE import_staging;
```

After this command, `import_staging` is empty. It is useful for a staging table whose old rows are no longer needed. It is a poor choice when only some rows should go: use `DELETE ... WHERE` for that.

## Identity values and related tables

By default, PostgreSQL continues the table's identity or serial sequence after a truncate. To reset sequences owned by the table, write:

```sql
TRUNCATE TABLE import_staging RESTART IDENTITY;
```

Resetting a sequence does not promise that every later ID will be gap-free. PostgreSQL normally refuses to truncate a table that other tables refer to through foreign keys unless those tables are included too. `CASCADE` can include those related tables, which may remove far more data than expected. List the intended tables explicitly and inspect their relationships first.

## Transaction, locks, and triggers

```sql
BEGIN;
TRUNCATE TABLE import_staging;
ROLLBACK;
```

In PostgreSQL, the rollback restores the rows. The common claim that `TRUNCATE` can never be rolled back is false for PostgreSQL. It also takes a strong lock, so another session may have to wait to use the table while the transaction is open. Keep the transaction short.

`TRUNCATE` does not fire row-level `ON DELETE` triggers. It can fire `ON TRUNCATE` triggers. It also has different visibility behavior from ordinary row deletion for some concurrent transactions. Use `DELETE` when per-row delete behavior or a filtered removal is part of the rule.

## Check your understanding

1. Can `TRUNCATE` remove just last year's rows?
2. What does `RESTART IDENTITY` change?
3. Does `ROLLBACK` undo a PostgreSQL truncate in the example transaction?

## Further reading

- [PostgreSQL TRUNCATE](https://www.postgresql.org/docs/current/sql-truncate.html)
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
