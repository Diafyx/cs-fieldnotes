# Primary Key

A primary key identifies one row in a table. Its value must be unique and cannot be `NULL`. A table may have many unique rules, but it can declare only one primary key. In PostgreSQL, declaring a primary key also creates a unique B-tree index for the key columns.

Think of the key as the row's identity. A person's name is a poor key because names can repeat and change. A stable customer ID is often easier to use.

## One-column key

```sql
CREATE TABLE customers (
    customer_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    email text UNIQUE
);
```

The database generates `customer_id`. `email` is separately marked `UNIQUE`, but it is not the primary key. If an email address changes, the customer's identity does not have to change. A unique constraint on a nullable email column may still allow more than one missing value in PostgreSQL, so decide whether email is required and add `NOT NULL` if it is.

## A key can have several columns

A membership table may represent one user joining one team. The pair, rather than either value alone, identifies a row:

```sql
CREATE TABLE team_memberships (
    team_id bigint NOT NULL,
    user_id bigint NOT NULL,
    joined_at timestamptz NOT NULL,
    PRIMARY KEY (team_id, user_id)
);
```

This allows one user in many teams and many users in one team. It prevents the same user from appearing twice in the same team. The order of key columns can matter for index use, so choose it with the queries you expect in mind.

## Natural and generated keys

A natural key comes from the domain, such as a stable external code. A generated key is created for the table, such as an identity number. Neither is always right. Use a natural key when its uniqueness and stability are part of the real rules. Use a generated key when the visible value may change or has awkward size or structure.

Even with a generated primary key, keep other real uniqueness rules. If each user can have only one account for a particular service, a `UNIQUE` constraint on the right columns may still be needed. A primary key does not protect every business rule.

## Common mistakes

- Treating row position as identity. SQL tables have no stable row number unless you store one.
- Using a mutable label as a key without considering what happens when it changes.
- Assuming a primary key makes every query fast. It helps lookups that use its index, but other queries may need different indexes.

## Check your understanding

1. Why would a customer's email be a risky primary key?
2. What does `PRIMARY KEY (team_id, user_id)` allow and forbid?
3. If a table has a generated ID, which other uniqueness rules might still be needed?

## Further reading

- [PostgreSQL primary keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS)
- [PostgreSQL identity columns](https://www.postgresql.org/docs/current/ddl-identity-columns.html)
