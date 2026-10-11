# REVOKE

`REVOKE` takes away a privilege granted on an object, or removes membership in a role. It changes a named grant. The recipient may still have the same effective access through another role, through `PUBLIC`, or through ownership.

Assume `app.orders` and role `app_writer` exist:

```sql
REVOKE INSERT, UPDATE, DELETE ON TABLE app.orders
FROM app_writer;
```

This removes those table privileges granted to `app_writer` by the acting grantor. It does not remove `SELECT` unless that is also named. If `app_writer` inherits write access from another role, this command alone will not make it read-only.

## Revoke a grant option

```sql
REVOKE GRANT OPTION FOR SELECT ON TABLE app.orders
FROM team_lead RESTRICT;
```

This removes the ability to grant `SELECT` onward while leaving `team_lead`'s own `SELECT` privilege. If other roles depend on a grant made by `team_lead`, `RESTRICT` makes the command fail. `CASCADE` would also remove grants that depend on the revoked path. Check the grant chain before choosing it.

Membership is removed with a different form, such as `REVOKE report_readers FROM analyst;`. Before and after a revoke, test the intended action as the affected role in a safe database. A role can get the same privilege from several sources, so reading one grant statement is not enough to know its effective access.

## Check your understanding

1. Why might `app_writer` still be able to update after the first command?
2. Does `REVOKE GRANT OPTION FOR SELECT` remove the role's own `SELECT` privilege?
3. What can `CASCADE` remove beyond the named role's grant?

## Further reading

- [PostgreSQL REVOKE](https://www.postgresql.org/docs/current/sql-revoke.html)
- [PostgreSQL privileges](https://www.postgresql.org/docs/current/ddl-priv.html)
