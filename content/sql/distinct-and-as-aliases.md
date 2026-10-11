# DISTINCT and AS (Aliases)

`DISTINCT` removes duplicate output rows. `AS` gives a result column or table a name for the query. They solve different problems: one changes which rows appear, and the other changes how we refer to a value or source.

## Remove duplicate results

Suppose `orders` has three paid orders for customer 4 and one for customer 8:

```sql
SELECT DISTINCT customer_id
FROM orders
WHERE status = 'paid';
```

This returns customer 4 once and customer 8 once. Without `DISTINCT`, customer 4 would appear three times. A `DISTINCT` query still has no guaranteed order unless it uses `ORDER BY`.

`DISTINCT` applies to the entire selected row:

```sql
SELECT DISTINCT customer_id, status
FROM orders;
```

The pair `(customer_id, status)` must be unique in the result. The same customer can appear more than once if their statuses differ. PostgreSQL treats duplicate output rows containing `NULL` as duplicates here, so repeated missing statuses do not each get their own row.

Do not add `DISTINCT` just to hide repeated rows from a join. First ask whether those rows represent real matches. If you need one row per customer with a total or count, `GROUP BY` usually states that question more clearly.

## Name output columns and tables

```sql
SELECT o.customer_id,
       o.quantity * o.unit_price AS line_total
FROM order_lines AS o;
```

The result column is named `line_total`. The table is named `o` within this query. Neither alias changes the stored schema. In PostgreSQL, once a table has an alias, refer to it by that alias in the query.

An output alias can be used in `ORDER BY`:

```sql
SELECT quantity * unit_price AS line_total
FROM order_lines
ORDER BY line_total DESC;
```

Do not rely on an output alias in the same query's `WHERE` clause. `WHERE` filters source rows before the output name is assigned. Repeat the expression, or use a subquery when repeating it would be hard to read.

## One row per group in PostgreSQL

PostgreSQL has `DISTINCT ON`, which is not standard SQL. It keeps one row for each value of the listed expression. Use `ORDER BY` to choose which row wins:

```sql
SELECT DISTINCT ON (customer_id)
       customer_id, order_id, placed_at
FROM orders
ORDER BY customer_id, placed_at DESC, order_id DESC;
```

This chooses the latest order for each customer. `order_id` breaks timestamp ties. The `DISTINCT ON` expressions must match the leftmost `ORDER BY` expressions. For portable SQL, a window function can solve the same kind of problem.

## Check your understanding

1. Can `SELECT DISTINCT customer_id, status` return one customer twice?
2. Does `AS line_total` add a column to `order_lines`?
3. What happens to a `DISTINCT ON` result if tied rows have no tie-breaker?

## Further reading

- [PostgreSQL SELECT reference](https://www.postgresql.org/docs/current/sql-select.html)
- [PostgreSQL select lists](https://www.postgresql.org/docs/current/queries-select-lists.html)
