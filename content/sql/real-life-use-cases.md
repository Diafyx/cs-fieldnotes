# Real-Life Use Cases

Window functions are useful when a report needs each row plus facts about nearby rows or its group. A customer order report can show a running spend, the prior order amount, and each order's position from newest to oldest without losing order rows.

## One report, three questions

```sql
WITH orders(customer_id, order_id, ordered_at, amount) AS (
  VALUES (1, 1, '2026-01-01', 10),
         (1, 2, '2026-01-02', 20),
         (1, 3, '2026-01-03', 15),
         (2, 4, '2026-01-01', 5),
         (2, 5, '2026-01-02', 7)
)
SELECT customer_id, order_id, amount,
       ROW_NUMBER() OVER (
         PARTITION BY customer_id ORDER BY ordered_at DESC, order_id DESC
       ) AS recent_position,
       LAG(amount) OVER (
         PARTITION BY customer_id ORDER BY ordered_at, order_id
       ) AS previous_amount,
       SUM(amount) OVER (
         PARTITION BY customer_id ORDER BY ordered_at, order_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_spend
FROM orders
ORDER BY customer_id, ordered_at, order_id;
```

For customer 1, the three rows have recent positions `3, 2, 1`, previous amounts `NULL, 10, 20`, and running spend `10, 30, 45`. Customer 2 starts its own sequence: positions `2, 1`, previous amounts `NULL, 5`, and running spend `5, 12`. `PARTITION BY customer_id` keeps the customers separate.

Choose the order that matches each question. Recency sorts newest first, while prior amount and running spend sort oldest first. The order ID settles same-day ties. If you need only the two newest orders, place this query in a CTE and filter `recent_position <= 2` outside it. Filtering the source first would change the running spend.

Window calculations can require sorting many rows. For a large table, inspect the plan and consider an index that starts with the partition key and then the order keys. Measure on real data; an index is not a promise that every window sort disappears. A rolling seven-calendar-day result also needs calendar logic when dates are missing, since a row frame counts rows.

## Check your understanding

1. Why does customer 2's running spend start at 5 rather than 50?
2. Why do the recency and running-spend windows order rows in opposite directions?
3. Where should a top-two filter go if running spend must include older orders?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL query plans](https://www.postgresql.org/docs/current/using-explain.html)
