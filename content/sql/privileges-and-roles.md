# Privileges and Roles

PostgreSQL uses roles to manage access. A role with `LOGIN` can connect as a database user. A role without `LOGIN` is often used to hold permissions for a group. Roles can own objects, receive privileges, and become members of other roles.

## Put shared access in one role

Run this as an administrator in a scratch database. Assume schema `app` and table `app.orders` already exist:

```sql
CREATE ROLE report_readers NOLOGIN;
CREATE ROLE analyst LOGIN;

GRANT USAGE ON SCHEMA app TO report_readers;
GRANT SELECT ON TABLE app.orders TO report_readers;
GRANT report_readers TO analyst;
```

`analyst` can connect and, with normal inherited membership, use the read privileges of `report_readers`. The group role itself cannot log in. One membership grant is easier to maintain than repeating table grants for many people. PostgreSQL can also grant membership without automatic inheritance, so inspect membership options if access does not behave as expected.

## Know the source of a privilege

A role's effective access can come from a direct grant, an inherited role, or `PUBLIC`, which includes every role. An object's owner has special control over that object. `SUPERUSER` bypasses ordinary permission checks and should not be used as an application login. `LOGIN` alone does not give a role permission to read every table.

Database `CONNECT`, schema `USAGE`, and table `SELECT` are separate permissions. A role may need each step to reach a table. An insert that uses a sequence-generated ID may also need a sequence privilege, depending on how the ID is defined.

To check an actual role, try the intended operation while connected as that role in a test database. Review direct grants, group membership, and `PUBLIC` privileges when the result surprises you.

## Check your understanding

1. Why does `report_readers` have `NOLOGIN`?
2. Does creating `analyst LOGIN` give it read access to every table?
3. What three routes can give a role an effective object privilege?

## Further reading

- [PostgreSQL database roles](https://www.postgresql.org/docs/current/user-manag.html)
- [PostgreSQL role membership](https://www.postgresql.org/docs/current/role-membership.html)
- [PostgreSQL privileges](https://www.postgresql.org/docs/current/ddl-priv.html)
