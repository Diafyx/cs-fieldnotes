# Basic Aggregate Functions (MIN, MAX, SUM, AVG)

An aggregate reads several input rows and returns one value. `MIN` finds the smallest value, `MAX` the largest, `SUM` adds values, and `AVG` finds their arithmetic mean. With `GROUP BY`, each group gets its own result.

## See all four at once

Suppose a table contains three non-null prices: 10, 20, and 30.

```sql
SELECT MIN(price) AS lowest,
       MAX(price) AS highest,
       SUM(price) AS total,
       AVG(price) AS average
FROM products;
```

For those three rows, the result is 10, 30, 60, and 20. Without `GROUP BY`, the query makes one overall result. Add `GROUP BY category_id` to get a separate result per category, and select `category_id` so each result can be identified.

## What NULL changes

These four aggregates ignore `NULL` inputs. If the prices are 10, 20, and `NULL`, `AVG(price)` is 15, not 10. It divides by two known prices. `SUM(price)` is 30.

If there are no non-null prices, `MIN`, `MAX`, `SUM`, and `AVG` return `NULL`. `SUM` does not return zero for an empty input. Use `COALESCE(SUM(price), 0)` only when zero is the correct meaning for your report.

`AVG` over PostgreSQL integer or `numeric` inputs returns `numeric`. Floating point inputs can have small rounding errors. For money, store exact decimal values with `numeric` and decide how to round the displayed result.

## Do not average averages without weights

Suppose one store sold one item for 100 and another sold nine items averaging 10. The average of store averages is 55, but the average price across all ten items is 19. To combine groups, use their sums and counts: `(100 + 90) / 10`.

`MIN` and `MAX` can also work on types with an order, such as dates. `SUM` and `AVG` need suitable numeric or interval types. A minimum date is the earliest date, not a count of dates.

## Check your understanding

1. What is `AVG(price)` for 10, 20, and `NULL`?
2. What does `SUM(price)` return when no rows match the filter?
3. Why can averaging two group averages give the wrong overall average?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html)
