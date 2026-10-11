# Most Frequently Ordered Product(s) for Each Customer

For each customer who has ordered something, return every product they ordered the most times. Count order rows, not units. Keep ties. Include the product name with its ID.

## Sample data

```sql
CREATE TEMP TABLE customers (customer_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE products (product_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  product_id integer NOT NULL
);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara');
INSERT INTO products VALUES (10, 'Pen'), (20, 'Book');
INSERT INTO orders VALUES
  (1, 1, 10), (2, 1, 10), (3, 1, 20), (4, 1, 20),
  (5, 2, 20), (6, 2, 20), (7, 2, 20), (8, 2, 10);
```

## Solution

```sql
WITH counts AS (
  SELECT o.customer_id, o.product_id, COUNT(*) AS times_ordered
  FROM orders AS o
  GROUP BY o.customer_id, o.product_id
), ranked AS (
  SELECT customer_id, product_id, times_ordered,
         RANK() OVER (
           PARTITION BY customer_id ORDER BY times_ordered DESC
         ) AS place
  FROM counts
)
SELECT r.customer_id, p.product_id, p.name, r.times_ordered
FROM ranked AS r
JOIN customers AS c ON c.customer_id = r.customer_id
JOIN products AS p ON p.product_id = r.product_id
WHERE r.place = 1
ORDER BY r.customer_id, p.product_id;
```

The rows are Ana with Pen twice, Ana with Book twice, and Ben with Book three times. Cara has no orders, so she has no most frequent product. `counts` makes one row per customer and product. `ranked` gives the largest count rank 1 within each customer. `RANK()` gives the same rank to a tie; `ROW_NUMBER()` would choose only one of Ana's products.

The sample treats each order row as one product order. If an order can contain many products, count order-line rows or distinct order IDs according to the question. If an order line has a quantity column, summing quantity answers “most units bought,” which is different from “ordered most times.” The joins assume valid customer and product IDs; foreign keys should enforce that in a real schema.

## Check your understanding

1. Why are both of Ana's products returned?
2. Why does Cara not appear?
3. How would the measure change if the task asked for most units bought?

## Further reading

- [PostgreSQL WITH queries](https://www.postgresql.org/docs/current/queries-with.html)
- [PostgreSQL ranking functions](https://www.postgresql.org/docs/current/functions-window.html)
