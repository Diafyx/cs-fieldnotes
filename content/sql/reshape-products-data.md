# Reshape Products Data

A product table may keep regular and sale prices in separate columns. For a report that needs one row per price kind, take each column in its own query and combine the results with `UNION ALL`.

## The question

Return `product_id`, `product_name`, `price_type`, and `price`. Every product has a regular price. Add a sale-price row only when a sale price is present. Sort by product ID and price type.

```sql
CREATE TEMP TABLE products (
  product_id integer PRIMARY KEY,
  product_name text NOT NULL,
  regular_price numeric(10, 2) NOT NULL,
  sale_price numeric(10, 2)
);

INSERT INTO products
  (product_id, product_name, regular_price, sale_price) VALUES
  (1, 'Notebook', 12.00, 9.00),
  (2, 'Pen', 2.00, NULL),
  (3, 'Bag', 20.00, 20.00);
```

## A solution

```sql
SELECT product_id, product_name,
       'regular' AS price_type, regular_price AS price
FROM products
UNION ALL
SELECT product_id, product_name,
       'sale' AS price_type, sale_price AS price
FROM products
WHERE sale_price IS NOT NULL
ORDER BY product_id, price_type;
```

Notebook has regular 12 and sale 9. Pen has only regular 2. Bag has regular 20 and sale 20, so it has two rows even though the numbers are equal. The `price_type` values explain why those equal prices are separate facts. The output has five rows in total.

The branches return four columns in the same order and with matching types. A missing sale price means there is no sale-price row; it does not mean the sale price is zero. `UNION ALL` keeps the rows we ask for without an unneeded duplicate-removal step.

This is often called an *unpivot*: values stored across columns become rows. The result can be easier to chart or group by price type. It does not change the stored product table.

## Check your understanding

1. Why does Bag have two rows?
2. Why does Pen have no sale-price row?
3. Does this query update `products`?

## Further reading

- [PostgreSQL combining queries](https://www.postgresql.org/docs/current/queries-union.html)
- [PostgreSQL SELECT](https://www.postgresql.org/docs/current/sql-select.html)
