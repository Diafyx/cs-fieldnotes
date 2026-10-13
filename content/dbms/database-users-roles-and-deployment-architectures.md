# Database Users, Roles, and Deployment Architectures

People use a database in different ways. An administrator maintains it, a developer changes its schema, an analyst reads reports, and an application reads and writes data for its users. These people and programs need different access. A database role is the identity PostgreSQL uses to grant that access. A person using a website is not automatically a separate PostgreSQL role; the website often connects through one application role.

## See the connected role

Run this in PostgreSQL:

```sql
SELECT current_user AS active_role,
       session_user AS login_role,
       current_database() AS database_name;
```

It returns one row with the active role, the login role, and the database name. The exact names depend on your connection. `current_user` can differ from `session_user` after a permitted role switch. These names identify database access, not necessarily the person using the application.

PostgreSQL roles can have `LOGIN`, own objects, receive privileges, and be members of other roles. A group role without `LOGIN` can collect privileges for several login roles. Grant an application only the reads and writes it needs. Keep schema changes, backups, and administration under separate roles. A `GRANT SELECT` on a table also needs access to its schema; application authorization still decides which website user may request which record.

For example, an owner could create a group role for report readers and grant it access. The following commands assume the `reporting` schema and `monthly_sales` table already exist, and the person running them has the needed privileges:

```sql
CREATE ROLE report_reader NOLOGIN;
GRANT USAGE ON SCHEMA reporting TO report_reader;
GRANT SELECT ON reporting.monthly_sales TO report_reader;
```

`NOLOGIN` means this role holds permissions but does not connect directly. A separate login role can be made a member of it. The example grants reading one table; it does not grant writing that table or reading every table in the schema. Practice on a disposable local PostgreSQL server. Roles are shared across databases on that server and persist after the session ends.

## Where the DBMS runs

| Arrangement | Path of a request | Common use |
| --- | --- | --- |
| Embedded database | Application calls a library that reads a local database file | Local tools, mobile apps, small single-host services |
| Client/server database | Application driver connects to a database server | Shared data used by several clients |
| Web application with database | Browser calls the application; application connects to the database | Most web services |
| Primary with replicas | Application writes to the primary; some reads can use replicas | More read capacity or standby availability |

SQLite is an embedded DBMS. PostgreSQL is usually run as a server. A managed PostgreSQL service changes who operates the server; it does not change the basic client/server request path. A replica may lag behind the primary, so a read that must see a recent write may need the primary. A replica is not a backup because it can also receive an accidental delete.

For a web service, keep the database off the public browser path. The browser should call the application, which validates the request and sends parameterized SQL using a restricted role. Keep credentials out of source code. Plan connection limits, backups, failover, and schema migrations for the chosen deployment.

## Check your understanding

1. Does every website customer need a PostgreSQL login role? Why or why not?
2. What does a managed database service change, and what does the application still do?
3. Why might a confirmation page read from the primary instead of a replica?

## Further reading

- [PostgreSQL database roles](https://www.postgresql.org/docs/current/user-manag.html)
- [PostgreSQL privileges](https://www.postgresql.org/docs/current/ddl-priv.html)
- [PostgreSQL client/server architecture](https://www.postgresql.org/docs/current/tutorial-arch.html)
- [SQLite: appropriate uses](https://www.sqlite.org/whentouse.html)
