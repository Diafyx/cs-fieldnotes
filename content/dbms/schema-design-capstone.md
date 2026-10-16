# Schema-Design Capstone

A good schema starts with the work the application must do. Here the application sells a small catalog of products. A customer can place many orders. An order has one or more lines. The price on an old order must stay the same when a product's current price changes.

## Turn requirements into tables

| Rule | Design choice |
| --- | --- |
| A customer can place many orders. | `orders.customer_id` refers to `customers.customer_id`. |
| An order can contain the same product on different lines. | `(order_id, line_no)` identifies each line. |
| Product names and current prices belong to the catalog. | Store them once in `products`. |
| A sale needs its old price. | Store `unit_price` on each order line. |
| A line cannot have zero or negative units. | Add a `CHECK` constraint. |

This is a one-to-many relationship from customer to order and from order to line. An order line also points to one product. The two foreign keys stop a line from naming an order or product that does not exist. They do not prove that an order has at least one line. The application must create the order and its first line in one transaction, or add a database-side rule if that guarantee must hold for every writer.

## Build the small schema

Run this in a scratch PostgreSQL database. The table names use a `cap_` prefix so they are easy to remove later.

```sql
CREATE TABLE cap_customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE cap_products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    current_price NUMERIC(10, 2) NOT NULL CHECK (current_price >= 0)
);

CREATE TABLE cap_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES cap_customers(customer_id),
    status TEXT NOT NULL CHECK (status IN ('open', 'paid', 'cancelled'))
);

CREATE TABLE cap_order_lines (
    order_id INTEGER NOT NULL REFERENCES cap_orders(order_id),
    line_no INTEGER NOT NULL CHECK (line_no > 0),
    product_id INTEGER NOT NULL REFERENCES cap_products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    PRIMARY KEY (order_id, line_no)
);

CREATE INDEX cap_orders_by_customer ON cap_orders (customer_id, order_id);

INSERT INTO cap_customers VALUES
    (1, 'Ana', 'ana@example.test'),
    (2, 'Ben', 'ben@example.test');
INSERT INTO cap_products VALUES
    (10, 'Notebook', 5.00),
    (20, 'Mug', 12.00);

BEGIN;
INSERT INTO cap_orders VALUES (100, 1, 'paid');
INSERT INTO cap_order_lines VALUES
    (100, 1, 10, 2, 5.00),
    (100, 2, 20, 1, 12.00);
COMMIT;

UPDATE cap_products SET current_price = 14.00 WHERE product_id = 20;

SELECT o.order_id, c.name,
       SUM(l.quantity * l.unit_price) AS order_total
FROM cap_orders AS o
JOIN cap_customers AS c ON c.customer_id = o.customer_id
JOIN cap_order_lines AS l ON l.order_id = o.order_id
GROUP BY o.order_id, c.name;
```

The result is `(100, Ana, 22.00)`. The mug now costs `14.00` in the catalog, but order 100 keeps its sale price of `12.00`. Ben has no order and does not appear in this inner join. Use a left join from `cap_customers` if a report must also show customers with no orders.

## Check what the schema does and does not guarantee

The line table avoids repeating the customer's name and email on every line. Product details live in one place, while `unit_price` is a deliberate sale-time snapshot. This avoids an update anomaly without changing past receipts. A stored order total would be another copy that must stay in step with the lines. Calculate it when reading, or define and test the transaction that updates it.

For a real checkout, decide how tax, discounts, shipping, refunds, and currency are represented. `NUMERIC(10, 2)` suits this small example, but currencies can have different decimal rules. With a normal case-sensitive PostgreSQL collation, this plain `TEXT` unique constraint treats `Ana@...` and `ana@...` as different addresses. Decide what your application needs. A paid order may also need to forbid later line edits. A foreign key or the status check alone cannot enforce that workflow.

The customer index helps a query that starts with one `customer_id`. Foreign keys do not automatically create an index on the referencing column in PostgreSQL. The primary key on `(order_id, line_no)` already helps find lines for one order. Check real query plans before adding more indexes: each index also costs space and write work.

## Extend the design safely

Write down the main queries before adding tables or indexes. If the application needs stock counts, add a separate inventory rule and test two buyers racing for the last unit. If an order must have a payment, decide whether payment is local to this database or handled by another service. A remote payment cannot join this local transaction automatically. Plan how a schema migration will handle old rows and old application versions before making a new column required.

When finished, drop the four `cap_` tables in dependency order in the scratch database: lines, orders, products, then customers.

## Try it yourself

1. Why is `unit_price` on a line even though the product already has `current_price`?
2. Which key lets one order contain two lines for the same product?
3. Why can an order with no lines still pass the listed foreign key checks?
4. What changes if a report must show Ben with a total of zero?
5. What must be protected when two buyers try to buy the last item?

## References

- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html)
- [PostgreSQL transaction tutorial](https://www.postgresql.org/docs/current/tutorial-transactions.html)
