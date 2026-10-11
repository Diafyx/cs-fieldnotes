# INSERT

`INSERT` adds rows to a table. Name the target columns so each value has a clear place and adding a column later does not silently change what your statement means.

## Add one or more rows

```sql
CREATE TABLE products (
  product_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name text NOT NULL,
  price numeric(10, 2) NOT NULL CHECK (price >= 0),
  active boolean NOT NULL DEFAULT true
);

INSERT INTO products (name, price)
VALUES ('Notebook', 12.50),
       ('Pen', 1.25)
RETURNING product_id, name, active;
```

This adds two rows. PostgreSQL makes each `product_id` from the identity column and sets `active` to `true`. `RETURNING` shows the actual IDs and values assigned. Do not guess the next generated ID: other writes and sequence gaps can change it.

The order of named columns can differ from table order, but each row of `VALUES` must supply a matching value for each named column. A missing column receives its default, or `NULL` when no default exists. `NOT NULL` can reject that `NULL`; the price check rejects a negative price. An insert that violates a constraint fails instead of adding an invalid row.

## Insert rows from a query

Assume `archived_products` has `name` and `price` columns with compatible types:

```sql
INSERT INTO archived_products (name, price)
SELECT name, price
FROM products
WHERE active = false;
```

Here the `SELECT` supplies zero or more rows. The two selected expressions must fit the two target columns. Think about duplicate rows before running a copy twice. A unique constraint or a clear rule for which rows have already moved can prevent unwanted repeats.

## Handle duplicates on purpose

If a unique key already exists, an ordinary `INSERT` raises an error. PostgreSQL's `ON CONFLICT` can skip the new row or update the existing row. That choice belongs to the business rule, not to the database automatically. See [UPSERT](/topics/sql/upsert.html) for an example.

Use parameters when values come from Python or Java. Building SQL by joining user text into a string can change the statement and expose the data. Parameters also handle quotes in names such as `O'Brien` correctly.

## Check your understanding

1. Why is the generated ID returned instead of predicted?
2. What happens if `price` is omitted from this insert?
3. What can happen if the archive copy is run twice?

## Further reading

- [PostgreSQL INSERT](https://www.postgresql.org/docs/current/sql-insert.html)
- [PostgreSQL identity columns](https://www.postgresql.org/docs/current/ddl-identity-columns.html)
