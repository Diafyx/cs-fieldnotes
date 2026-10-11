# Connection, Connection Pool and Commit

A connection is one client's live link to PostgreSQL. A transaction is a group of statements run through a connection. `COMMIT` ends that transaction and keeps its changes. It does not close the connection.

## See the separate steps

```sql
CREATE TEMP TABLE jobs (
  job_id integer PRIMARY KEY,
  status text NOT NULL
);
INSERT INTO jobs VALUES (1, 'waiting');
```

```sql
BEGIN;
UPDATE jobs SET status = 'done' WHERE job_id = 1;
COMMIT;
```

```sql
SELECT job_id, status FROM jobs;
```

The final query returns `(1, 'done')`. The connection can run that query after `COMMIT` because it remains open. If the update fails, the application should roll back before reusing the connection. A connection left in an open transaction can hold locks and delay other work.

## Why pools exist

Opening and keeping a database connection uses resources. A pool keeps a limited set of connections ready for requests. An application borrows a connection, runs its work, commits or rolls back, and returns the connection. Pool size should fit the database's connection capacity and the application's workload.

An application library can keep its own pool of client connections. PgBouncer is a separate pooler in front of PostgreSQL. In PgBouncer's session mode, one server connection stays with a client session. In transaction mode, a server connection can be reused after each transaction. Session features such as a persistent temporary table or session-level settings may not work as expected across transactions in that mode. The temporary table above is for the basic connection example, not a pattern to carry through transaction pooling.

## Check your understanding

1. Does `COMMIT` close the database connection?
2. What must the application do before returning a connection after a failed write?
3. Why can a session-level temporary table be a poor fit for transaction pooling?

## Further reading

- [PostgreSQL COMMIT](https://www.postgresql.org/docs/current/sql-commit.html)
- [PostgreSQL connection functions](https://www.postgresql.org/docs/current/libpq-connect.html)
- [PgBouncer pooling modes](https://www.pgbouncer.org/features.html)
