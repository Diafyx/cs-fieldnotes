# Dummy Data Setup

Small test data should make the behavior of a query clear. This table has three products: one with two tags, one with no tags, and one with a JSON `null` color. Those cases make later searches and null checks easier to test.

## Create a small PostgreSQL table

```sql
CREATE TEMP TABLE demo_products (
  product_id integer PRIMARY KEY,
  sku text NOT NULL UNIQUE,
  details jsonb NOT NULL,
  CHECK (jsonb_typeof(details) = 'object')
);

INSERT INTO demo_products (product_id, sku, details) VALUES
  (1, 'LAMP-1', '{"name":"Desk lamp","color":"blue","tags":["home","light"]}'::jsonb),
  (2, 'MUG-1',  '{"name":"Mug","color":"white","tags":[]}'::jsonb),
  (3, 'BAG-1',  '{"name":"Bag","color":null,"tags":["travel"]}'::jsonb);

SELECT product_id, sku, details ->> 'name' AS name
FROM demo_products
ORDER BY product_id;
```

The final query returns `(1, LAMP-1, Desk lamp)`, `(2, MUG-1, Mug)`, and `(3, BAG-1, Bag)`. Run the code in order in one database session. A temporary table belongs to that session and goes away when it ends. Use a normal table when you need the rows to remain for later sessions.

## Why this setup is useful

The primary key prevents repeated IDs. The unique constraint prevents repeated SKUs. `jsonb NOT NULL` stops SQL `NULL` in the whole document. The `CHECK` requires a JSON object; a valid JSON array such as `[]` would fail it. These constraints do not require every object to have a `name` or `tags` key. Add more checks or normal columns if those are business rules.

Keep an explicit column list in `INSERT`. It protects the data load when someone later adds a column to the table. The `::jsonb` cast also checks each JSON literal while loading. Invalid JSON makes the statement fail instead of silently storing broken text.

To rerun this setup in the same session, create a new session or remove the old temporary table first. The `CREATE TEMP TABLE` statement will fail if the table already exists. Avoid using real customer data for examples; invented rows make a test safe to share.

## Check your understanding

1. Why does the `CHECK` reject `[]` even though it is valid JSON?
2. Is product 3's `color` the same as a missing `color` key?
3. Which constraint stops two rows from using `MUG-1`?

## Further reading

- [PostgreSQL JSON types](https://www.postgresql.org/docs/current/datatype-json.html)
- [PostgreSQL CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
