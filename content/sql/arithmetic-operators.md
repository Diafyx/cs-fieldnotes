# Arithmetic Operators

SQL can calculate values from numeric columns. The usual operators are `+` for addition, `-` for subtraction, `*` for multiplication, `/` for division, and `%` for remainder. The examples here use PostgreSQL.

## Calculate a value per row

Suppose `order_lines` has `quantity` and `unit_price`. A line total is the price of one item times the number sold:

```sql
SELECT order_id, quantity, unit_price,
       quantity * unit_price AS line_total
FROM order_lines;
```

`line_total` is an output value. It does not change the table. If either input is `NULL`, the calculated value is `NULL`.

Use parentheses to make the intended order clear:

```sql
SELECT (subtotal + shipping_fee) * 0.10 AS tax_example
FROM invoices;
```

This is only an arithmetic example. Real tax rules can depend on location and what was sold.

## Division needs care

In PostgreSQL, dividing two integer values truncates the fractional part. Dividing by zero raises an error:

```sql
SELECT 5 / 2 AS integer_result,
       5.0 / 2 AS decimal_result,
       5 % 2 AS remainder;
```

The results are `2`, `2.5`, and `1`. If a rate should keep decimals, make sure at least one operand has a suitable numeric type. For stored money or exact decimal rates, use `numeric` with a chosen precision and scale. Floating point types can have small representation errors.

When zero is allowed in a denominator, `NULLIF` can turn it into a missing result instead of an error:

```sql
SELECT sold_units::numeric / NULLIF(available_units, 0) AS sell_through
FROM inventory;
```

`NULLIF(available_units, 0)` returns `NULL` when the count is zero. Division by `NULL` then returns `NULL`. Decide whether that missing result should be shown as blank, as an error message, or handled some other way. Do not silently replace it with zero if zero would mean a real rate.

## Remainders and negative values

`%` returns a remainder. For a positive integer ID, `id % 2 = 1` selects odd IDs. With negative numbers, remainder rules vary across languages and database products. Test those cases before using `%` to assign buckets.

## Check your understanding

1. Why does `5 / 2` lose the `.5` in PostgreSQL?
2. What does `quantity * unit_price` return when `unit_price` is `NULL`?
3. Why might `NULLIF` be better than returning zero for an undefined rate?

## Further reading

- [PostgreSQL mathematical operators](https://www.postgresql.org/docs/current/functions-math.html)
- [PostgreSQL numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html)
- [PostgreSQL conditional expressions](https://www.postgresql.org/docs/current/functions-conditional.html)
