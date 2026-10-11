# Database & Table Basics

A table is a named collection of rows. Every row follows the same column definitions, but two rows can hold different values. A column has a name and a data type. A database contains tables and other objects, such as indexes and views. In PostgreSQL, a schema is a namespace inside a database; it helps group and name those objects.

The words are simple, but a good table starts with a precise question: what does one row represent? If that answer is unclear, joins, keys, and updates become harder to get right.

## Choose what one row means

Suppose one row in `customers` represents one customer, and one row in `orders` represents one order:

```sql
CREATE TABLE customers (
    customer_id integer PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    customer_id integer NOT NULL REFERENCES customers(customer_id),
    placed_at timestamptz NOT NULL,
    amount numeric(10, 2) NOT NULL CHECK (amount >= 0)
);
```

The `customers` table has one row per customer. The `orders` table has one row per order, even when one customer places many orders. `customer_id` connects the two tables. The primary keys identify rows. `NOT NULL` requires a value, and `CHECK` rules out a negative amount.

## Insert and read rows

```sql
INSERT INTO customers (customer_id, name)
VALUES (10, 'Maya');

INSERT INTO orders (order_id, customer_id, placed_at, amount)
VALUES (101, 10, '2026-01-12 09:00:00+00', 24.50);

SELECT order_id, amount
FROM orders
WHERE customer_id = 10;
```

The second insert succeeds because customer 10 exists. An order that refers to a missing customer fails if the foreign key is active. This is better than relying on every application path to remember the same rule.

## Rows do not have a default order

Do not treat a table like an array. Even if inserts appear in a certain order, a query without `ORDER BY` has no guaranteed result order. If you need the newest orders first, request it:

```sql
SELECT order_id, placed_at
FROM orders
ORDER BY placed_at DESC, order_id DESC;
```

The second sort key makes the order stable when two orders share the same timestamp.

## Keep separate facts separate

Putting many orders into columns such as `order_1`, `order_2`, and `order_3` limits how many orders a customer can have and makes queries awkward. Use a separate `orders` table instead. Avoid copying a customer's name into every order unless you have a clear need to preserve a historical snapshot. Otherwise, one name change can leave conflicting copies.

## Check your understanding

1. What does one row in `orders` represent? What does `customer_id` represent there?
2. Which rule prevents an order from pointing to a missing customer?
3. Why is `ORDER BY placed_at DESC` alone not enough for a stable order when timestamps can tie?

## Further reading

- [PostgreSQL table basics](https://www.postgresql.org/docs/current/ddl-basics.html)
- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL sorting rows](https://www.postgresql.org/docs/current/queries-order.html)
