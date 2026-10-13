# Triggers, Stored Routines, and Database-Side Logic

A trigger runs database code when a named event happens. In PostgreSQL, triggers can respond to `INSERT`, `UPDATE`, `DELETE`, and `TRUNCATE` on supported relations. A row trigger runs for each affected row. A statement trigger runs once for the statement, even when the statement affects no rows. PostgreSQL also has triggers on views for some events.

Stored routines put reusable logic in the database. A **function** returns a value and can be called in an expression when its type permits. A **procedure** is called with `CALL` and is useful for a unit of database work. A PostgreSQL trigger calls a trigger function, which returns the special `trigger` type. `NEW` holds the new row for an insert or update; `OLD` holds the old row for an update or delete.

## Trigger timing

| Timing | Typical use |
| --- | --- |
| `BEFORE` | Check or change a row before it is stored. |
| `AFTER` | React after the row change, such as writing an audit row. |
| `INSTEAD OF` | Handle an attempted change to a view. |

A `BEFORE` row trigger can change `NEW` or return `NULL` to skip that row. An `AFTER` row trigger sees the completed change, and its return value is ignored. Trigger actions run in the same transaction as the statement that fired them. If the transaction rolls back, its audit rows roll back too.

This PostgreSQL example records inserted order IDs. Run it in a scratch database. The transaction rolls back all objects at the end.

```sql
BEGIN;

CREATE TABLE demo_orders (
    order_id INTEGER PRIMARY KEY
);

CREATE TABLE demo_order_audit (
    order_id INTEGER NOT NULL,
    action TEXT NOT NULL
);

CREATE FUNCTION demo_log_order_insert()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO demo_order_audit (order_id, action)
    VALUES (NEW.order_id, 'insert');
    RETURN NEW;
END;
$$;

CREATE TRIGGER demo_order_insert_audit
AFTER INSERT ON demo_orders
FOR EACH ROW
EXECUTE FUNCTION demo_log_order_insert();

INSERT INTO demo_orders VALUES (10), (11);

SELECT order_id, action
FROM demo_order_audit
ORDER BY order_id;

ROLLBACK;
```

The query returns `(10, insert)` and `(11, insert)`. The one `INSERT` statement added two rows, so the row trigger ran twice. With `FOR EACH STATEMENT`, it would run once, and there would be no single `NEW` row.

## Where database logic belongs

Use a primary key, foreign key, `NOT NULL`, or `CHECK` for rules those constraints can express. A constraint is easier to see and harder to bypass by accident. Use a trigger when the action truly depends on a row change, such as recording an audit event. Use a function for reusable database calculations. Put logic where every writer must follow it, even if several applications write to the same database.

Triggers can make writes slower and harder to trace. A trigger may fire more triggers, so check for unwanted chains or recursion. For a multirow `UPDATE`, do not assume row triggers fire in any useful row order. Keep trigger work small, document its side effects, and test failed statements and rollback. If an audit must survive a rollback, a normal trigger writing in the same transaction cannot provide that guarantee.

Functions also have permission and security settings. PostgreSQL functions run with the caller's privileges by default; `SECURITY DEFINER` uses the function owner's privileges and needs careful review, including a safe `search_path`. Do not add elevated privileges just to avoid granting the right table access.

## Try it yourself

1. How many times does the example trigger run if the `INSERT` adds zero rows?
2. What happens to the audit rows if a later command in the transaction fails and you roll back?
3. Why should a nonnegative salary rule usually be a `CHECK` constraint instead of a trigger?

## References

- [PostgreSQL triggers](https://www.postgresql.org/docs/current/triggers.html)
- [PostgreSQL CREATE TRIGGER](https://www.postgresql.org/docs/current/sql-createtrigger.html)
- [PostgreSQL trigger functions](https://www.postgresql.org/docs/current/plpgsql-trigger.html)
- [PostgreSQL CREATE FUNCTION](https://www.postgresql.org/docs/current/sql-createfunction.html)
