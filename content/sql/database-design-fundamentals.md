# Database Design Fundamentals

Database design means deciding which facts to store, where each fact belongs, and which rules the database must enforce. A good design lets you add, change, and find data without guessing which copy is correct. Start with the questions the application must answer and the rules that must always hold.

For a small shop, we may need to know who placed an order and when. A customer can place many orders. Every order belongs to one customer. That gives us two kinds of rows and a link between them.

## Put each fact in a clear place

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  name text NOT NULL
);

CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customers(customer_id),
  placed_at timestamp NOT NULL
);

INSERT INTO customers (customer_id, name)
VALUES (1, 'Ada'), (2, 'Ben');

INSERT INTO orders (order_id, customer_id, placed_at)
VALUES (10, 1, '2026-01-03 09:00:00'),
       (11, 1, '2026-01-04 10:00:00');

SELECT o.order_id, c.name
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
ORDER BY o.order_id;
```

The query returns `(10, Ada)` and `(11, Ada)`. Ben has no orders, so an inner join does not show him. Customer names live in `customers`; an order stores the customer ID, not another copy of the name. Changing Ada's name needs one update. The foreign key prevents an order from naming a customer that does not exist.

## Design from rules, not just sample rows

Ask what one row means. Here, one `orders` row means one placed order. Decide which values must exist, which can be missing, and which must be unique. A primary key identifies a row. A foreign key protects a relationship. `NOT NULL` protects a required value. Add `CHECK` and `UNIQUE` constraints for other rules that the database can enforce.

Do not assume the sample is the full rule. Ben currently has no orders, but the design allows that. If the shop needs several products per order, add an `order_items` table. Do not add `product_1`, `product_2`, and `product_3` columns to `orders`; that would impose an arbitrary limit and make queries harder.

Design changes as requirements become clearer. Write down assumptions, test them with example rows, and review them when a new feature arrives. A schema that stores the wrong fact in the wrong place is harder to fix than a missing index.

## Check your understanding

1. Why does an order store `customer_id` instead of a second customer name?
2. How would the query change if Ben must appear with no order?
3. What new table would you add for orders with several products?

## Further reading

- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Chen's original entity and relationship model](https://doi.org/10.1145/320434.320440)
