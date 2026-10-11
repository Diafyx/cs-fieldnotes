# Inactive Customers

An inactive customer can mean several things. This exercise defines it as a customer with no orders on or after January 1, 2026. A customer with only older orders is inactive under that rule.

## The question

Return the IDs and names of customers with no recent order, sorted by ID.

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  ordered_on date NOT NULL
);

INSERT INTO customers VALUES
  (1, 'Ana'), (2, 'Ben'), (3, 'Cara'), (4, 'Dev');
INSERT INTO orders VALUES
  (10, 1, '2025-12-20'),
  (11, 2, '2026-01-03'),
  (12, 4, '2025-12-01'),
  (13, 4, '2026-01-10');
```

## A solution

```sql
SELECT c.customer_id, c.name
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id
 AND o.ordered_on >= '2026-01-01'
WHERE o.order_id IS NULL
ORDER BY c.customer_id;
```

The result is Ana and Cara. Ana has only an old order; Cara has none. Ben and Dev each have a recent order. The date test belongs in `ON` so only recent orders count as matches. If it were put in `WHERE` with `o.order_id IS NULL`, the logic would not describe the intended unmatched rows.

The test uses a non-null order key. A missing value in a nullable order field would not prove that no order matched. For a moving definition such as "no order in the last 90 days," specify the time zone and exact boundary before replacing the fixed date.

## Check your understanding

1. Why is Ana inactive even though she has an order?
2. Why is `o.order_id IS NULL` checked after the left join?
3. What should be decided before using a timestamp-based 90-day rule?

## Further reading

- [PostgreSQL outer joins and conditions](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
