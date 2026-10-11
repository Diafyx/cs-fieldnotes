# HAVING Clause (Basics, HAVING with COUNT)

`HAVING` filters groups after they have been made. `WHERE` filters individual rows before grouping. Use `HAVING` when the rule depends on a group result such as `COUNT(*)` or `SUM(amount)`.

## Find customers with enough paid orders

```sql
SELECT customer_id, COUNT(*) AS paid_orders
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
HAVING COUNT(*) >= 3
ORDER BY customer_id;
```

First, `WHERE` keeps paid orders. Next, `GROUP BY` gathers those orders by customer. `HAVING` keeps customers with at least three paid orders. An order with a different status never enters a group. A customer with no paid orders has no group in this query.

`WHERE COUNT(*) >= 3` is not valid because `WHERE` runs before the groups and their counts exist. In PostgreSQL, repeat the aggregate in `HAVING` instead of using the output alias `paid_orders` there.

## Filter with a different aggregate

```sql
SELECT customer_id, SUM(amount) AS paid_total
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
HAVING SUM(amount) > 100
ORDER BY customer_id;
```

This asks for customers whose paid order amounts add to more than 100. It is different from looking for individual orders above 100. If all matching amounts for a customer are `NULL`, `SUM(amount)` is `NULL`, so that group does not pass.

## Avoid a common mix-up

To find customers with at least three orders of any status and show how many were paid, do not put `status = 'paid'` in the query's `WHERE`. That would remove non-paid orders from the total. Use `COUNT(*)` for all orders and a conditional count for paid orders, then apply `HAVING COUNT(*) >= 3`.

PostgreSQL allows `HAVING` without `GROUP BY`; then the whole input acts as one group. Most beginner reports are clearer when the grouping key is explicit.

## Check your understanding

1. Does the first query count pending orders toward the threshold?
2. Why does `WHERE COUNT(*) >= 3` fail?
3. How is a customer's total paid amount different from one large paid order?

## Further reading

- [PostgreSQL HAVING clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-HAVING)
- [PostgreSQL table expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html)
