# Schema Design

A schema is the set of tables, columns, keys, constraints, and relationships that represent the data. In PostgreSQL, the word also means a named namespace inside a database. Here we are designing the table structure. A useful design starts with real actions and rules, then turns them into tables.

## Build a small shop schema

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  email text NOT NULL UNIQUE,
  name text NOT NULL
);

CREATE TEMP TABLE products (
  product_id integer PRIMARY KEY,
  name text NOT NULL,
  current_price numeric(10, 2) NOT NULL CHECK (current_price >= 0)
);

CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customers(customer_id),
  placed_at timestamp NOT NULL
);

CREATE TEMP TABLE order_items (
  order_id integer NOT NULL REFERENCES orders(order_id),
  product_id integer NOT NULL REFERENCES products(product_id),
  quantity integer NOT NULL CHECK (quantity > 0),
  unit_price numeric(10, 2) NOT NULL CHECK (unit_price >= 0),
  PRIMARY KEY (order_id, product_id)
);

INSERT INTO customers VALUES (1, 'ada@example.test', 'Ada');
INSERT INTO products VALUES (100, 'Lamp', 30.00);
INSERT INTO orders VALUES (10, 1, '2026-01-03 09:00:00');
INSERT INTO order_items VALUES (10, 100, 2, 25.00);

SELECT o.order_id, SUM(i.quantity * i.unit_price) AS total
FROM orders AS o
JOIN order_items AS i ON i.order_id = o.order_id
GROUP BY o.order_id;
```

The query returns order `10` with total `50.00`. The current lamp price is `30.00`, but the order line records the charged price of `25.00`. The primary key on `(order_id, product_id)` means a product can appear only once on an order. If the business allows several separate lines for one product, give each line its own `line_id` or line number instead.

## Work through the design in order

List the actions first: create customers, place orders, add several products, change current prices, and read old receipts. Define one row for each table. Choose IDs and relationships. Choose types that fit the values, such as `numeric` for money rather than floating point. Mark required fields `NOT NULL`, add unique and check rules, and decide what a delete should do.

Try edge cases before release: a customer with no orders, an order with no items, two lines for the same product, and an invalid price. This schema allows an empty order because foreign keys alone do not require a child row. If an order must have an item before it is considered placed, enforce that in the workflow or with a suitable database rule.

After the rules are sound, inspect real queries and add indexes where they help. PostgreSQL creates indexes for primary and unique keys, but it does not automatically index every referencing foreign key. Plan schema changes as migrations: add a new rule, clean old data if needed, then validate it. A diagram helps discussion, but the DDL and tests define what the database actually accepts.

## Check your understanding

1. Why does the order line store `25.00` when the product row stores `30.00`?
2. What part of the schema prevents two lines for product 100 on order 10?
3. Does this schema stop an order with no items?

## Further reading

- [PostgreSQL data definition](https://www.postgresql.org/docs/current/ddl.html)
- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
