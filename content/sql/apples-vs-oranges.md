# Apples vs Oranges

This exercise compares daily apple and orange sales. For each day, subtract orange units from apple units. A positive result means more apples were sold. A negative result means more oranges were sold.

## The question

Each row in `fruit_sales` records a quantity sold. Return every sale day and `apple_minus_orange`, sorted by day. Other fruit types contribute zero to this comparison.

```sql
CREATE TEMP TABLE fruit_sales (
  sale_id integer PRIMARY KEY,
  sale_day date NOT NULL,
  fruit text NOT NULL,
  quantity integer NOT NULL
);

INSERT INTO fruit_sales (sale_id, sale_day, fruit, quantity) VALUES
  (1, '2026-01-01', 'apple', 10),
  (2, '2026-01-01', 'orange', 4),
  (3, '2026-01-01', 'banana', 100),
  (4, '2026-01-02', 'orange', 3),
  (5, '2026-01-03', 'apple', 2),
  (6, '2026-01-03', 'orange', 5);
```

## A solution

```sql
SELECT sale_day,
       SUM(CASE
             WHEN fruit = 'apple' THEN quantity
             WHEN fruit = 'orange' THEN -quantity
             ELSE 0
           END) AS apple_minus_orange
FROM fruit_sales
GROUP BY sale_day
ORDER BY sale_day;
```

The daily results are 6, -3, and -3. On January 1, ten apples minus four oranges is six. Banana sales do not change the comparison. On January 2, there are no apple rows, so the three oranges make the result negative three.

This assumes `quantity` is present and non-negative. If returns are stored as negative quantities, they change the result and need a stated rule. A day with only bananas would appear with zero; if the report should show only days with apples or oranges, filter those rows before grouping.

## Check your understanding

1. Why does January 2 have a negative result?
2. What would happen if the `ELSE 0` branch were omitted for a day with only bananas?
3. How could returned items affect the calculation?

## Further reading

- [PostgreSQL CASE expression](https://www.postgresql.org/docs/current/functions-conditional.html#FUNCTIONS-CASE)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
