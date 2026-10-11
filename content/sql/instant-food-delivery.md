# Instant Food Delivery

This exercise calls a delivery instant when the requested delivery date is the same as the order date. Find what percentage of all orders are instant.

## The question

Each row in `deliveries` is one order. Return one `instant_percentage`, rounded to two decimal places. Both dates are present. A later requested date is not instant.

```sql
CREATE TEMP TABLE deliveries (
  delivery_id integer PRIMARY KEY,
  order_date date NOT NULL,
  requested_date date NOT NULL
);

INSERT INTO deliveries (delivery_id, order_date, requested_date) VALUES
  (1, '2026-01-03', '2026-01-03'),
  (2, '2026-01-03', '2026-01-05'),
  (3, '2026-01-04', '2026-01-04');
```

## A solution

```sql
SELECT ROUND(
         100.0 * AVG(
           CASE WHEN order_date = requested_date THEN 1 ELSE 0 END
         ),
         2
       ) AS instant_percentage
FROM deliveries;
```

The result is 66.67. The `CASE` makes a 1 for an instant order and a 0 for any other order. The average of 1, 0, and 1 is two thirds. Multiplying by 100 turns it into a percentage, and `ROUND` limits the result to two decimal places.

The `ELSE 0` is needed. Without it, non-instant orders become `NULL`, and `AVG` ignores them. That would make the percentage too high. With no delivery rows, `AVG` returns `NULL`, so the percentage is undefined rather than zero.

If the business means delivery within 24 hours instead of the same calendar date, this date-only table cannot answer that question. It would need timestamps and a time zone rule.

## Check your understanding

1. Why does `ELSE 0` matter inside `AVG`?
2. What percentage would the sample have if order 2 were also instant?
3. Why are dates alone insufficient for a 24-hour rule?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL CASE expression](https://www.postgresql.org/docs/current/functions-conditional.html#FUNCTIONS-CASE)
