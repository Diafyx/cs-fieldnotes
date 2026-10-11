# Introduction to SQL

SQL is the language you use to ask a relational database for data and to change that data. You describe the result you want. The database decides how to find it. That difference matters: a query says which rows meet a condition, while the database chooses whether to scan a table, use an index, or combine several steps.

The examples in these notes use PostgreSQL. Most basic queries also work in other relational databases. Functions, data types, and some commands vary between products, so check the database you actually use.

## Start with a small table

Imagine a `books` table with one row per book:

```sql
CREATE TABLE books (
    book_id integer PRIMARY KEY,
    title text NOT NULL,
    price numeric(8, 2) NOT NULL
);

INSERT INTO books (book_id, title, price) VALUES
    (1, 'The River', 12.50),
    (2, 'Small Maps', 18.00),
    (3, 'Northbound', 9.75);
```

To see the titles of books that cost less than 15:

```sql
SELECT title
FROM books
WHERE price < 15
ORDER BY title;
```

The result has two rows: `Northbound` and `The River`. `FROM` names the source table, `WHERE` keeps matching rows, `SELECT` chooses the output column, and `ORDER BY` makes the output order predictable. Without `ORDER BY`, the database does not promise any particular row order.

## What SQL is used for

The main jobs are easy to separate:

- `SELECT` reads data. It can filter, join, group, and sort rows.
- `INSERT`, `UPDATE`, and `DELETE` change rows.
- `CREATE TABLE` and `ALTER TABLE` change the database structure.
- `BEGIN`, `COMMIT`, and `ROLLBACK` control a group of changes as one transaction.
- Constraints such as `PRIMARY KEY` and `FOREIGN KEY` protect rules about the data.

SQL works with rows and sets of rows. A single statement can update many rows, so a condition is not an optional detail. Before running an `UPDATE` or `DELETE`, check its `WHERE` clause and, when useful, run a matching `SELECT` first.

## SQL and the database are different things

SQL is a language. PostgreSQL, MySQL, SQLite, and other database systems implement that language and add their own features. A Python program or Java program is a client. It sends SQL to a database and reads the result. The program does not become the database just because it contains a query string.

When a query contains a value from a user, pass that value as a parameter. Do not join it into SQL text. Python's `sqlite3` placeholders and Java's `PreparedStatement` both keep values separate from the SQL command.

## Check your understanding

1. In the example, what changes if you remove `ORDER BY title`?
2. Which command would add a new book? Which command would change its price?
3. Why does a Python or Java application still need a database system to run SQL?

## Further reading

- [PostgreSQL SQL tutorial](https://www.postgresql.org/docs/current/tutorial-sql.html)
- [PostgreSQL SELECT reference](https://www.postgresql.org/docs/current/sql-select.html)
- [Python sqlite3 parameters](https://docs.python.org/3/library/sqlite3.html)
- [Java prepared statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)
