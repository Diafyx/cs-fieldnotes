# DDL vs DML

DDL and DML are labels for two kinds of SQL work. Data definition language changes the structure of a database. Data manipulation language changes its rows. The labels are useful for reading a change plan, but real commands can have details that do not fit a neat memory trick.

## Data definition changes the shape

`CREATE TABLE`, `ALTER TABLE`, and `DROP TABLE` are common DDL commands:

```sql
CREATE TABLE tags (
    tag_id integer PRIMARY KEY,
    label text NOT NULL UNIQUE
);

ALTER TABLE tags ADD COLUMN color text;
```

The first statement defines a table. The second changes its columns. DDL can also create or change indexes, views, schemas, and other database objects. A structural change can affect many applications even if it does not directly edit every row.

## Data manipulation changes rows

`INSERT`, `UPDATE`, and `DELETE` are common DML commands:

```sql
INSERT INTO tags (tag_id, label) VALUES (1, 'database');

UPDATE tags SET color = 'green' WHERE tag_id = 1;

DELETE FROM tags WHERE tag_id = 1;
```

The `WHERE` clause on `UPDATE` and `DELETE` controls which rows change. Remove it and all rows in the table are candidates. `SELECT` reads data and is often taught as a separate query category. You do not need to argue about the label to write a correct query.

## Transactions matter more than labels

PostgreSQL allows many DDL statements inside transactions. A migration can create a table and roll it back if something fails. But not every command can run in a transaction block. `CREATE DATABASE`, for example, cannot. Other database products can handle schema changes differently. Do not assume every DDL command will auto-commit or that every one can be rolled back.

```sql
BEGIN;
ALTER TABLE tags ADD COLUMN description text;
UPDATE tags SET description = label WHERE description IS NULL;
COMMIT;
```

This example changes structure and data in one PostgreSQL transaction. Before applying a similar change to a live table, inspect its size, locks, dependencies, and old rows. A successful transaction is still capable of making the wrong change if the SQL is wrong.

## Check your understanding

1. Is adding a column DDL or DML? Is filling that column in existing rows DDL or DML?
2. Why does the absence of `WHERE` matter for `UPDATE`?
3. Why should you check the database product before assuming a schema change can be rolled back?

## Further reading

- [PostgreSQL SQL commands](https://www.postgresql.org/docs/current/sql-commands.html)
- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- [PostgreSQL CREATE DATABASE](https://www.postgresql.org/docs/current/sql-createdatabase.html)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
