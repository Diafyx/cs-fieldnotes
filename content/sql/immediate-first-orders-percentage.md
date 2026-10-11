# Immediate First Orders Percentage

An order is immediate when its order date equals the customer's preferred delivery date. Find the percentage of customers whose first order was immediate. If two orders share a customer's earliest date, use the smaller order ID as the first.

## Sample data

```sql
CREATE TEMP TABLE deliveries (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  order_date date NOT NULL,
  preferred_date date NOT NULL
);
INSERT INTO deliveries VALUES
  (10, 1, '2026-01-01', '2026-01-01'),
  (11, 1, '2026-01-02', '2026-01-03'),
  (12, 2, '2026-01-01', '2026-01-02'),
  (13, 3, '2026-01-03', '2026-01-03');
```

## Solution

```sql
SELECT ROUND(100.0 * SUM(CASE WHEN order_date = preferred_date THEN 1 ELSE 0 END)
             / NULLIF(COUNT(*), 0), 2) AS immediate_percentage
FROM (
  SELECT d.order_date, d.preferred_date,
         ROW_NUMBER() OVER (
           PARTITION BY d.customer_id ORDER BY d.order_date, d.order_id
         ) AS position
  FROM deliveries AS d
) AS ranked
WHERE position = 1;
```

The answer is `66.67`. Customers 1 and 3 had an immediate first order; customer 2 did not. The inner query picks one first order for each customer. The outer aggregate counts those first orders, not all orders. `100.0` avoids integer division, and `NULLIF` makes an empty input return `NULL` instead of dividing by zero.

If “first” means the earliest timestamp rather than calendar date, store and order by that timestamp. If all orders tied on the first date should count, the business rule must say how to combine them before calculating one percentage per customer.

## Check your understanding

1. Why does order 11 not affect the percentage?
2. How many customers are in the denominator?
3. What does the query return when there are no orders?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
