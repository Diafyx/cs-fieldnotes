# Savepoint

A savepoint marks a point inside a transaction. `ROLLBACK TO` undoes work done after that point while keeping earlier work in the same transaction. It is useful when one optional step can fail without canceling the whole task.

## Try it

Start with two items:

```sql
CREATE TEMP TABLE items (
  item_id integer PRIMARY KEY,
  quantity integer NOT NULL CHECK (quantity >= 0)
);
INSERT INTO items VALUES (1, 5), (2, 5);
```

Keep the first change and cancel the second:

```sql
BEGIN;
UPDATE items SET quantity = 3 WHERE item_id = 1;
SAVEPOINT before_optional;
UPDATE items SET quantity = 0 WHERE item_id = 2;
ROLLBACK TO SAVEPOINT before_optional;
RELEASE SAVEPOINT before_optional;
COMMIT;
```

```sql
SELECT item_id, quantity FROM items ORDER BY item_id;
```

The result is `(1, 3)` and `(2, 5)`. Rolling back to the savepoint removed the second update. The first update remained in the transaction and was saved by `COMMIT`.

## How the marker works

`ROLLBACK TO` keeps the named savepoint so you may use it again. `RELEASE SAVEPOINT` removes it and keeps the work done so far. A final `ROLLBACK` of the whole transaction still discards all its changes, including work kept after a savepoint. A savepoint is not an independent nested transaction.

PostgreSQL can recover from a statement error inside a transaction by rolling back to a savepoint set before that statement. The application still needs to handle the error and decide whether to continue. Avoid making a savepoint for every statement without a reason; it adds work and makes transaction flow harder to follow.

## Check your understanding

1. Which update survives the example's `COMMIT`?
2. Does `ROLLBACK TO` remove the named savepoint?
3. Would an outer `ROLLBACK` keep the first update?

## Further reading

- [PostgreSQL SAVEPOINT](https://www.postgresql.org/docs/current/sql-savepoint.html)
- [PostgreSQL ROLLBACK TO SAVEPOINT](https://www.postgresql.org/docs/current/sql-rollback-to.html)
- [PostgreSQL RELEASE SAVEPOINT](https://www.postgresql.org/docs/current/sql-release-savepoint.html)
