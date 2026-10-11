# Numeric and NULL Functions

SQL functions can calculate a value for each row. Numeric functions work with numbers. `NULL` functions help when a value is missing or when a calculation has no valid result. This page uses PostgreSQL.

## Work on one row at a time

```sql
SELECT order_id,
       ABS(balance_change) AS size_of_change,
       ROUND(amount, 2) AS rounded_amount
FROM orders;
```

`ABS(-12)` is 12. `ROUND(12.345::numeric, 2)` is 12.35. These expressions make output values. They do not change the stored rows.

`GREATEST(a, b)` picks the larger of two values for one row. `LEAST(a, b)` picks the smaller. They do not find the largest value across many rows; `MAX` and `MIN` are aggregates for that job.

## Deal with missing or unusable values

`COALESCE(a, b)` returns `a` when it is present, otherwise `b`. `NULLIF(a, b)` returns `NULL` when `a` equals `b`:

```sql
SELECT item_id,
       COALESCE(display_name, internal_name) AS name_to_show,
       sold_units::numeric / NULLIF(stock_units, 0) AS sell_through
FROM inventory;
```

The first expression chooses a name. The second avoids division by zero by returning `NULL` for zero stock. A missing rate is different from a rate of zero. Decide how the application should show that missing result.

## Choose the right kind of operation

Use `IS NULL` to test whether a value is missing. Use `COALESCE` to choose a fallback value. Use `NULLIF` to turn a special value into missing. None of these changes the table. Do not replace every `NULL` with zero: doing so can change sums, averages, and the meaning of a report.

PostgreSQL uses `COALESCE`, not MySQL's `IFNULL` name. The functions do similar work for two arguments, but the names are not interchangeable in a PostgreSQL query.

## Check your understanding

1. Which function finds the larger value within one row, and which finds the largest value across rows?
2. Why is a missing sell-through rate different from zero?
3. Does `COALESCE(display_name, internal_name)` update either column?

## Further reading

- [PostgreSQL mathematical functions](https://www.postgresql.org/docs/current/functions-math.html)
- [PostgreSQL conditional expressions](https://www.postgresql.org/docs/current/functions-conditional.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
