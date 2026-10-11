# Product Selling Price Report

A product's price can change over time. To report what buyers actually paid, match each sale date to the price period in force that day. Weight the price by units sold.

## The question

Return each product's average selling price, rounded to two decimal places. Show zero for a product with no sales under this report's rule. Price periods are inclusive, do not overlap for a product, and cover every sale.

```sql
CREATE TEMP TABLE products (
  product_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE price_history (
  product_id integer NOT NULL,
  starts_on date NOT NULL,
  ends_on date NOT NULL,
  price numeric(10, 2) NOT NULL
);
CREATE TEMP TABLE sold_units (
  sale_id integer PRIMARY KEY,
  product_id integer NOT NULL,
  sold_on date NOT NULL,
  units integer NOT NULL CHECK (units > 0)
);

INSERT INTO products VALUES (1, 'Pen'), (2, 'Book'), (3, 'Bag');
INSERT INTO price_history VALUES
  (1, '2026-01-01', '2026-01-10', 2.00),
  (1, '2026-01-11', '2026-01-31', 3.00),
  (2, '2026-01-01', '2026-01-31', 10.00);
INSERT INTO sold_units VALUES
  (100, 1, '2026-01-05', 10),
  (101, 1, '2026-01-20', 5),
  (102, 2, '2026-01-03', 2);
```

## A solution

```sql
SELECT p.product_id,
       COALESCE(
         ROUND(1.0 * SUM(s.units * h.price) /
               NULLIF(SUM(s.units), 0), 2),
         0
       ) AS average_price
FROM products AS p
LEFT JOIN sold_units AS s ON s.product_id = p.product_id
LEFT JOIN price_history AS h
  ON h.product_id = s.product_id
 AND s.sold_on BETWEEN h.starts_on AND h.ends_on
GROUP BY p.product_id
ORDER BY p.product_id;
```

Pen sold ten units at 2 and five at 3, so its average is `(10 * 2 + 5 * 3) / 15`, or 2.33. Book's average is 10.00. Bag has no sales and shows 0 by the question's display rule. `NULLIF` avoids division by zero for a product with no units.

The price periods must not overlap. If one sale matches two periods, its units and amount are both counted twice. A sale with no matching period is also a data error; this query's denominator would still count its units while its price is missing. Check price coverage and period rules before trusting a real report.

## Check your understanding

1. Why is Pen's average weighted by units instead of averaging 2 and 3?
2. What happens if two price periods both include January 5?
3. Why must every sale have a matching price period?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
