# Most Recent Three Orders for Each Customer

Return up to three latest orders for each customer who has ordered. If orders share a timestamp, choose the larger order ID first. This gives a stable limit of three rows per customer.

## Sample data

```sql
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  ordered_at timestamp NOT NULL
);
INSERT INTO orders VALUES
  (10, 1, '2026-01-01 09:00:00'),
  (11, 1, '2026-01-02 10:00:00'),
  (12, 1, '2026-01-02 10:00:00'),
  (13, 1, '2026-01-03 08:00:00'),
  (20, 2, '2026-01-01 12:00:00'),
  (21, 2, '2026-01-04 11:00:00');
```

## Solution

```sql
SELECT customer_id, order_id, ordered_at, recent_position
FROM (
  SELECT o.customer_id, o.order_id, o.ordered_at,
         ROW_NUMBER() OVER (
           PARTITION BY o.customer_id
           ORDER BY o.ordered_at DESC, o.order_id DESC
         ) AS recent_position
  FROM orders AS o
) AS ranked
WHERE recent_position <= 3
ORDER BY customer_id, recent_position;
```

Customer 1 gets orders 13, 12, and 11 in positions 1, 2, and 3. Order 10 is fourth and is excluded. Customer 2 gets both of its orders, 21 then 20. The inner query numbers rows separately for each customer. The outer query keeps at most three rows for each.

If every order tied at the third timestamp must appear, use `RANK` on `ordered_at` without the ID tie breaker, but the result may contain more than three rows. If the task means three distinct order dates, use `DENSE_RANK` on the timestamp or date instead. A customer with no orders is absent; join a customer table if the report must show them with empty order fields.

## Check your understanding

1. Why does order 12 come before order 11?
2. How many rows does customer 2 return?
3. Which ranking rule could return more than three orders for one customer?

## Further reading

- [PostgreSQL ROW_NUMBER and RANK](https://www.postgresql.org/docs/current/functions-window.html)
