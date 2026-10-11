# Find the Most Recent Order for Each Product

Show each product and its latest order. Keep products that have never been ordered. If orders share the latest time, choose the larger order ID.

## Sample data

```sql
CREATE TEMP TABLE products (product_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  product_id integer NOT NULL,
  ordered_at timestamp NOT NULL
);
INSERT INTO products VALUES (1, 'Pen'), (2, 'Book'), (3, 'Bag');
INSERT INTO orders VALUES
  (10, 1, '2026-01-01 09:00:00'),
  (11, 1, '2026-01-02 10:00:00'),
  (12, 1, '2026-01-02 10:00:00'),
  (13, 2, '2026-01-03 08:00:00');
```

## Solution

```sql
SELECT p.product_id, p.name, r.order_id
FROM products AS p
LEFT JOIN (
  SELECT o.product_id, o.order_id,
         ROW_NUMBER() OVER (
           PARTITION BY o.product_id
           ORDER BY o.ordered_at DESC, o.order_id DESC
         ) AS position
  FROM orders AS o
) AS r ON r.product_id = p.product_id AND r.position = 1
ORDER BY p.product_id;
```

The rows are `(1, 'Pen', 12)`, `(2, 'Book', 13)`, and `(3, 'Bag', NULL)`. The subquery ranks orders within each product. The left join keeps Bag. Order 12 wins the time tie for Pen because its ID is larger.

If the requirement is to show every order tied at the latest time, use `RANK()` on `ordered_at` alone and keep rank 1. A simple `MAX(ordered_at)` join can return several rows when times tie.

## Check your understanding

1. Why does order 12 win over order 11?
2. Why is Bag included?
3. How would the answer change if every latest-time tie must be kept?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
