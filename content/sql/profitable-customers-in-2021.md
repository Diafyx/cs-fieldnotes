# Profitable Customers in 2021

This practice question asks for customers whose recorded profit was greater than zero in 2021. It needs two row filters: the year and the profit amount. Here, profit means income minus cost. Revenue alone would not tell us whether a customer was profitable.

## The question

Each row in `customer_profit` gives one customer's profit for one year. Return only `customer_id` for customers with positive profit in 2021. A zero profit does not count. A missing profit does not count. Sort by `customer_id` for a stable result.

```sql
CREATE TEMP TABLE customer_profit (
  customer_id integer NOT NULL,
  year integer NOT NULL,
  profit numeric(12, 2),
  PRIMARY KEY (customer_id, year)
);

INSERT INTO customer_profit (customer_id, year, profit) VALUES
  (1, 2020, 90.00),
  (1, 2021, 15.00),
  (2, 2021, -4.00),
  (3, 2021, 0.00),
  (4, 2021, 100.00),
  (5, 2021, NULL),
  (6, 2020, 40.00);
```

## A solution

```sql
SELECT customer_id
FROM customer_profit
WHERE year = 2021
  AND profit > 0
ORDER BY customer_id;
```

The output is customer IDs 1 and 4. Customer 2 lost money. Customer 3 broke even. Customer 5 has no known profit. Customer 6 has profit in 2020, but no 2021 row.

The primary key makes each `(customer_id, year)` pair unique, so the query cannot return the same customer twice for 2021. Without that rule, you would need to decide whether the task means any profitable row or a positive sum across the year. Those are different questions.

## Check your understanding

1. Why does a profit of zero fail `profit > 0`?
2. Would customer 6 pass if the year filter were removed?
3. If the table held monthly profits, what extra step would be needed to find customers with positive annual profit?

## Further reading

- [PostgreSQL WHERE clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-WHERE)
- [PostgreSQL numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html)
