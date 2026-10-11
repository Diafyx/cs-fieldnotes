# EXISTS and NOT EXISTS

`EXISTS` is true when its subquery returns at least one row. `NOT EXISTS` is true when it returns none. The selected value is usually irrelevant, so `SELECT 1` makes the intent clear.

## Find customers without orders

```sql
WITH customers(customer_id, name) AS (
  VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara')
), orders(order_id, customer_id) AS (
  VALUES (10, 1), (11, 1), (12, 3)
)
SELECT c.customer_id, c.name
FROM customers AS c
WHERE NOT EXISTS (
  SELECT 1
  FROM orders AS o
  WHERE o.customer_id = c.customer_id
)
ORDER BY c.customer_id;
```

The answer is Ben. For each customer, the inner condition looks for a matching order. Extra orders do not change the result. An order with a `NULL` customer ID would not match anyone and would not hide Ben. That is a useful difference from a careless `NOT IN` query.

## Read the condition closely

The comparison to `c.customer_id` makes this a correlated subquery. If you leave it out, the inner query checks whether *any* order exists, which would give the same answer for every customer. `EXISTS` works with the opposite filter to find customers who have orders.

PostgreSQL may stop checking after finding a match, but the query planner decides how to execute the condition. Do not put functions with side effects inside an `EXISTS` query and assume they will run once for every row. A join can also solve some of these tasks; choose the one that expresses the intended result clearly.

## Check your understanding

1. Which customer appears in the result?
2. What breaks if the inner `WHERE` condition is removed?
3. Why does a `NULL` customer ID in `orders` not exclude Ben?

## Further reading

- [PostgreSQL EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html#FUNCTIONS-SUBQUERY-EXISTS)
