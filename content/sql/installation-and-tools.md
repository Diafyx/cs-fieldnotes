# Installation and Tools

You need a running database and a way to send it SQL. For these notes, use PostgreSQL and its `psql` terminal. A graphical tool is fine, but learning a few terminal commands makes it easier to follow examples and understand where a query runs.

Install software only from the official project page or a trusted package source. PostgreSQL's Windows download page links to an installer that includes the server, `psql`, and pgAdmin. On other systems, use the download instructions for your operating system.

## Set up a local database

On Windows, install PostgreSQL from the official download page. Keep the password you set for the `postgres` role somewhere safe. Open the installed SQL Shell (`psql`) from the Start menu. It asks for the server, database, port, user, and password. For a default local setup, accept the offered host and port, connect to the `postgres` database, and use the role you created during installation.

If `psql` is already on your command path, a terminal command can connect instead:

```text
psql -h localhost -U postgres -d postgres
```

Once connected, create a separate database for exercises:

```sql
CREATE DATABASE fieldnotes;
```

`CREATE DATABASE` needs a role with permission to create databases. If it fails with a permission error, use the installation administrator role or ask the person who manages the server. Do not try to solve it by putting a password into a script file.

In `psql`, connect to the new database and check the connection:

```text
\c fieldnotes
\conninfo
```

The backslash commands belong to `psql`. They are not SQL, so a different query tool may not understand them. `\q` leaves `psql`, and `\dt` lists tables in the current database.

## Run a first exercise

```sql
CREATE TABLE notes (
    note_id integer PRIMARY KEY,
    title text NOT NULL
);

INSERT INTO notes (note_id, title) VALUES (1, 'First note');

SELECT note_id, title FROM notes;
```

You should see one row. If `CREATE TABLE` says the table already exists, you likely ran the exercise before. Use another table name or remove your own practice table after checking that it contains nothing you need.

## Pick the right tool for the job

- `psql` is useful for running statements, viewing results, and inspecting a database quickly.
- pgAdmin provides a graphical view of databases and objects.
- A code editor is useful for saving SQL in files that you can review and rerun.
- Python's `sqlite3` module is a quick way to practice basic SQL without a PostgreSQL server, but SQLite and PostgreSQL do not have identical syntax or data types.
- Java applications commonly use JDBC. Use prepared statements for values that come from users or other outside input.

Keep examples in a throwaway learning database. Do not practice `DROP`, `TRUNCATE`, or broad `UPDATE` statements against data you care about.

## Check your understanding

1. Which lines above are SQL, and which are `psql` commands?
2. Why should your exercises use a separate database?
3. If `psql` cannot connect, what would you check before changing the SQL statement?

## Further reading

- [PostgreSQL downloads](https://www.postgresql.org/download/)
- [PostgreSQL Windows installer information](https://www.postgresql.org/download/windows/)
- [PostgreSQL psql reference](https://www.postgresql.org/docs/current/app-psql.html)
- [PostgreSQL creating a database](https://www.postgresql.org/docs/current/tutorial-createdb.html)
