# UPDATE

`UPDATE` changes columns in rows that match a condition. Write the condition carefully: without `WHERE`, PostgreSQL updates every row in the table.

## Change a known row

```sql
UPDATE products
SET price = 13.00,
    active = true
WHERE product_id = 7
RETURNING product_id, price, active;
```

`SET` names the new values. `WHERE` chooses the rows. `RETURNING` shows what was actually changed. If no row has ID 7, the update succeeds but returns no rows. If ID 7 is a primary key, at most one row can match.

An expression can use the old row value:

```sql
UPDATE products
SET price = price * 1.05
WHERE active = true
RETURNING product_id, price;
```

This raises the price of every active product by five percent. Running it twice raises prices twice. If the change should happen only once, record which products received it or use a migration with a clear one-time rule. Decide how money should be rounded before storing the new price in a fixed-scale column.

## Check the intended rows

Start with `SELECT product_id, price FROM products WHERE active = true;` to review the candidates. Then run the update inside a transaction and inspect `RETURNING` before committing. Other sessions can change data between the preview and update; a transaction alone does not freeze every possible change. If the current value matters, put that value in the `WHERE` clause or use an appropriate lock or version check.

PostgreSQL also supports `UPDATE ... FROM` to read another table. Make sure the join gives at most one source row per target row. If it gives several, PostgreSQL may choose one source row in a way you cannot predict. `SET price = NULL` is different from leaving `price` unchanged and may fail a `NOT NULL` rule.

## Check your understanding

1. What happens if the first query finds no row with ID 7?
2. Why is the five percent update unsafe to rerun without a one-time rule?
3. What problem appears when `UPDATE ... FROM` matches two source rows to one product?

## Further reading

- [PostgreSQL UPDATE](https://www.postgresql.org/docs/current/sql-update.html)
- [PostgreSQL explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html)
