# JSON in SQL

JSON stores objects, arrays, strings, numbers, booleans, and `null` in one value. In PostgreSQL, a row can have normal columns such as `product_id` and a JSON column for details that vary by product. You can read and search inside the JSON with SQL.

## Start with one document

```sql
SELECT '{"name":"Desk lamp","price":25,"tags":["home","light"],"active":true}'::jsonb AS product;
```

The result is one JSON object. The cast checks that the input is valid JSON. Text inside JSON needs double quotes. The number `25` and boolean `true` are JSON values, not strings.

PostgreSQL has `json` and `jsonb`. `json` keeps the original input text, including whitespace and object key order. `jsonb` stores a parsed form that is usually faster to search and can use GIN indexes. It does not keep object key order or duplicate keys. For duplicate keys, `jsonb` keeps the last value. Use `jsonb` for most searchable documents. Choose `json` when preserving the original text matters.

## Keep the right data in columns

```sql
CREATE TEMP TABLE products (
  product_id integer PRIMARY KEY,
  sku text NOT NULL UNIQUE,
  details jsonb NOT NULL DEFAULT '{}'::jsonb,
  CHECK (jsonb_typeof(details) = 'object')
);

INSERT INTO products (product_id, sku, details)
VALUES (1, 'LAMP-1', '{"name":"Desk lamp","color":"blue"}'::jsonb);

SELECT product_id, sku, details ->> 'name' AS name
FROM products;
```

This returns product `1`, SKU `LAMP-1`, and name `Desk lamp`. The primary key and SKU have database constraints because every product must follow those rules. The JSON object holds attributes that can vary. A field that every query joins or filters on may be better as a normal column. Storing everything in one document can make constraints, joins, and updates harder.

SQL `NULL` means there is no SQL value. JSON `null` is a value inside a JSON document. A missing key is different again. The `->` operator returns a JSON value, while `->>` returns text. For a missing key, either extraction gives SQL `NULL`. For a key whose JSON value is `null`, `->` gives JSON `null` and `->>` gives SQL `NULL`. Check key presence when that difference matters.

## Check your understanding

1. Why is `sku` a separate column in this example?
2. What does `jsonb` do with two `name` keys in one object?
3. How can a JSON `null` differ from a missing key?

## Further reading

- [PostgreSQL JSON types](https://www.postgresql.org/docs/current/datatype-json.html)
- [PostgreSQL JSON operators](https://www.postgresql.org/docs/current/functions-json.html)
