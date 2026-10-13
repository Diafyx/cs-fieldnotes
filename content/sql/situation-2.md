# Situation-2

## The question

An order can have several payment attempts. A failed attempt does not make the order paid. Return the IDs of orders that have no successful payment. Sort by order ID.

```sql
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY
);
CREATE TEMP TABLE payment_attempts (
  attempt_id integer PRIMARY KEY,
  order_id integer NOT NULL REFERENCES orders(order_id),
  status text NOT NULL CHECK (status IN ('failed', 'succeeded'))
);

INSERT INTO orders VALUES (1), (2), (3), (4);
INSERT INTO payment_attempts VALUES
  (10, 1, 'succeeded'),
  (11, 2, 'failed'),
  (12, 2, 'failed'),
  (13, 4, 'failed'),
  (14, 4, 'succeeded');
```

Order 1 succeeded. Order 2 failed twice. Order 3 has no attempt. Order 4 failed once and then succeeded. The answer is orders 2 and 3.

## Work through it

For each order, ask whether at least one successful attempt exists. Keep the order if the answer is no.

```sql
SELECT o.order_id
FROM orders AS o
WHERE NOT EXISTS (
  SELECT 1
  FROM payment_attempts AS p
  WHERE p.order_id = o.order_id
    AND p.status = 'succeeded'
)
ORDER BY o.order_id;
```

The result is `2`, then `3`. `NOT EXISTS` works for both a failed-only order and an order with no attempts. It also handles any number of attempts without making duplicate order rows.

A common wrong query joins every attempt and filters `status = 'failed'`. It would include order 4 because order 4 has a failed attempt, even though it later succeeded. Another wrong query asks for no payment attempt at all; it would miss order 2. Define "unpaid" from successful attempts, not from the mere presence or absence of a row.

In a real system, decide what `succeeded` means for refunds, chargebacks, and pending payments. Those are separate business rules. The sample question only asks whether an attempt succeeded.

## Check your understanding

1. Why is order 4 absent from the result?
2. Why does filtering joined rows to `failed` give the wrong answer?
3. What would change if the question asked for orders with no payment attempt of any kind?

## Further reading

- [PostgreSQL EXISTS and NOT EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html)
