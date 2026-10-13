# Everything About Keys

A key is a column or set of columns that identifies a row under a stated rule. Keys also give other tables a stable way to refer to that row. The key rules must hold for all valid data, not just for today's sample.

## Primary, alternate, and foreign keys

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  email text NOT NULL UNIQUE,
  name text NOT NULL
);

CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customers(customer_id)
);

CREATE TEMP TABLE order_items (
  order_id integer NOT NULL REFERENCES orders(order_id),
  line_number integer NOT NULL,
  product_name text NOT NULL,
  PRIMARY KEY (order_id, line_number)
);

INSERT INTO customers VALUES (1, 'ada@example.test', 'Ada');
INSERT INTO orders VALUES (10, 1);
INSERT INTO order_items VALUES (10, 1, 'Lamp'), (10, 2, 'Mug');

SELECT o.order_id, c.name, i.line_number, i.product_name
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN order_items AS i ON i.order_id = o.order_id
ORDER BY o.order_id, i.line_number;
```

The query returns Lamp as line 1 and Mug as line 2 on Ada's order 10. `customer_id` is the chosen primary key for customers. Because `email` is both `UNIQUE` and `NOT NULL`, it is another possible key if the business rule really guarantees that one address belongs to one customer. `orders.customer_id` is a foreign key. The pair `(order_id, line_number)` is a composite primary key for order items.

## Key terms

A superkey uniquely identifies rows, but it may contain extra columns. A candidate key is a minimal superkey: removing any part would lose uniqueness. One candidate key is chosen as the primary key; other candidate keys are alternate keys. A natural key comes from the business, such as an assigned SKU. A surrogate key is made for identification, such as `customer_id`. Neither kind is automatically right for every table.

For example, `(customer_id, email)` is a superkey here but is not minimal because `customer_id` alone is enough. Email may change, be shared, or need case handling. If it is not reliably unique in the business, do not force it into a `UNIQUE` constraint. A surrogate ID does not remove the need to protect a real business key such as a unique SKU.

In PostgreSQL, a primary key is unique and not null. A `UNIQUE` column can usually contain several SQL `NULL` values because nulls are distinct by default. Add `NOT NULL` if it must identify every row; `UNIQUE NULLS NOT DISTINCT` is another choice when at most one null is allowed. A foreign key normally points to a primary key or another suitable unique key. A composite foreign key must use the matching columns together.

Primary and unique constraints create indexes on their own columns in PostgreSQL. PostgreSQL does not automatically create an index on a child table's referencing foreign key. Add one when joins or parent deletes need it, then check the workload. The foreign key constraint still works without that index.

## Check your understanding

1. Why is `(customer_id, email)` not a candidate key in this example?
2. What stops two order items from both using line number 1 on order 10?
3. Why might a surrogate key still need a separate `UNIQUE` business rule?

## Further reading

- [PostgreSQL primary, unique, and foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Codd's relational model paper](https://doi.org/10.1145/362384.362685)
