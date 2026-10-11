# How Databases Work

A database system accepts a request, checks what it means, finds or changes the needed rows, and sends a result back. The table you see in SQL is a logical view. The bytes on disk, indexes, cache, and transaction log are physical parts of the system. Keeping those two views separate helps you reason about both correctness and speed.

This note describes a typical relational database, using PostgreSQL as the concrete example. Different products make different internal choices.

## From query to result

For a query such as `SELECT title FROM books WHERE book_id = 7`, the database roughly does the following:

1. **Parse:** Check that the SQL is valid and identify the command, table, columns, and condition.
2. **Plan:** Choose how to reach the rows. A small table may be scanned. A useful index may provide a shorter path.
3. **Execute:** Read the rows, apply the condition, and produce the requested columns.
4. **Return:** Send the result to the client program.

The plan is a choice, not a promise written into the SQL. The database may change plans as data grows or as its statistics change. `EXPLAIN` shows the plan PostgreSQL expects to use. `EXPLAIN ANALYZE` also runs the query and reports what happened, so use it with care for statements that change data.

## Tables and indexes

A table holds rows. An index is another structure that helps locate rows by a value or an expression. Think of an index as a route to records, not as a second copy of the whole table. The database may still need to read table data after finding an index entry.

An index helps only when it fits the query and the data. If most rows match a condition, scanning the table can be cheaper. Every index also needs storage and must be maintained when affected rows change. Add indexes in response to real queries, then inspect their plans and timings.

## Transactions and concurrent work

A transaction groups changes. In PostgreSQL, `BEGIN` starts one, `COMMIT` keeps its changes, and `ROLLBACK` discards them. A transfer between accounts is a useful example: subtracting money from one account and adding it to another should be treated as one unit.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 50 WHERE account_id = 2;
COMMIT;
```

This example shows the shape of a transaction, but a real transfer also needs checks for missing accounts, insufficient funds, and concurrent transfers. A transaction alone does not prove that the business rules are correct.

Databases coordinate concurrent transactions so one user's work does not casually overwrite another's. The exact behavior depends on the isolation level and the commands used. Learn that behavior before assuming two operations cannot interfere.

## What is kept when a process stops

Durability means committed changes should survive a crash according to the database's guarantees. PostgreSQL uses a write-ahead log as part of that work. Memory caches make reads and writes faster, but memory alone would not be enough to keep committed data after a restart.

## Check your understanding

1. Why can the same SQL query use different plans on a small table and a large table?
2. What extra cost does an index add when a row changes?
3. What important checks are missing from the sample transfer?

## Further reading

- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [PostgreSQL write-ahead logging](https://www.postgresql.org/docs/current/wal-intro.html)
