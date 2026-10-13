# Situation-11

## The question

A product's price changes over time. An order must use the price that was valid on its order date, not today's price. Return each order with its unit price and line total. Keep orders for which no price is known so they can be investigated.

Each price row covers `valid_from` and stops just before `valid_to`. A `NULL` end means the price is still current.

```sql
CREATE TEMP TABLE price_history (
  product_id integer NOT NULL,
  valid_from date NOT NULL,
  valid_to date,
  unit_price numeric(10, 2) NOT NULL CHECK (unit_price >= 0),
  PRIMARY KEY (product_id, valid_from),
  CHECK (valid_to IS NULL OR valid_to > valid_from)
);
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  product_id integer NOT NULL,
  ordered_on date NOT NULL,
  quantity integer NOT NULL CHECK (quantity > 0)
);

INSERT INTO price_history VALUES
  (1, '2026-01-01', '2026-02-01', 10.00),
  (1, '2026-02-01', NULL, 12.00),
  (2, '2026-01-01', '2026-01-10', 5.00);
INSERT INTO orders VALUES
  (101, 1, '2026-01-31', 2),
  (102, 1, '2026-02-01', 3),
  (103, 2, '2026-01-15', 1);
```

## Work through it

Match the product and the date range. Use a left join so an order with no matching price stays visible.

```sql
SELECT o.order_id, p.unit_price,
       o.quantity * p.unit_price AS line_total
FROM orders AS o
LEFT JOIN price_history AS p
  ON p.product_id = o.product_id
 AND o.ordered_on >= p.valid_from
 AND (p.valid_to IS NULL OR o.ordered_on < p.valid_to)
ORDER BY o.order_id;
```

Order 101 has price 10.00 and total 20.00. Order 102 falls exactly on February 1, so it has price 12.00 and total 36.00. Order 103 remains in the result with `NULL` price and total. Do not silently treat that missing price as zero.

The query assumes that a product's price periods do not overlap. If they do, one order can match two prices and appear twice. This check finds overlapping periods that start on different dates:

```sql
SELECT a.product_id, a.valid_from AS first_start, b.valid_from AS second_start
FROM price_history AS a
JOIN price_history AS b
  ON a.product_id = b.product_id
 AND a.valid_from < b.valid_from
 AND (a.valid_to IS NULL OR b.valid_from < a.valid_to)
ORDER BY a.product_id, a.valid_from, b.valid_from;
```

It returns no rows for the sample data. A primary key prevents two periods with the same start but does not prevent overlap with different starts. In PostgreSQL, a range exclusion constraint can enforce nonoverlap when the schema is designed for it. Also decide how price corrections affect old orders. Many shops store the charged unit price on the order line so later changes to price history do not change past receipts.

## Check your understanding

1. Why does order 102 use the second price period?
2. What would an inner join do to order 103?
3. Why is a primary key on `(product_id, valid_from)` not enough to stop overlapping prices?

## Further reading

- [PostgreSQL range types and exclusion constraints](https://www.postgresql.org/docs/current/rangetypes.html)
- [PostgreSQL joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
