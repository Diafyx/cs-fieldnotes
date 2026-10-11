# Fundamentals of GROUP BY

`GROUP BY` collects rows with the same grouping values. An aggregate such as `COUNT` or `SUM` then makes one answer for each group. The grouping columns decide what one output row means.

## One grouping column

```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
ORDER BY customer_id;
```

If customer 7 has three orders, the result has one row for customer 7 with `order_count = 3`. The query does not promise an order until `ORDER BY` is added.

## More than one grouping column

```sql
SELECT customer_id, status, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id, status
ORDER BY customer_id, status;
```

Now one result row represents one `(customer_id, status)` pair. A customer with both paid and pending orders gets two rows. If `status` can be `NULL`, rows with the same customer ID and a `NULL` status form one group. Grouping can put missing values together even though `NULL = NULL` is not true in a `WHERE` comparison.

## Which columns can SELECT show?

In a grouped query, a selected column normally must be a grouping column or be inside an aggregate. This would be unclear:

```sql
SELECT customer_id, order_id, COUNT(*)
FROM orders
GROUP BY customer_id;
```

A customer may have several order IDs. Which one should the result show? PostgreSQL rejects this unless it can prove the extra column depends on a grouped primary key. For clear, portable queries, group by every non-aggregated value you want to display, or choose a specific aggregate such as `MIN(order_id)`.

## No GROUP BY means one overall group

```sql
SELECT COUNT(*) AS all_orders
FROM orders;
```

This returns one row for the whole table, even if the table is empty. In that case the count is zero. By contrast, `GROUP BY customer_id` on an empty table returns no groups and therefore no rows.

`SELECT DISTINCT customer_id` also returns one row per different customer ID, but it does not calculate a count for each customer. Use `GROUP BY` when you need a value for each group.

## Check your understanding

1. What does one output row mean when the query groups by customer and status?
2. Why is `order_id` unclear in the rejected example?
3. What is the difference between an overall count and a grouped count on an empty table?

## Further reading

- [PostgreSQL GROUP BY clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-GROUPBY)
- [PostgreSQL table expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html)
