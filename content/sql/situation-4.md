# Situation-4

## The question

A shop asks for the total amount of paid orders placed in January 2026. Cancelled orders do not count. Return one amount, even if the month has no paid orders.

```sql
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  ordered_on date NOT NULL,
  status text NOT NULL CHECK (status IN ('paid', 'cancelled')),
  amount numeric(10, 2) NOT NULL
);

INSERT INTO orders VALUES
  (1, '2026-01-01', 'paid', 50.00),
  (2, '2026-01-31', 'paid', 40.00),
  (3, '2026-01-20', 'cancelled', 30.00),
  (4, '2026-02-01', 'paid', 60.00);
```

Orders 1 and 2 count. The January total is 90.00.

## Work through it

Use a lower bound that includes January 1 and an upper bound that excludes February 1. Filter the status before summing.

```sql
SELECT COALESCE(SUM(amount), 0) AS january_paid_total
FROM orders
WHERE status = 'paid'
  AND ordered_on >= '2026-01-01'
  AND ordered_on < '2026-02-01';
```

The result is `90.00` in PostgreSQL. The cancelled order does not count, and February 1 is outside the range. `SUM` returns `NULL` when no rows qualify; `COALESCE` makes that result zero as the question asks.

The same lower-inclusive, upper-exclusive pattern works well for timestamps. If a report uses local business dates but the database stores timestamps, first define the business time zone and convert the month boundaries correctly. Do not assume that the server's time zone is the business time zone. For money, decide whether refunds, tax, and shipping are included before calling a sum "revenue." This exercise only sums the stored amount of paid orders.

## Check your understanding

1. Why is February 1 excluded by the upper bound?
2. What would the query return for a month with no paid orders if `COALESCE` were removed?
3. What extra rule is needed if orders store timestamps but the report uses a local time zone?

## Further reading

- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
