# IS NULL vs. IS NOT NULL, IN, and NOT IN

`IS NULL` finds missing values. `IS NOT NULL` finds present ones. `IN` checks whether a value matches a member of a list or query result. `NOT IN` checks that it matches none. Their behavior with `NULL` is the part to learn carefully.

## Find missing or present values

```sql
SELECT order_id
FROM orders
WHERE shipped_at IS NULL;
```

This finds orders with no recorded shipping time. To find orders with a shipping time, use `IS NOT NULL`. `shipped_at = NULL` and `shipped_at <> NULL` do not work because ordinary comparisons with `NULL` are unknown.

An empty string, zero, and `NULL` are different. `'' IS NOT NULL` is true. If an application uses both empty strings and `NULL` to mean "missing," fix the data rule or test both values explicitly.

## Check membership with IN

```sql
SELECT order_id
FROM orders
WHERE status IN ('paid', 'shipped');
```

This is like `status = 'paid' OR status = 'shipped'`. A `NULL` status does not pass. A `NULL` inside the list can also make a nonmatching comparison unknown, though `WHERE` would discard it either way.

## Why NOT IN can surprise you

```sql
SELECT 7 NOT IN (3, NULL) AS allowed;
```

The result is `NULL`, not `true`. Seven differs from three, but SQL cannot know whether it differs from the missing list value. In a `WHERE` clause, this row is dropped. The same problem can occur when a `NOT IN` subquery returns even one `NULL`.

If the exclusion list is known and non-null, `NOT IN` is clear:

```sql
SELECT order_id
FROM orders
WHERE status NOT IN ('cancelled', 'refunded');
```

A missing `status` still does not pass. To include it, add `OR status IS NULL` and group the condition with parentheses if needed.

## Excluding values from another table

For a list from another table that may contain `NULL`, `NOT EXISTS` often states the rule more safely:

```sql
SELECT c.customer_id
FROM customers AS c
WHERE NOT EXISTS (
  SELECT 1
  FROM blocked_customers AS b
  WHERE b.customer_id = c.customer_id
);
```

This keeps a customer when no matching blocked row exists. A `NULL` in `blocked_customers.customer_id` cannot block every customer. If `c.customer_id` can itself be `NULL`, decide separately whether that row should be kept; a primary key would normally prevent it.

## Check your understanding

1. Does `NULL NOT IN (1, 2)` return true?
2. Why can one `NULL` from a subquery cause `NOT IN` to return no rows?
3. How would you include orders with missing status when excluding cancelled orders?

## Further reading

- [PostgreSQL comparison predicates](https://www.postgresql.org/docs/current/functions-comparison.html)
- [PostgreSQL IN and NOT IN](https://www.postgresql.org/docs/current/functions-comparisons.html)
- [PostgreSQL EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html)
