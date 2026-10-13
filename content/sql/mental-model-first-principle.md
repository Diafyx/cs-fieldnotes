# Mental Model (First Principle)

Start with a question: what fact does one row own? A customer row owns the customer's current name. An order row owns when that order was placed. An order line owns the quantity and price charged for one product on that order. This question helps decide where a column belongs.

## Give each fact an owner

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  current_name text NOT NULL
);

CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customers(customer_id),
  placed_at timestamp NOT NULL
);

CREATE TEMP TABLE order_items (
  order_id integer NOT NULL REFERENCES orders(order_id),
  product_id integer NOT NULL,
  quantity integer NOT NULL CHECK (quantity > 0),
  unit_price_at_purchase numeric(10, 2) NOT NULL CHECK (unit_price_at_purchase >= 0),
  PRIMARY KEY (order_id, product_id)
);

INSERT INTO customers VALUES (1, 'Ada');
INSERT INTO orders VALUES (10, 1, '2026-01-03 09:00:00');
INSERT INTO order_items VALUES (10, 100, 2, 25.00);

SELECT o.order_id, c.current_name,
       SUM(i.quantity * i.unit_price_at_purchase) AS order_total
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN order_items AS i ON i.order_id = o.order_id
GROUP BY o.order_id, c.current_name;
```

The result is order `10`, Ada, and total `50.00`. The total is calculated from line facts. It does not need a stored copy for this small design. The price at purchase stays on the order line because it is a historical fact; changing a product's current price must not rewrite old orders.

## Ask which values determine which facts

If `customer_id` always identifies exactly one current customer name, we say `customer_id` determines `current_name`. If `(order_id, product_id)` identifies one line, that pair determines its quantity and charged price. These are business rules, not guesses from a small dataset. A table should not put a fact under a key that does not determine it.

Some facts change over time. A customer's current name and the name printed on an old receipt may be different valid facts. If the receipt must preserve the old name, store a snapshot on the order or in an immutable receipt record and name it clearly. That is deliberate history, not an accidental second copy of a current field.

Think about delete behavior too. If an order must be kept for records, deleting a customer may need to be blocked or handled by a clear retention rule. Do not choose `ON DELETE CASCADE` merely to make a foreign key error go away.

## Check your understanding

1. Why does an order line store `unit_price_at_purchase`?
2. Which row owns the customer's current name?
3. When would storing a name snapshot on an order be justified?

## Further reading

- [Codd's relational model paper](https://doi.org/10.1145/362384.362685)
- [PostgreSQL foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html)
