# Situation-6

## The question

A report needs the net amount for each order: settled payments minus refunds. One order can have several payments and several refunds. Return every order, including one with no payment yet, and sort by order ID.

```sql
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY
);
CREATE TEMP TABLE payments (
  payment_id integer PRIMARY KEY,
  order_id integer NOT NULL REFERENCES orders(order_id),
  amount numeric(10, 2) NOT NULL CHECK (amount > 0)
);
CREATE TEMP TABLE refunds (
  refund_id integer PRIMARY KEY,
  order_id integer NOT NULL REFERENCES orders(order_id),
  amount numeric(10, 2) NOT NULL CHECK (amount > 0)
);

INSERT INTO orders VALUES (1), (2), (3);
INSERT INTO payments VALUES (10, 1, 100.00), (11, 1, 50.00), (12, 2, 80.00);
INSERT INTO refunds VALUES (20, 1, 20.00), (21, 1, 30.00);
```

Order 1 has 150.00 in payments and 50.00 in refunds, so its net is 100.00. Order 2 has 80.00. Order 3 has zero.

## Work through it

The answer needs one row per order. Summing after joining both child tables is unsafe: order 1 has two payment rows and two refund rows, so a direct join produces four combinations. Each amount is repeated. Sum each child table at order level first, then join those totals.

```sql
WITH paid AS (
  SELECT order_id, SUM(amount) AS total_paid
  FROM payments
  GROUP BY order_id
), refunded AS (
  SELECT order_id, SUM(amount) AS total_refunded
  FROM refunds
  GROUP BY order_id
)
SELECT o.order_id,
       COALESCE(p.total_paid, 0) - COALESCE(r.total_refunded, 0) AS net_amount
FROM orders AS o
LEFT JOIN paid AS p ON p.order_id = o.order_id
LEFT JOIN refunded AS r ON r.order_id = o.order_id
ORDER BY o.order_id;
```

The result is `(1, 100.00)`, `(2, 80.00)`, and `(3, 0.00)` in PostgreSQL. `COALESCE` turns a missing payment or refund total into zero. It does not change any stored row.

In a real payment system, define which states count as settled and whether refunds are stored as positive or negative amounts. This exercise uses positive refund amounts and subtracts them once. A negative net amount may be valid if earlier payments are missing from the data; investigate before hiding it with a zero floor.

## Check your understanding

1. How many rows does a direct join make for order 1 before grouping?
2. Why does order 3 still appear in the answer?
3. What would change if the refunds table stored negative amounts?

## Further reading

- [PostgreSQL joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
