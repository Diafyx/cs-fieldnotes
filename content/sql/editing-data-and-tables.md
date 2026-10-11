# Editing Data and Tables

Reading a table with `SELECT` leaves its rows alone. Writing to a table changes rows or the table's definition. In PostgreSQL, `INSERT` adds rows, `UPDATE` changes existing rows, and `DELETE` removes selected rows. `ALTER TABLE` changes the table's structure. `TRUNCATE` clears all its rows.

## Choose the command by the change

Imagine a table named `products` with `product_id`, `name`, and `price`:

```sql
INSERT INTO products (product_id, name, price)
VALUES (7, 'Notebook', 12.50);

UPDATE products
SET price = 13.00
WHERE product_id = 7;

DELETE FROM products
WHERE product_id = 7;
```

The first statement creates a row. The second changes that row's price. The third removes it. Each statement is separate. Running all three in order would leave no row with ID 7.

`ALTER TABLE products ADD COLUMN active boolean DEFAULT true;` changes the columns available to every row. It does not mean that a single product was edited. Constraints such as `NOT NULL`, `CHECK`, and foreign keys can reject a write that would break a table rule.

## Check a write before you keep it

For a change to existing rows, first run a `SELECT` with the same `WHERE` condition. Then make the change in a transaction and inspect the affected rows:

```sql
BEGIN;

UPDATE products
SET price = price + 1
WHERE product_id = 7
RETURNING product_id, price;

ROLLBACK;
```

`RETURNING` shows the changed row. `ROLLBACK` undoes this trial. If the result is right, run the change again and `COMMIT` instead. A preview query and the later write can see different data when other sessions are active, so the write's `WHERE` clause and `RETURNING` result are the final checks.

Never assume a write affects one row just because you intended one row. A missing `WHERE` on `UPDATE` or `DELETE` can affect every row. A duplicate insert may fail on a unique rule, and an update can also fail a constraint. For changes that belong together, use one transaction so they either all commit or all roll back.

## Check your understanding

1. Which command changes a column's definition rather than one product's price?
2. What would the example leave in the table after `ROLLBACK`?
3. Why should the `RETURNING` result be checked even after a preview query?

## Further reading

- [PostgreSQL INSERT](https://www.postgresql.org/docs/current/sql-insert.html)
- [PostgreSQL UPDATE](https://www.postgresql.org/docs/current/sql-update.html)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
