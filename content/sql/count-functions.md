# COUNT Functions

`COUNT` answers how many. The expression inside it decides what is counted. `COUNT(*)` counts rows. `COUNT(column)` counts rows where that column is not `NULL`. `COUNT(DISTINCT column)` counts different non-null values.

## Compare the forms

Suppose `visits` has four rows with `referrer_id` values 2, 2, 5, and `NULL`:

```sql
SELECT COUNT(*) AS visits,
       COUNT(referrer_id) AS known_referrers,
       COUNT(DISTINCT referrer_id) AS different_referrers
FROM visits;
```

The result is 4, 3, and 2. The repeated 2 counts twice in `COUNT(referrer_id)`, but once in `COUNT(DISTINCT referrer_id)`. The `NULL` row counts only in `COUNT(*)`.

On an empty input, all three counts return zero. The result still has one row when there is no `GROUP BY`. With `GROUP BY`, groups with no source rows do not exist, so they do not produce a zero count by themselves.

## Count a condition

PostgreSQL supports `FILTER` on an aggregate:

```sql
SELECT customer_id,
       COUNT(*) AS all_orders,
       COUNT(*) FILTER (WHERE status = 'paid') AS paid_orders
FROM orders
GROUP BY customer_id;
```

This counts all orders and paid orders in the same customer group. A customer with orders but no paid orders gets `paid_orders = 0`. The `FILTER` condition applies to that aggregate, not to the entire query. Some other databases use different syntax for conditional counts.

## Count the thing the question names

If one customer has several orders, `COUNT(*)` after grouping by customer counts orders. It does not count customers. If a join repeats each order once per line item, `COUNT(*)` counts joined rows. Check the table and join grain first. `COUNT(DISTINCT order_id)` can count unique orders after a join, but may hide an unnecessary join.

## Check your understanding

1. Why are `COUNT(*)` and `COUNT(referrer_id)` different in the example?
2. Can `COUNT(DISTINCT referrer_id)` include `NULL` as one distinct value?
3. What does `COUNT(*) FILTER (WHERE status = 'paid')` return for a customer with only pending orders?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL aggregate syntax](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-AGGREGATES)
