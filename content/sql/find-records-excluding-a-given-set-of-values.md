# Find Records Excluding a Given Set of Values

This practice question removes a short list of category IDs. `NOT IN` states the rule in one place, but a missing category needs its own decision.

## The question

Return products whose `category_id` is not 2, 4, or 7. Keep products with no category so they can be reviewed. Sort by `product_id`.

```sql
CREATE TEMP TABLE products_for_review (
  product_id integer PRIMARY KEY,
  category_id integer
);

INSERT INTO products_for_review (product_id, category_id) VALUES
  (10, 1),
  (11, 2),
  (12, 4),
  (13, 5),
  (14, 7),
  (15, NULL);
```

## A solution

```sql
SELECT product_id, category_id
FROM products_for_review
WHERE category_id NOT IN (2, 4, 7)
   OR category_id IS NULL
ORDER BY product_id;
```

The output contains products 10, 13, and 15. Product 15 appears because the question explicitly keeps missing categories. Without `OR category_id IS NULL`, `NOT IN` would not keep it.

Do not put `NULL` inside the excluded list. `category_id NOT IN (2, 4, 7, NULL)` is unknown for every category that does not match 2, 4, or 7, so those rows disappear from a `WHERE` result. If the excluded values come from another table and that table can contain `NULL`, use a `NOT EXISTS` query or remove missing values from the subquery on purpose.

## Check your understanding

1. Why is product 15 included here?
2. What would happen if the `OR` line were removed?
3. Why is `NOT IN (2, 4, 7, NULL)` unsafe for this question?

## Further reading

- [PostgreSQL IN and NOT IN](https://www.postgresql.org/docs/current/functions-comparisons.html)
- [PostgreSQL NULL comparisons](https://www.postgresql.org/docs/current/functions-comparison.html)
