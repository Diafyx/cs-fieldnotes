# JSON Read / Query Commands

PostgreSQL has operators for reading a JSON field, following a path, and testing whether a document contains a smaller document. The operator you choose changes the type of the result. Decide whether you need JSON, text, or a true or false answer.

## Read fields and paths

```sql
WITH products(product_id, details) AS (
  VALUES
    (1, '{"name":"Lamp","specs":{"color":"blue"},"stock":5}'::jsonb),
    (2, '{"name":"Mug","specs":{"color":null},"stock":0}'::jsonb),
    (3, '{"name":"Bag","specs":{},"stock":3}'::jsonb)
)
SELECT product_id,
       details -> 'name' AS json_name,
       details ->> 'name' AS text_name,
       details #>> '{specs,color}' AS color,
       (details ->> 'stock')::integer AS stock
FROM products
ORDER BY product_id;
```

`->` returns a JSON value, so the first name has JSON quotes. `->>` returns SQL text, so the second name does not. `#>>` follows a path and returns text. Products 2 and 3 both show SQL `NULL` for `color`: one has JSON `null`, and the other has no color key. The stock cast gives integers `5`, `0`, and `3`.

## Search without losing the structure

```sql
WITH products(product_id, details) AS (
  VALUES
    (1, '{"name":"Lamp","specs":{"color":"blue"},"stock":5}'::jsonb),
    (2, '{"name":"Mug","specs":{"color":null},"stock":0}'::jsonb),
    (3, '{"name":"Bag","specs":{},"stock":3}'::jsonb)
)
SELECT product_id
FROM products
WHERE details @> '{"specs":{"color":"blue"}}'::jsonb
ORDER BY product_id;
```

This returns product `1`. `@>` asks whether the left JSON value contains the right JSON structure. The nested `specs` key matters. A search for just `{"color":"blue"}` would not match because `color` is not at the top level.

The `?` operator checks whether a text key exists at the top level of an object. `details ? 'name'` is true for all three products. To tell a missing nested key from JSON `null`, test `(details -> 'specs') ? 'color'`. It is true for product 2 and false for product 3. A missing path with `->`, `->>`, `#>`, or `#>>` returns SQL `NULL` rather than an error. A cast such as `(details ->> 'stock')::integer` can still fail if the stored text is not an integer.

## Check your understanding

1. Why does `-> 'name'` look different from `->> 'name'`?
2. Why does the containment query need the `specs` level?
3. How can you tell product 2's color from product 3's missing color?

## Further reading

- [PostgreSQL JSON operators](https://www.postgresql.org/docs/current/functions-json.html)
- [PostgreSQL JSON containment](https://www.postgresql.org/docs/current/datatype-json.html)
