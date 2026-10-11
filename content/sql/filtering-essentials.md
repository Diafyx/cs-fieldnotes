# Filtering Essentials

Filtering means keeping only rows that answer a question. In a basic `SELECT`, put row conditions in `WHERE`. A good filter names the column, the rule, and what should happen when the value is missing.

## Build the rule from the question

Suppose you need paid orders placed in January 2026. The table has `status` and `placed_at`:

```sql
SELECT order_id, customer_id, placed_at
FROM orders
WHERE status = 'paid'
  AND placed_at >= TIMESTAMPTZ '2026-01-01 00:00:00+00'
  AND placed_at < TIMESTAMPTZ '2026-02-01 00:00:00+00';
```

This includes the start of January and excludes the start of February. The example uses UTC. If your business uses another time zone, choose boundaries in that zone before writing the filter. A row with `status = NULL` does not pass the status check.

## Common kinds of filters

- Use `=`, `<>`, `<`, and related operators for comparisons.
- Use `AND`, `OR`, `NOT`, and parentheses to combine rules.
- Use `IS NULL` for missing values.
- Use `IN` for a short list of allowed values.
- Use `BETWEEN` when both ends of a range should count.
- Use `LIKE` for simple text patterns.

Choose the operator that states the rule directly. For example, `status IN ('paid', 'shipped')` is easier to read than two equality tests joined by `OR`.

## What exclusion really means

```sql
SELECT order_id
FROM orders
WHERE status <> 'cancelled';
```

This excludes both cancelled orders and orders with a missing status. If you want missing status included, write:

```sql
WHERE status IS DISTINCT FROM 'cancelled'
```

The choice depends on what missing status means in your data. Do not make it by accident.

## Filtering rows and filtering groups

`WHERE` filters individual rows. `HAVING` filters groups after aggregation. If the question is "customers with at least three paid orders," filter paid orders with `WHERE`, group by customer, then use `HAVING COUNT(*) >= 3`.

## Filters in application code

Pass user values as SQL parameters in Python or Java. This keeps the value separate from the SQL text. It also handles quotes in strings correctly. For a date range, pass the start and end values as parameters with explicit time zone rules.

## Check your understanding

1. Why does the January query use `<` for the February boundary?
2. Should a missing status count as "not cancelled" for your system?
3. Which clause filters orders, and which clause filters customers after grouping?

## Further reading

- [PostgreSQL WHERE clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-WHERE)
- [PostgreSQL comparison operators](https://www.postgresql.org/docs/current/functions-comparison.html)
- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
