# Highest Order Placing Customer

Count orders per customer, then find the largest count. This page returns every customer tied for the most orders. That rule matters because real data can have ties.

## The question

Each row in `customer_orders` is one order. Return `customer_id` and `order_count` for the customer or customers with the highest count. Sort tied customers by ID.

```sql
CREATE TEMP TABLE customer_orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL
);

INSERT INTO customer_orders (order_id, customer_id) VALUES
  (101, 1),
  (102, 1),
  (103, 2),
  (104, 3),
  (105, 3);
```

## A solution

```sql
WITH order_counts AS (
  SELECT customer_id, COUNT(*) AS order_count
  FROM customer_orders
  GROUP BY customer_id
)
SELECT customer_id, order_count
FROM order_counts
WHERE order_count = (SELECT MAX(order_count) FROM order_counts)
ORDER BY customer_id;
```

The output is `(1, 2)` and `(3, 2)`. Customer 2 has one order. `order_counts` is a named intermediate result with one row per customer. The outer query keeps rows whose count equals the largest count in that result.

If the table is empty, the query returns no customers. If the problem guarantees one winner, a shorter query can sort grouped counts from largest to smallest and use `LIMIT 1`. Without that guarantee, `LIMIT 1` hides tied winners. Adding `customer_id` to the sort only chooses one winner in a predictable way; it does not answer a request for all ties.

This counts rows, so `order_id` must identify one real order. If a join repeats each order once per line item, counting joined rows would give the wrong answer.

## Check your understanding

1. Why does this query return two rows for the sample?
2. What would `LIMIT 1` do to the tie?
3. Why is counting order lines different from counting orders?

## Further reading

- [LeetCode Customer Placing the Largest Number of Orders](https://leetcode.com/problems/customer-placing-the-largest-number-of-orders/)
- [PostgreSQL WITH queries](https://www.postgresql.org/docs/current/queries-with.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
