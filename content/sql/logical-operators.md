# Logical Operators

Logical operators combine conditions. `AND` needs both conditions to be true. `OR` needs at least one. `NOT` reverses true and false. SQL also has an unknown result, shown as `NULL`, when a condition depends on a missing value.

## Combine conditions

```sql
SELECT order_id
FROM orders
WHERE status = 'paid'
  AND (amount >= 100 OR customer_id = 7);
```

An order must be paid. It must also cost at least 100 or belong to customer 7. The parentheses state exactly what the `OR` applies to.

`NOT` reverses a condition:

```sql
SELECT order_id
FROM orders
WHERE NOT (status = 'cancelled');
```

This does not return rows whose `status` is `NULL`. For them, `status = 'cancelled'` is unknown, and `NOT unknown` is still unknown. If missing status should count as not cancelled, say so:

```sql
WHERE status IS DISTINCT FROM 'cancelled'
```

## How unknown combines with true and false

The useful cases are:

- `false AND NULL` is `false`. One false condition is enough.
- `true AND NULL` is `NULL`. The answer depends on the missing value.
- `true OR NULL` is `true`. One true condition is enough.
- `false OR NULL` is `NULL`. The answer depends on the missing value.
- `NOT NULL` is `NULL`.

`WHERE` keeps only rows for which the whole condition is `true`. It drops both `false` and `NULL`.

## Precedence and evaluation

In PostgreSQL, `NOT` binds more tightly than `AND`, and `AND` more tightly than `OR`. Still, use parentheses when mixing them. The next reader should not have to remember the order.

Do not use `AND` to guard an expression that would fail for some rows, such as division by zero. PostgreSQL may reorganize Boolean expressions while planning a query. Use `CASE` when one expression must only be evaluated for certain values:

```sql
SELECT CASE
         WHEN units = 0 THEN NULL
         ELSE total::numeric / units
       END AS amount_per_unit
FROM sales;
```

Here a missing result means the rate cannot be calculated. A real application might report that case separately.

## Check your understanding

1. Does `false OR NULL` pass a `WHERE` clause?
2. Why does `NOT (status = 'cancelled')` leave out a missing status?
3. What do the parentheses change in the first query?

## Further reading

- [PostgreSQL logical operators](https://www.postgresql.org/docs/current/functions-logical.html)
- [PostgreSQL expression evaluation](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-EXPRESS-EVAL)
