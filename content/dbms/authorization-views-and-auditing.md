# Authorization, Views, and Auditing

Authentication answers **who connected**. Authorization answers **what that identity may do**. Auditing records **what happened** so a person can investigate later. These are separate jobs. A successful login should not mean a role can read every table, and a granted privilege does not create an audit trail by itself.

## Build access from small grants

In PostgreSQL, a role can have `LOGIN`, own objects, receive privileges, or inherit privileges from another role. A user often needs database `CONNECT`, schema `USAGE`, and an object privilege such as table `SELECT`. A grant to `PUBLIC` reaches every role, including future ones. Use a group role to collect permissions and grant membership to the people or services that need them. Review default privileges when new tables must receive grants automatically.

Views can expose only selected columns or rows. By default, PostgreSQL checks access to underlying tables using the **view owner's** privileges. A reader may therefore query a granted view without a grant on its base table. A `security_invoker` view instead checks the reader's privileges on the base tables. When a view is meant to hide rows from untrusted SQL callers, study `security_barrier` as well. A plain filtering view is not always a safe row-security boundary.

This example needs a role administrator and a scratch PostgreSQL database. Run the whole transaction together. `ROLLBACK` removes the example objects and role.

```sql
BEGIN;

CREATE ROLE lesson_view_reader NOLOGIN;
CREATE SCHEMA lesson_access;
CREATE TABLE lesson_access.orders (
    order_id INTEGER PRIMARY KEY,
    customer_email TEXT NOT NULL,
    total NUMERIC(10, 2) NOT NULL
);
INSERT INTO lesson_access.orders VALUES (1, 'sam@example.test', 25.00);

CREATE VIEW lesson_access.order_totals AS
SELECT order_id, total FROM lesson_access.orders;

GRANT USAGE ON SCHEMA lesson_access TO lesson_view_reader;
GRANT SELECT ON lesson_access.order_totals TO lesson_view_reader;

SELECT
    has_table_privilege('lesson_view_reader',
                        'lesson_access.order_totals', 'SELECT') AS can_read_view,
    has_table_privilege('lesson_view_reader',
                        'lesson_access.orders', 'SELECT') AS can_read_table;

ROLLBACK;
```

The query returns `true` for the view and `false` for the base table, assuming no other grant gave that role base-table access. The view has no email column. The role has `NOLOGIN`, so this example checks its grants rather than connecting as it. A real login role could be made a member of it. If you change this to `security_invoker = true`, the reader would also need base-table access, which changes the design.

## Row access needs its own rule

Column grants and views do not always solve row access. PostgreSQL row-level security (RLS) adds policies to a table. When RLS is enabled and no policy allows an action, normal access is denied. A policy's `USING` condition controls which existing rows can be seen or changed. `WITH CHECK` controls which new row values can be inserted or produced by an update. Table owners normally bypass RLS unless forced to follow it. Superusers and roles with `BYPASSRLS` bypass it. Test policies as the actual application role, not only as the owner.

Many web users share one database role. In that design, `current_user` identifies the application role, not the person using the website. The application must authenticate the person, decide what they may request, and pass a trusted identity into any row policy or audit record. Never trust a tenant ID supplied only by the browser.

## Decide what the audit must prove

| Source | What it can record | Limit |
| --- | --- | --- |
| Application audit event | The signed-in user, request ID, action, and reason. | It misses writes made outside the application. |
| Database trigger | Row changes made through any writer on that table. | Its audit row normally rolls back with the transaction. |
| Database server log | Connections, errors, and statements chosen by logging settings. | A statement log is not always a clean record of committed row changes. |

Keep enough detail to answer who, what, and when, but avoid copying passwords, tokens, or private values into logs. Protect audit storage from the same role whose actions it records. Set retention and check that logs are collected. For an audit that must survive a failed transaction, use a separate reliable channel; a trigger in the same transaction cannot provide that guarantee. An external audit system needs its own failure and retry plan.

## Try it yourself

1. Why can the reader query the example view but not the table?
2. What changes when a view uses `security_invoker`?
3. Why is `current_user` often insufficient to identify a website customer?
4. Which audit source would show a direct database write that bypassed the application?

## References

- [PostgreSQL privileges](https://www.postgresql.org/docs/current/ddl-priv.html)
- [PostgreSQL CREATE VIEW](https://www.postgresql.org/docs/current/sql-createview.html)
- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [PostgreSQL server logging](https://www.postgresql.org/docs/current/runtime-config-logging.html)
- [PostgreSQL privilege inquiry functions](https://www.postgresql.org/docs/current/functions-info.html)
