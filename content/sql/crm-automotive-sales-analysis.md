# CRM Automotive Sales Analysis

This exercise reports completed car sales in 2025. For each model, it shows the number of sales, total sale amount, and number of unique customers. The rules below say exactly which records count.

## The question

Each row in `car_sales` is one sale record. `sale_amount` uses one currency throughout the sample. Exclude refunded records and sales outside 2025. Return `model`, `sales_count`, `total_amount`, and `customer_count`, sorted by model.

```sql
CREATE TEMP TABLE car_sales (
  sale_id integer PRIMARY KEY,
  model text NOT NULL,
  sold_on date NOT NULL,
  status text NOT NULL,
  customer_id integer NOT NULL,
  sale_amount numeric(12, 2) NOT NULL
);

INSERT INTO car_sales
    (sale_id, model, sold_on, status, customer_id, sale_amount) VALUES
  (1, 'sedan', '2025-01-05', 'completed', 1, 20000.00),
  (2, 'sedan', '2025-03-01', 'completed', 2, 21000.00),
  (3, 'suv', '2025-04-02', 'completed', 3, 30000.00),
  (4, 'suv', '2025-05-06', 'refunded', 3, 30000.00),
  (5, 'sedan', '2024-12-30', 'completed', 1, 19000.00),
  (6, 'suv', '2025-08-01', 'completed', 3, 31000.00),
  (7, 'hatch', '2025-10-01', 'completed', 4, 15000.00);
```

## A solution

```sql
SELECT model,
       COUNT(*) AS sales_count,
       SUM(sale_amount) AS total_amount,
       COUNT(DISTINCT customer_id) AS customer_count
FROM car_sales
WHERE status = 'completed'
  AND sold_on >= '2025-01-01'
  AND sold_on < '2026-01-01'
GROUP BY model
ORDER BY model;
```

The output is `hatch: 1 sale, 15000, 1 customer`; `sedan: 2 sales, 41000, 2 customers`; and `suv: 2 sales, 61000, 1 customer`. The same customer bought two SUVs, so the SUV customer count is one. The refunded sale and the 2024 sale are left out before grouping.

Real CRM reports need firmer rules. Decide whether a refund is a separate negative amount or a status on the original sale. Decide whether sale amounts include tax, discounts, and fees. If currencies differ, do not add their amounts without conversion. A summary can be numerically correct and still answer the wrong business question if those rules are missing.

## Check your understanding

1. Why is the SUV sales count two but its customer count one?
2. What would happen if the status filter were removed?
3. Why is a separate currency rule needed before summing sales from several countries?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL WHERE and GROUP BY](https://www.postgresql.org/docs/current/sql-select.html)
