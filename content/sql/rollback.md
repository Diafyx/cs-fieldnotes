# Rollback

`ROLLBACK` ends the current transaction and discards its uncommitted changes. Use it when a group of writes cannot be completed safely. A rollback does not undo an earlier `COMMIT`.

## Try it

Create one item:

```sql
CREATE TEMP TABLE stock (
  item_id integer PRIMARY KEY,
  quantity integer NOT NULL CHECK (quantity >= 0)
);
INSERT INTO stock VALUES (1, 5);
```

Change its quantity, then cancel the transaction:

```sql
BEGIN;
UPDATE stock SET quantity = 2 WHERE item_id = 1;
ROLLBACK;
```

```sql
SELECT item_id, quantity FROM stock;
```

The result is `(1, 5)`. The update was never committed. Within the transaction, a query on the same connection would have seen `2`. Other sessions do not see that uncommitted value.

## What happens after an error?

In PostgreSQL, a statement error leaves the transaction in a failed state. Later ordinary statements in that transaction fail until you run `ROLLBACK`, or roll back to a savepoint created before the error. An application should also roll back when it detects a business error, such as an update that matched no row.

Some effects are outside transaction rollback. For example, a PostgreSQL sequence value consumed by `nextval` is not put back. A message sent to another service is not undone by a database rollback. Design retries with these facts in mind.

If you run `ROLLBACK` without an open transaction, PostgreSQL issues a warning and does not change previously committed data. Keep a clear transaction boundary so it is easy to tell what can still be canceled.

## Check your understanding

1. What quantity remains after the example's rollback?
2. Can `ROLLBACK` undo a transaction that was already committed?
3. What should an application do with a PostgreSQL transaction after a statement error?

## Further reading

- [PostgreSQL ROLLBACK](https://www.postgresql.org/docs/current/sql-rollback.html)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [PostgreSQL sequence functions](https://www.postgresql.org/docs/current/functions-sequence.html)
