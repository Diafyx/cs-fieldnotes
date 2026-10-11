# Sales Analysis

A product report often needs sales totals beside every product, including products that have never sold. Join from products to sale items and group the result.

## The question

Return each product's sold units and revenue. An unsold product should show zero for both. Use the price stored on each sale item, since a product's current price can change later.

```sql
CREATE TEMP TABLE products (
  product_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE sale_items (
  sale_item_id integer PRIMARY KEY,
  product_id integer NOT NULL,
  quantity integer NOT NULL,
  unit_price numeric(10, 2) NOT NULL
);

INSERT INTO products VALUES (1, 'Pen'), (2, 'Book'), (3, 'Bag');
INSERT INTO sale_items VALUES
  (10, 1, 3, 2.00),
  (11, 1, 2, 2.50),
  (12, 2, 1, 10.00);
```

## A solution

```sql
SELECT p.product_id, p.name,
       COALESCE(SUM(i.quantity), 0) AS units_sold,
       COALESCE(SUM(i.quantity * i.unit_price), 0) AS revenue
FROM products AS p
LEFT JOIN sale_items AS i ON i.product_id = p.product_id
GROUP BY p.product_id, p.name
ORDER BY p.product_id;
```

The result is Pen with 5 units and 11.00 revenue, Book with 1 and 10.00, and Bag with 0 and 0. Pen revenue is `3 * 2.00 + 2 * 2.50`. Bag has no sale item, so the sums are `NULL` before `COALESCE` changes them to zero for this report.

If you join sale items to another one-to-many table before summing, the same sale item may appear several times and revenue will be too high. Aggregate at the needed level first. Returns, discounts, tax, and currency need separate rules before this becomes a financial report.

## Check your understanding

1. Why is Pen revenue 11.00 instead of 10.00?
2. Why does Bag still appear?
3. How could joining each sale item to several tags change the total?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
