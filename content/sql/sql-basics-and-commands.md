# SQL Basics and Commands

An SQL statement is a command sent to a database. The command may read rows, change rows, change a table, or control a transaction. You can write many statements in one file, but it helps to understand what each statement can change before you run it.

The examples here use PostgreSQL. Other databases share much of the syntax but can differ on data types, functions, and administrative commands.

## The commands you will use first

```sql
CREATE TABLE tasks (
    task_id integer PRIMARY KEY,
    title text NOT NULL,
    done boolean NOT NULL DEFAULT false
);

INSERT INTO tasks (task_id, title) VALUES (1, 'Read chapter one');

SELECT task_id, title, done FROM tasks;

UPDATE tasks SET done = true WHERE task_id = 1;

DELETE FROM tasks WHERE task_id = 1;
```

`CREATE TABLE` defines a table. `INSERT` adds rows. `SELECT` reads rows. `UPDATE` changes rows. `DELETE` removes rows. The semicolon ends a statement in SQL tools and scripts. Uppercase keywords are a reading habit, not a requirement in PostgreSQL.

## A useful command map

People often group commands by purpose:

- Data definition: `CREATE`, `ALTER`, and `DROP` change the structure.
- Data manipulation: `INSERT`, `UPDATE`, and `DELETE` change stored rows.
- Queries: `SELECT` reads and combines data.
- Transaction control: `BEGIN`, `COMMIT`, and `ROLLBACK` group changes.
- Access control: `GRANT` and `REVOKE` change permissions.

These labels are a learning aid. They do not tell you how every database handles a command inside a transaction. Check the product documentation for the system you use.

## Names and values

In the example, `tasks` and `task_id` are identifiers. `'Read chapter one'` is a text value. SQL uses single quotes for string literals. PostgreSQL uses double quotes around an identifier when you need an exact mixed-case name or a name containing spaces, but simple lowercase names are easier to work with.

Do not put a user's value directly into a SQL string by concatenation. Use parameters in Python or a `PreparedStatement` in Java. Parameters keep a value separate from the command text.

## Be careful with broad changes

Without `WHERE`, `UPDATE tasks SET done = true` changes every row. `DELETE FROM tasks` removes every row. If you meant to change one row, first run a `SELECT` with the same condition and inspect the result. For important data, use a transaction so you can review and roll back before committing.

```sql
BEGIN;
UPDATE tasks SET done = true WHERE task_id = 1;
SELECT task_id, title, done FROM tasks WHERE task_id = 1;
COMMIT;
```

If the result is wrong, use `ROLLBACK` instead of `COMMIT` while the transaction is still open.

## Check your understanding

1. Which statements in the first example change table structure, and which change rows?
2. What happens if the `WHERE` clause is removed from the `UPDATE`?
3. Why should user input be passed as a parameter instead of pasted into SQL text?

## Further reading

- [PostgreSQL SQL commands](https://www.postgresql.org/docs/current/sql-commands.html)
- [PostgreSQL modifying data](https://www.postgresql.org/docs/current/dml.html)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [Java prepared statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)
