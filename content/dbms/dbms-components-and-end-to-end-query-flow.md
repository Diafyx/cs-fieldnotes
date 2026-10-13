# DBMS Components and End-to-End Query Flow

A DBMS has several parts because a SQL request does more than read a file. The server must understand the statement, check that it is allowed, choose a way to run it, find the data, and send a result. For writes, it must also coordinate other transactions and make committed changes recoverable.

This page follows one PostgreSQL request from a client to the stored rows and back. Other database systems use similar ideas, but their internal parts differ.

## Follow one query

```sql
CREATE TEMP TABLE purchases (
  purchase_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  amount numeric(10, 2) NOT NULL
);
INSERT INTO purchases VALUES
  (1, 7, 20.00), (2, 8, 5.00), (3, 7, 10.00);

SELECT purchase_id, amount
FROM purchases
WHERE customer_id = 7
ORDER BY purchase_id;
```

The query returns `(1, 20.00)` and `(3, 10.00)`. The table is temporary, so it is visible only in this database session. A client such as `psql`, a Python driver, or JDBC sends the SQL to PostgreSQL over a connection.

| Part | What it does for this request |
| --- | --- |
| Connection and access control | Identifies the database role and checks permission to use the objects |
| Parser and analysis | Checks SQL syntax, names, and types |
| Rewrite step | Expands relevant views or rules when needed |
| Planner | Chooses scans, filters, and sort work based on available paths and estimates |
| Executor | Runs that plan and produces rows |
| Buffer and storage layers | Read needed pages from memory or storage |
| Client protocol | Sends rows and status back to the client |

The planner might scan this tiny table. On a much larger table, an index on `customer_id` might help, but an index is not a promise that the planner will use it. `EXPLAIN` shows the chosen plan; `EXPLAIN ANALYZE` also runs the statement and measures what happened. A plan's estimated cost is not elapsed time.

PostgreSQL also keeps system catalogs with table, column, index, and role definitions. The planner uses collected statistics to estimate how many rows each step may read. A buffer manager keeps frequently used pages in memory. Background maintenance such as vacuum reclaims space from old row versions and updates information the server needs to keep working well. These parts matter even though the client does not call them directly for each query.

## Writes and concurrent readers

An `INSERT` or `UPDATE` goes through planning and execution too. PostgreSQL uses row versions so transactions can see data according to their snapshots. Locks and transaction rules coordinate conflicting changes. Write-ahead logging records information needed to recover committed changes after a crash. Buffer pages can be written to data files later; a successful commit does not mean every changed table page was written at that instant.

The client also has work. It may wait for a network round trip, fetch many rows, decode values, and render a page. A server plan that runs quickly can still lead to a slow screen if the application asks for too much data. Measure both database time and full request time.

When debugging, locate the stage first. A syntax error points to parsing. A missing column points to name checking. A valid but slow query calls for a plan and row count check. A blocked write calls for lock and transaction checks. A connection failure may happen before PostgreSQL sees any SQL.

## Check your understanding

1. Which part chooses between a table scan and an index scan?
2. Why can a committed write survive even if changed table pages are written later?
3. Why can a fast database query still make a page feel slow?

## Further reading

- [PostgreSQL path of a query](https://www.postgresql.org/docs/current/query-path.html)
- [PostgreSQL executor](https://www.postgresql.org/docs/current/executor.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL write-ahead log](https://www.postgresql.org/docs/current/wal-intro.html)
- [PostgreSQL system catalogs](https://www.postgresql.org/docs/current/catalogs.html)
