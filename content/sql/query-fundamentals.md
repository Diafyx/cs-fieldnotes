# Query Fundamentals

A query asks the database to return rows. To read a query well, identify its source, its row filter, its groups, and its output. Then check whether the requested order is explicit. Many query mistakes come from getting one of those parts right and quietly assuming the rest.

## Read a query in stages

Suppose `orders` has `customer_id`, `status`, and `amount` columns:

```sql
SELECT customer_id, SUM(amount) AS total
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
HAVING SUM(amount) >= 100
ORDER BY total DESC, customer_id;
```

A useful logical reading is:

1. `FROM orders` provides the source rows.
2. `WHERE` keeps only paid orders.
3. `GROUP BY` makes one group per customer.
4. `HAVING` keeps groups whose sum is at least 100.
5. `SELECT` produces a customer ID and sum for each surviving group.
6. `ORDER BY` puts larger totals first and breaks ties by customer ID.

This is a way to reason about the result. It is not a step-by-step promise about the physical execution plan. The database may reorder work internally while preserving the query's meaning.

## Rows can repeat

SQL query results are not automatically unique. If two orders have the same amount, `SELECT amount FROM orders` can return that amount twice. `DISTINCT` removes duplicate output rows when you ask for it. Use it only when duplicates are truly unwanted; sometimes repeated values are the point of the data.

`SELECT *` is useful when exploring a table. For code you maintain, naming the needed columns makes the result shape clear and avoids pulling data you do not use.

## Missing values change logic

If `status` is `NULL`, `status = 'paid'` is unknown, so `WHERE` does not keep that row. `NULL` also affects joins, groups, and aggregates. Decide what a missing value means before adding a default with `COALESCE`.

## Order is a separate request

The database does not guarantee a row order unless the query uses `ORDER BY`. A limit without a stable sort can return different rows as data or plans change. For pages of results, include a tie-breaker such as a unique ID.

## Ask one clear question

Before writing SQL, say what one output row should represent. In the example, one output row represents one customer who spent at least 100 on paid orders. This sentence tells you why the query groups by customer and why `status` is filtered before the sum.

## Check your understanding

1. In the example, does `WHERE` filter orders or customers?
2. Why is `HAVING` used for `SUM(amount)`?
3. Could the result order be relied on if `ORDER BY` were removed?
4. What does one output row represent?

## Further reading

- [PostgreSQL SELECT reference](https://www.postgresql.org/docs/current/sql-select.html)
- [PostgreSQL table expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [PostgreSQL sorting rows](https://www.postgresql.org/docs/current/queries-order.html)
