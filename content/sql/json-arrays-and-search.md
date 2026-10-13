# JSON Arrays and Search

JSON arrays keep an order and can hold several values under one key. PostgreSQL can test whether an array contains a value, expand its elements into rows, or search nested objects with a JSON path. A JSON array is different from a PostgreSQL SQL array, even though both can hold several items.

## Find products by tag

```sql
WITH products(product_id, details) AS (
  VALUES
    (1, '{"tags":["home","light"],"offers":[{"qty":1},{"qty":3}]}'::jsonb),
    (2, '{"tags":[],"offers":[]}'::jsonb),
    (3, '{"tags":["travel"],"offers":[{"qty":2}]}'::jsonb)
)
SELECT product_id
FROM products
WHERE details @> '{"tags":["home"]}'::jsonb
ORDER BY product_id;
```

Only product `1` matches. For `jsonb` containment, array order does not matter. Repeated values in the search array do not demand repeated copies in the stored array. The shorter document still has to match the same nesting: `details ? 'home'` would not search inside `tags` because `?` looks only at the top level.

## Turn array values into rows

```sql
WITH products(product_id, details) AS (
  VALUES (1, '{"tags":["home","light"]}'::jsonb),
         (2, '{"tags":[]}'::jsonb)
)
SELECT p.product_id, tag.value AS tag
FROM products AS p
CROSS JOIN LATERAL jsonb_array_elements_text(p.details -> 'tags') AS tag(value)
ORDER BY p.product_id, tag.value;
```

The result is `(1, home)` and `(1, light)`. Product 2 has an empty array, so it produces no tag rows. `CROSS JOIN LATERAL` runs the function for each product. Use a left lateral join when products without tags must still appear. The input must be a JSON array; a scalar under `tags` is a data error for this query.

## Search objects inside an array

```sql
WITH products(product_id, details) AS (
  VALUES
    (1, '{"offers":[{"qty":1},{"qty":3}]}'::jsonb),
    (2, '{"offers":[]}'::jsonb),
    (3, '{"offers":[{"qty":2}]}'::jsonb)
)
SELECT product_id
FROM products
WHERE details @? '$.offers[*] ? (@.qty >= 2)'
ORDER BY product_id;
```

Products `1` and `3` match. The path looks at each offer and asks whether its quantity is at least 2. The `@?` operator returns true when the path finds a match. It suppresses some missing-field and wrong-type errors, which helps with mixed documents but can also hide bad input. Set a clear document shape when the data should be consistent.

## Check your understanding

1. Why does `details ? 'home'` not find product 1?
2. Why is product 2 absent after `CROSS JOIN LATERAL`?
3. What does `[*]` mean in the JSON path?

## Further reading

- [PostgreSQL JSON array functions and paths](https://www.postgresql.org/docs/current/functions-json.html)
- [PostgreSQL JSON containment](https://www.postgresql.org/docs/current/datatype-json.html)
