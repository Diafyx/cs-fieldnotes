# Performance and Indexing

JSONB makes flexible documents searchable, but a search across many rows can be slow. An index helps only when it matches the operator and expression in the query. Start with the queries you actually run, then check their plans on realistic data.

## Index containment searches

```sql
CREATE TEMP TABLE search_products (
  product_id integer PRIMARY KEY,
  details jsonb NOT NULL
);

INSERT INTO search_products (product_id, details) VALUES
  (1, '{"sku":"LAMP-1","tags":["home","light"]}'::jsonb),
  (2, '{"sku":"MUG-1","tags":["home"]}'::jsonb),
  (3, '{"sku":"BAG-1","tags":["travel"]}'::jsonb);

CREATE INDEX search_products_details_gin
ON search_products USING GIN (details);

SELECT product_id
FROM search_products
WHERE details @> '{"tags":["home"]}'::jsonb
ORDER BY product_id;
```

The query returns products `1` and `2`. The default JSONB GIN index can support containment (`@>`), top-level key existence (`?`), and JSON path searches (`@?` and `@@`). On three rows, PostgreSQL may still choose a table scan because that can be cheaper. Creating an index does not force its use.

## Index one extracted value

```sql
CREATE INDEX search_products_sku_idx
ON search_products ((details ->> 'sku'));

SELECT product_id
FROM search_products
WHERE details ->> 'sku' = 'MUG-1';
```

This returns product `2`. A B-tree expression index fits equality on the extracted SKU. If SKU is always required and unique, a normal `sku` column with a unique constraint is usually clearer and can enforce that rule. A GIN index on the whole document does not automatically replace an expression index for `details ->> 'sku' = ...`.

PostgreSQL also has the `jsonb_path_ops` GIN operator class. It supports `@>`, `@?`, and `@@`, and can be smaller or more selective for those searches. It does not support `?`, `?|`, or `?&`. Choose it only after checking which operators the workload uses. Whole-document GIN indexes can take space and add work to inserts and updates. A targeted expression index may be better for a frequent path.

Run `EXPLAIN (ANALYZE, BUFFERS)` on a test or safe production query when you need to measure the chosen plan; `ANALYZE` runs the query. Check row counts, actual time, and buffer reads. Refresh table statistics after large loads. For a small table, a sequential scan can be the right choice.

## Check your understanding

1. Why might the first query scan this three-row table even with a GIN index?
2. Which index matches the extracted SKU equality query?
3. What operator would rule out `jsonb_path_ops` if it is needed often?

## Further reading

- [PostgreSQL JSONB indexing](https://www.postgresql.org/docs/current/datatype-json.html)
- [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
