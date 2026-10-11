# ALTER USER

In PostgreSQL, `ALTER USER` is another name for `ALTER ROLE`. It changes a role's attributes or session defaults. It does not grant access to a table and it does not change role memberships.

Assume a login role named `app_reader` already exists. An administrator can limit its connections and set a default statement timeout:

```sql
ALTER USER app_reader CONNECTION LIMIT 10;
ALTER USER app_reader SET statement_timeout = '5s';
```

The connection limit applies to that role's logins. The timeout becomes a session default when the role starts a new session. Existing sessions do not pick up a new role default just because this command ran. A statement that passes the timeout may be cancelled, so the application still needs to handle the error and end any failed transaction.

## Change login ability or membership

`ALTER USER app_reader NOLOGIN;` stops the role from being used for new logins. Its object privileges and memberships are separate. Use `GRANT group_role TO app_reader` or `REVOKE group_role FROM app_reader` to change membership; `ALTER USER` does not do that.

Some attributes, such as `SUPERUSER` or `CREATEROLE`, have broad effects and require an administrator with the right authority. A normal application role should receive only the attributes it needs.

Avoid putting a real password directly into a saved SQL file or command history. PostgreSQL's `psql` tool has `\password`, which prompts for a new password without leaving its clear text in the command history. Use the password process required by the environment where the database runs.

## Check your understanding

1. Does `ALTER USER` grant `SELECT` on a table?
2. When does a new role-level `statement_timeout` setting take effect?
3. Which commands change membership in another role?

## Further reading

- [PostgreSQL ALTER USER](https://www.postgresql.org/docs/current/sql-alteruser.html)
- [PostgreSQL ALTER ROLE](https://www.postgresql.org/docs/current/sql-alterrole.html)
