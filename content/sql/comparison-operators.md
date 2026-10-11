# Comparison Operators

A comparison asks whether two values have a given relationship. It returns `true`, `false`, or `NULL`. In a `WHERE` clause, only `true` keeps the row. This page uses PostgreSQL syntax.

## The common operators

- `=` means equal.
- `<>` means not equal.
- `<` and `>` mean less than and greater than.
- `<=` and `>=` include the boundary value.

PostgreSQL also accepts `!=` for not equal. Use `<>` when you want the standard spelling.

Suppose `products` has an `item_id`, `price`, and `stock_count`:

```sql
SELECT item_id, price
FROM products
WHERE price >= 10.00 AND price < 25.00;
```

A price of 10.00 passes. A price of 25.00 does not. This is a half-open interval. It is useful when two price bands must not overlap.

## Missing values are not ordinary values

`price = NULL` does not mean "price is missing." Any ordinary comparison with `NULL` gives unknown, represented by `NULL`. Use `IS NULL` or `IS NOT NULL`:

```sql
SELECT item_id
FROM products
WHERE price IS NULL;
```

If you need to compare two values and count two missing values as equal, PostgreSQL has `IS NOT DISTINCT FROM`:

```sql
SELECT 5 IS NOT DISTINCT FROM 5 AS same_numbers,
       NULL IS NOT DISTINCT FROM NULL AS both_missing,
       5 IS DISTINCT FROM NULL AS different_values;
```

All three output values are `true`. Unlike `=` and `<>`, these tests always return a Boolean result, even with `NULL`.

## Types matter

Compare numbers with numbers and dates with dates. Text comparison follows the active collation, which controls character ordering. Do not use `name > 'M'` as a portable test for a name's first letter. A date or timestamp should also be compared to a value of the intended type and time zone.

SQL does not support mathematical chains such as `0 < price < 100`. Write two comparisons:

```sql
WHERE price > 0 AND price < 100
```

## Check your understanding

1. Does a row with `price = NULL` pass `WHERE price <> 0`?
2. Which operator includes a price of exactly 25.00?
3. When would `IS NOT DISTINCT FROM` be more useful than `=`?

## Further reading

- [PostgreSQL comparison operators](https://www.postgresql.org/docs/current/functions-comparison.html)
- [PostgreSQL collations](https://www.postgresql.org/docs/current/collation.html)
