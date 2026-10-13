# JSON Insertion + Data Loading

PostgreSQL can insert a JSON document directly, build one from typed SQL values, or turn a JSON array of objects into rows. Choose the form that matches the input. In all three cases, write down which fields are required.

## Insert and build documents

```sql
CREATE TEMP TABLE import_products (
  product_id integer PRIMARY KEY,
  sku text NOT NULL UNIQUE,
  details jsonb NOT NULL
);

INSERT INTO import_products (product_id, sku, details)
VALUES (1, 'LAMP-1', '{"name":"Desk lamp","price":25}'::jsonb);

INSERT INTO import_products (product_id, sku, details)
VALUES (2, 'MUG-1', jsonb_build_object('name', 'Mug', 'price', 12));

SELECT product_id, sku, details
FROM import_products
ORDER BY product_id;
```

The first document is parsed from JSON text. The second is built from SQL values. Both contain a JSON number for `price`. `jsonb_build_object` handles quoting and escaping for string values, so it is safer than joining text fragments to make JSON.

## Load several rows from one JSON array

Run this after the table setup above:

```sql
INSERT INTO import_products (product_id, sku, details)
SELECT x.product_id, x.sku,
       jsonb_build_object('name', x.name, 'price', x.price)
FROM jsonb_to_recordset(
  '[{"product_id":3,"sku":"BAG-1","name":"Bag","price":40},
    {"product_id":4,"sku":"BOOK-1","name":"Notebook","price":6}]'::jsonb
) AS x(product_id integer, sku text, name text, price numeric);

SELECT product_id, sku, details ->> 'name' AS name
FROM import_products
ORDER BY product_id;
```

The final query now returns four products. `jsonb_to_recordset` reads each object as a row with the declared SQL column types. It does not guess those types for you. A missing field becomes SQL `NULL`; a `NOT NULL` constraint will reject it where the target column requires a value. If `price` must be present and nonnegative, add checks for that rule before relying on imported data.

When Python or Java sends JSON to the database, pass the document as a bound parameter through the database driver. Do not paste user text into SQL. A cast to `jsonb` checks JSON syntax, but it does not prove that the document follows your business rules. Validate required fields, types, and ranges as well.

## Check your understanding

1. Why is building JSON from typed values safer than joining text strings?
2. What happens if an imported object has no `sku`?
3. Why does `jsonb_to_recordset` need the `AS x(...)` column list?

## Further reading

- [PostgreSQL JSON creation and record functions](https://www.postgresql.org/docs/current/functions-json.html)
- [PostgreSQL INSERT](https://www.postgresql.org/docs/current/sql-insert.html)
