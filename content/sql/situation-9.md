# Situation-9

## The question

A product has five units in stock. Two shoppers each try to reserve three units at nearly the same time. The shop must not sell six units. Show a PostgreSQL statement that either reserves all three units or reserves none, and explain how the application knows which happened.

```sql
CREATE TEMP TABLE products (
  product_id integer PRIMARY KEY,
  stock integer NOT NULL CHECK (stock >= 0)
);
INSERT INTO products VALUES (1, 5);
```

## Work through it

Make the stock check and decrease one `UPDATE`. A separate `SELECT` followed by an unconditional `UPDATE` leaves room for another shopper to change the row between those steps.

```sql
UPDATE products
SET stock = stock - 3
WHERE product_id = 1 AND stock >= 3
RETURNING product_id, stock;
```

The first update returns `(1, 2)`. It changed one row, so three units were reserved. Try the same statement again:

```sql
UPDATE products
SET stock = stock - 3
WHERE product_id = 1 AND stock >= 3
RETURNING product_id, stock;
```

The second update returns no row. It did not reserve stock because only two units remain. A final read confirms the stored value:

```sql
SELECT stock FROM products WHERE product_id = 1;
```

It returns `2`. In PostgreSQL's default Read Committed isolation, concurrent updates of this same row wait for the first updater. After it commits, the waiting update checks its `WHERE` condition against the new row version. Only one of two requests for three units can succeed when stock starts at five.

If a reservation also creates an order row, put the stock update and order insert in one transaction. Commit both or roll back both. A client retry after a timeout might otherwise reserve twice; give each request a unique ID and record it so a repeated request can return the original result. Reject zero or negative requested quantities before running the update. For several products in one order, lock rows in a consistent order and handle a failed reservation by rolling back the whole transaction.

## Check your understanding

1. How does the application know that the second request failed to reserve stock?
2. Why is a separate stock read followed by an unconditional update unsafe?
3. What should happen if the stock change succeeds but creating the order fails?

## Further reading

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL UPDATE](https://www.postgresql.org/docs/current/sql-update.html)
