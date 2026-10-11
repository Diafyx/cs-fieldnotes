# Combine Sales Records Without Deduplication

Two sales sources can report rows that look the same. If each row represents a real sale, removing repeated rows would undercount sales. Combine the rows with `UNION ALL` before calculating totals.

## The question

Return one row per product with its sale count and total amount across web and market sales. Each input row is one sale. IDs are only unique inside their own source.

```sql
CREATE TEMP TABLE web_sales (
  sale_id integer PRIMARY KEY,
  product text NOT NULL,
  amount numeric(10, 2) NOT NULL
);

CREATE TEMP TABLE market_sales (
  sale_id integer PRIMARY KEY,
  product text NOT NULL,
  amount numeric(10, 2) NOT NULL
);

INSERT INTO web_sales (sale_id, product, amount) VALUES
  (1, 'Pen', 10.00),
  (2, 'Pen', 10.00),
  (3, 'Book', 30.00);

INSERT INTO market_sales (sale_id, product, amount) VALUES
  (1, 'Pen', 10.00),
  (2, 'Book', 30.00);
```

## A solution

```sql
WITH all_sales AS (
  SELECT product, amount FROM web_sales
  UNION ALL
  SELECT product, amount FROM market_sales
)
SELECT product,
       COUNT(*) AS sale_count,
       SUM(amount) AS total_amount
FROM all_sales
GROUP BY product
ORDER BY product;
```

The result is `('Book', 2, 60.00)` and `('Pen', 3, 30.00)`. The three Pen rows have the same selected values, but they represent three sales. `UNION` would remove repeated `(product, amount)` rows before counting and give the wrong totals.

The table rule says each row is a real sale. If a data import copied the same sale twice by mistake, `UNION ALL` would count it twice. In that case, identify duplicates by a real sale key such as `(source, sale_id)` and repair the input. Deduplicating only by product and amount can wrongly remove separate purchases of the same item at the same price.

## Check your understanding

1. Why does Pen have a count of three?
2. Why would `UNION` give a wrong count here?
3. Which columns could identify a sale when IDs are only unique within a source?

## Further reading

- [PostgreSQL combining queries](https://www.postgresql.org/docs/current/queries-union.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
