# WHERE

`WHERE` keeps source rows whose condition is true. It applies before grouping in the logical reading of a `SELECT` query. Use it to narrow a query to the rows that answer your question, not as a way to repair a join that produced unexpected rows.

## A basic filter

```sql
SELECT order_id, amount
FROM orders
WHERE status = 'paid';
```

Only rows with `status = 'paid'` are returned. The string uses single quotes because it is a value. A column name does not use single quotes. If `status` is `NULL`, the comparison is unknown, so that row is not returned.

## Combine conditions carefully

```sql
SELECT order_id, amount
FROM orders
WHERE status = 'paid'
  AND amount >= 50;
```

Both conditions must be true. With `OR`, either condition can be true. Parentheses make mixed conditions clear:

```sql
SELECT order_id, amount
FROM orders
WHERE status = 'paid'
  AND (amount >= 50 OR customer_id = 10);
```

Without parentheses, SQL operator precedence might produce a result you did not intend. Write the grouping explicitly when it matters.

## Ranges and missing values

For dates and timestamps, a half-open range is often safer than trying to include the last possible instant of a day:

```sql
SELECT order_id
FROM orders
WHERE placed_at >= '2026-01-01'
  AND placed_at < '2026-02-01';
```

This includes all of January for timestamps interpreted in the same chosen time zone. Decide which time zone the date boundaries mean before using this query in an application.

Use `IS NULL` and `IS NOT NULL` for missing values:

```sql
SELECT order_id
FROM orders
WHERE shipped_at IS NULL;
```

`shipped_at = NULL` does not test for missing values. A comparison with `NULL` produces unknown.

## Values from Python or Java

When a value comes from a user or another system, pass it as a query parameter. Do not build `WHERE customer_id = ...` by joining raw input into a SQL string. Python database drivers and Java prepared statements use different placeholder syntax, but both keep the value separate from SQL code.

## Check your understanding

1. What rows does `WHERE status = 'paid' AND amount >= 50` keep?
2. Why does `WHERE shipped_at = NULL` fail to find unshipped orders?
3. What time zone does a date boundary use when `placed_at` is `timestamptz`?

## Further reading

- [PostgreSQL WHERE clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-WHERE)
- [PostgreSQL comparison operators](https://www.postgresql.org/docs/current/functions-comparison.html)
- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
