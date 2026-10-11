# All-Product Buyers

Find customers who have bought every product in the catalog. A customer can buy a product more than once. The question is about coverage, not the number of purchases.

## Sample data

```sql
CREATE TEMP TABLE customers (customer_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE products (product_id integer PRIMARY KEY);
CREATE TEMP TABLE purchases (customer_id integer, product_id integer);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara');
INSERT INTO products VALUES (10), (20);
INSERT INTO purchases VALUES (1, 10), (1, 20), (2, 10), (2, 10);
```

## Solution

```sql
SELECT c.customer_id, c.name
FROM customers AS c
WHERE NOT EXISTS (
  SELECT 1
  FROM products AS p
  WHERE NOT EXISTS (
    SELECT 1
    FROM purchases AS b
    WHERE b.customer_id = c.customer_id
      AND b.product_id = p.product_id
  )
)
ORDER BY c.customer_id;
```

The answer is Ana. Read the double negative as “there is no product for which this customer has no purchase.” Ben bought product 10 twice but never product 20. Cara has no purchases.

If `products` is empty, every customer passes because there is no missing product. That follows the usual meaning of “every” over an empty set. A business rule may instead require at least one catalog product or at least one purchase. Add that rule explicitly if needed. `NULL` product IDs in purchases do not match a catalog product.

## Check your understanding

1. Why does Ben fail despite two purchase rows?
2. What does the inner `NOT EXISTS` test?
3. What happens when the product catalog is empty?

## Further reading

- [PostgreSQL EXISTS subqueries](https://www.postgresql.org/docs/current/functions-subquery.html#FUNCTIONS-SUBQUERY-EXISTS)
