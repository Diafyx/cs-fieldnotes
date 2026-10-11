# Creating and Managing Tables in SQL

Table definitions are rules about data. Before creating a table, decide what one row means, which values are required, how rows are identified, and how the table relates to others. A `CREATE TABLE` statement records those decisions where every client must follow them.

## Create a useful table

```sql
CREATE TABLE products (
    product_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku text NOT NULL UNIQUE,
    name text NOT NULL,
    price numeric(10, 2) NOT NULL CHECK (price >= 0),
    active boolean NOT NULL DEFAULT true
);
```

One row represents one product. `product_id` is its generated identity. `sku` must be unique. `name` and `price` are required. The check blocks a negative price. `active` gets a default value when an insert does not provide one.

These rules do not cover every business decision. For example, `sku text NOT NULL UNIQUE` still allows a blank string unless you add a rule that rejects it. Decide whether a blank SKU is meaningful.

## Insert data and name your columns

```sql
INSERT INTO products (sku, name, price)
VALUES ('P-100', 'Notebook', 4.50);
```

Naming the columns makes the statement readable and protects it from changes to the table's column order. The database supplies the generated ID and the `active` default. If you omit a required column without a default, the insert fails.

## Change a table carefully

`ALTER TABLE` changes a table definition. For example:

```sql
ALTER TABLE products ADD COLUMN description text;
```

Existing rows receive `NULL` for the new column unless another rule or default applies. If you later want `description` to be required, fill missing values first, then add `NOT NULL`. Adding a constraint to an existing table may fail if old rows violate it. A schema change in a busy production system can also need careful planning because it may lock data or take time to validate.

```sql
UPDATE products
SET description = name
WHERE description IS NULL;

ALTER TABLE products ALTER COLUMN description SET NOT NULL;
```

The update above uses the product name only as a simple practice value. A real description should be written for the product. The point is to repair old rows before enforcing a new required-value rule.

## Keep changes reviewable

Save schema changes in versioned migration files when building an application. That lets teammates and deployments apply the same change in the same order. Review the rows a data migration will touch, test it on a copy when possible, and keep a backup plan for important data. `DROP TABLE` removes a table and its data, so treat it as a deliberate operation.

## Check your understanding

1. Which rule prevents two products from using the same SKU?
2. Why can adding `NOT NULL` fail on a table that already contains rows?
3. What happens when an insert omits `active`? What happens when it omits `name`?

## Further reading

- [PostgreSQL CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/ddl-alter.html)
- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
