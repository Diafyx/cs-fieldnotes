# GRANTS

`GRANT` gives a role a named privilege on a database object, or gives it membership in another role. Name the object and the action. A grant on one table does not automatically cover every table in its schema.

## Grant specific table access

Assume `app.orders` and role `report_reader` exist, and run these as the object owner or another role allowed to grant access:

```sql
GRANT USAGE ON SCHEMA app TO report_reader;
GRANT SELECT ON TABLE app.orders TO report_reader;
```

The role can look up objects in `app` and read `app.orders`. It cannot insert into that table from these grants. PostgreSQL also supports column grants, such as `GRANT SELECT (order_id, total) ON TABLE app.orders TO report_reader;`, when only named columns should be readable.

## Other objects need their own access

`CONNECT` applies to a database. `USAGE` and `CREATE` apply to a schema. A table may receive `SELECT`, `INSERT`, `UPDATE`, `DELETE`, and other table privileges. A sequence can require `USAGE` or another sequence privilege. A function can require `EXECUTE`. A role can be given membership with `GRANT report_readers TO analyst;`.

`GRANT SELECT ON ALL TABLES IN SCHEMA app TO report_reader;` covers tables that exist in that schema at the time of the command. To control grants on tables created later, use `ALTER DEFAULT PRIVILEGES` for the role that will create them. That command does not change existing objects.

The keyword `PUBLIC` means every current and future role. A grant to `PUBLIC` can make data available more widely than a named-role grant. Check existing grants and memberships before deciding what a role can actually do.

## Check your understanding

1. Why can a table grant still fail without schema access?
2. Does `GRANT SELECT ON ALL TABLES IN SCHEMA app` cover future tables?
3. What does `PUBLIC` mean in a grant?

## Further reading

- [PostgreSQL GRANT](https://www.postgresql.org/docs/current/sql-grant.html)
- [PostgreSQL ALTER DEFAULT PRIVILEGES](https://www.postgresql.org/docs/current/sql-alterdefaultprivileges.html)
