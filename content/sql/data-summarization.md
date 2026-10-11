# Data Summarization

A summary turns many rows into a smaller set of answers. Before writing SQL, decide what one output row means. It might mean one customer, one day, or one product and month. Then decide which numbers to calculate for that row.

## Start with the source row

Suppose each row in `orders` is one order. It has `order_id`, `customer_id`, `status`, and `amount`. To report paid order count and paid amount per customer:

```sql
SELECT customer_id,
       COUNT(*) AS paid_orders,
       SUM(amount) AS paid_amount
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
ORDER BY customer_id;
```

One output row represents one customer with at least one paid order. `WHERE` removes other orders before grouping. `GROUP BY` makes a group for each customer. `COUNT(*)` counts orders in that group. `SUM(amount)` adds their non-null amounts.

## Name the grain

The grain is what one source row represents. If you join `orders` to `order_lines`, one order may appear once per line. Counting rows after that join counts lines, not orders. You could count distinct order IDs, but first check whether the join is needed. A wrong source grain gives a neat-looking but wrong summary.

The grain of the result also matters. If you group by both customer and month, one output row means one customer in one month. A customer may then appear many times. Say this in the report title or column names.

## Decide what missing data means

Most aggregates ignore `NULL` inputs. `COUNT(*)` still counts the row. If every amount in a group is `NULL`, `SUM(amount)` is `NULL`, not zero. Zero says you know the sum is zero; `NULL` says no usable amount was available. Choose a fallback only when the business rule justifies it.

## Check the result

After writing a summary, check one small group by hand. Count its source rows, add its amounts, and compare with the query. Also check a group with `NULL`, a boundary date, and a customer with no matching orders. A grouped query over `orders` alone cannot list customers who have no orders; that needs a customer table and a join.

## Check your understanding

1. What does one row of the example result represent?
2. Why might joining order lines make `COUNT(*)` too large?
3. Can the example show a customer with no paid orders?

## Further reading

- [PostgreSQL GROUP BY and HAVING](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
