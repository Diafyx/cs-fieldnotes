# Permissions and Transactions Part-1

Permissions answer who may use a database object. Transactions answer which changes are kept together. A safe application needs both: the right role for each task and a clear commit point for each group of writes. These examples use PostgreSQL.

## Give a role only the access it needs

Assume an administrator owns schema `app`, table `app.orders`, and a login role named `report_reader` already exists:

```sql
GRANT USAGE ON SCHEMA app TO report_reader;
GRANT SELECT ON TABLE app.orders TO report_reader;
```

`USAGE` lets the role look up objects in the schema. `SELECT` permits reading this table. These grants do not permit updating or deleting its rows. A role might still have more access through another role or `PUBLIC`, so inspect the full set of permissions before calling it read-only.

## Keep related changes together

```sql
BEGIN;
UPDATE app.orders SET status = 'paid' WHERE order_id = 42;
INSERT INTO app.order_events (order_id, event_name)
VALUES (42, 'paid');
COMMIT;
```

This example changes an order and writes its event in one transaction. `COMMIT` keeps both. If either statement fails, the application must end the failed transaction with `ROLLBACK` and handle the error. The example also assumes order 42 exists and that the role has the required `UPDATE` and `INSERT` privileges. Check the number of rows changed before treating the work as successful.

PostgreSQL also allows many permission changes inside a transaction. An administrator can group related `GRANT` and `REVOKE` commands, check them, and commit them together. Granting access does not make a poorly written update safe; a missing `WHERE` can still affect every row the role may update.

## Check your understanding

1. Why are both schema `USAGE` and table `SELECT` shown?
2. What should happen if the event insert fails after the order update?
3. Why is a successful `UPDATE` command not proof that order 42 existed?

## Further reading

- [PostgreSQL privileges](https://www.postgresql.org/docs/current/ddl-priv.html)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
