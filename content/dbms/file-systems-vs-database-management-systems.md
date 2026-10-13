# File Systems vs Database Management Systems

A file system stores and retrieves files. A database management system, or DBMS, uses files too, but it gives applications a way to work with records and rules. It can check keys, run queries, coordinate concurrent changes, and recover committed work after a crash. PostgreSQL is a DBMS. A CSV file on disk is not a DBMS by itself.

## A small example

Suppose two programs both store customer emails. If each program writes a CSV file, each must know how to check for duplicates and how to avoid overwriting the other's changes. A database can hold the shared rule:

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  email text NOT NULL UNIQUE
);

INSERT INTO customers VALUES
  (1, 'ada@example.test'),
  (2, 'lin@example.test');

SELECT customer_id, email FROM customers ORDER BY customer_id;
```

The query returns the two inserted customers. A third row with `ada@example.test` would be rejected by the `UNIQUE` constraint, even if it came from a different application. The rule is checked where the shared data is stored. If emails should be case insensitive, this exact constraint is not enough: `Ada@example.test` and `ada@example.test` are different text values under ordinary PostgreSQL equality. Choose a normalization rule or an appropriate case insensitive key before relying on the constraint.

## What the DBMS adds

| Need | Files alone | DBMS |
| --- | --- | --- |
| Find a few matching records | Application reads and searches data, or builds its own index | Query language and indexes |
| Keep a shared rule | Every writer must cooperate | Constraints can reject invalid rows |
| Change several records together | Application designs a recovery method | Transactions can commit or roll back together |
| Support concurrent writers | Application designs locking and conflict handling | DBMS coordinates access under its transaction rules |
| Recover after a crash | Application designs safe writes and backup | DBMS provides recovery and backup methods |

The DBMS does not make every query fast or every schema good. You still need useful indexes, correct transaction boundaries, and tested backups. A database also adds setup and operating work. A file can be the better choice for a photo, a document, or a small export that no one needs to query or update concurrently. An application often stores the file in object storage and keeps its owner, path, and permissions in a database.

Do not confuse a DBMS with a network server. SQLite is an embedded DBMS that runs inside an application and normally stores a database in a local file. PostgreSQL is commonly used as a client/server DBMS. Both give more structure than a plain file, but their concurrency and deployment models differ.

## Check your understanding

1. What extra code would two CSV writers need to enforce a unique email rule safely?
2. Why can a DBMS still need a file system?
3. When might storing the actual photo in object storage be simpler than storing it in a table?

## Further reading

- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [SQLite: appropriate uses](https://www.sqlite.org/whentouse.html)
