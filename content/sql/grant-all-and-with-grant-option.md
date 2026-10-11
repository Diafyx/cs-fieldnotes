# GRANT ALL and WITH GRANT OPTION

`GRANT ALL PRIVILEGES` gives every grantable privilege for the named kind of object. `WITH GRANT OPTION` lets the recipient pass those privileges to other roles. These two choices can give a role much more control than a simple read grant.

Assume `app.orders` and role `team_lead` exist:

```sql
GRANT ALL PRIVILEGES ON TABLE app.orders
TO team_lead WITH GRANT OPTION;
```

For this table, `team_lead` receives the available table privileges and may grant them onward. This is not the same as owning the table or becoming a database superuser. The right to change a table's definition or drop it belongs to its owner or another role with the needed ownership path, not to a table `GRANT ALL` alone. The role may still need schema `USAGE` to use the table.

## Grant narrowly when that fits

For a reporting role, this is easier to control:

```sql
GRANT SELECT ON TABLE app.orders TO team_lead;
```

The second command adds `SELECT`; it does not take away privileges already granted by the first. To reduce access, use `REVOKE` and check for other grants or memberships. `WITH GRANT OPTION` is separate from role membership's `ADMIN OPTION`, which controls whether a role can grant membership to others.

If a role has granted a privilege onward, revoking its grant option can affect those later grants. PostgreSQL may reject the revoke because of dependent grants unless `CASCADE` is chosen. Review those dependencies before changing a shared permission.

## Check your understanding

1. Does table `GRANT ALL` make `team_lead` the table owner?
2. What extra ability does `WITH GRANT OPTION` give?
3. Does the narrower second grant cancel the broad first grant?

## Further reading

- [PostgreSQL GRANT](https://www.postgresql.org/docs/current/sql-grant.html)
- [PostgreSQL REVOKE](https://www.postgresql.org/docs/current/sql-revoke.html)
