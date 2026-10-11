# ALTER

`ALTER TABLE` changes a table's definition. It can add or rename a column, change a column's type, add a constraint, or remove a column. These changes affect the shape and rules of future reads and writes, so plan them with the code that uses the table.

## Add a column

```sql
ALTER TABLE products
ADD COLUMN active boolean NOT NULL DEFAULT true;
```

This adds `active` and gives existing rows a value of `true` when read. New rows also get `true` unless an insert supplies another value. A default does not force every future row to stay `true`.

## Rename or change a column

```sql
ALTER TABLE products
RENAME COLUMN name TO product_name;

ALTER TABLE products
ALTER COLUMN price TYPE numeric(12, 2);
```

The rename does not remove the stored names, but queries that still use `name` need updating. The type change allows a larger price range. Other type changes can fail when old values cannot be converted. PostgreSQL can use `USING` to state how old values should be changed during a type change.

## Add a rule to existing data

```sql
ALTER TABLE products
ADD CONSTRAINT products_price_nonnegative CHECK (price >= 0);
```

PostgreSQL checks existing rows when adding an ordinary enforced `CHECK` constraint. The command fails if a stored price breaks the new rule. On a large table, `ADD CONSTRAINT ... NOT VALID` followed later by `VALIDATE CONSTRAINT` can separate adding the rule for new writes from checking older rows. That needs a migration plan because old bad rows remain until fixed and validated.

## Change defaults or remove a column

```sql
ALTER TABLE products
ALTER COLUMN active DROP DEFAULT;
```

Existing `active` values stay as they are. New inserts must now supply `active` because the column is still `NOT NULL`. A default is a rule for missing input on future writes, not a stored value that this command erases from old rows. `ALTER COLUMN active SET DEFAULT false` would set a new default for future writes.

`ALTER TABLE products DROP COLUMN old_code;` removes `old_code` from the table definition. Before doing that, find every query, view, constraint, and application path that uses the column. A column rename or removal can break running code even if the database change itself succeeds.

Some `ALTER TABLE` actions need a strong table lock or a table rewrite. A change that is quick on an empty table may take time and block queries on a large one. Check the exact action and table size before running a production migration. PostgreSQL can roll back most table changes inside a transaction, but a later application release may already depend on the new schema. Plan the application and database change together.

Dropping a column removes it from queries and can affect indexes, constraints, or dependent views. Do not use `CASCADE` without checking exactly what else it would remove.

## Check your understanding

1. Does a default value prevent an insert from supplying `false` for `active`?
2. What must happen to queries that still use `products.name` after the rename?
3. Why might a new constraint fail on a table that already contains rows?

## Further reading

- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- [PostgreSQL table constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
