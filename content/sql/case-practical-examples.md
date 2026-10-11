# CASE Practical Examples

Use `CASE` when a report needs a value chosen from clear rules. The rules might label rows, calculate a price, or count selected rows inside a group. Write down the rule before writing the SQL.

## Put a label on each row

```sql
SELECT ticket_id, priority,
       CASE
         WHEN priority = 'urgent' THEN 'respond today'
         WHEN priority = 'normal' THEN 'respond this week'
         ELSE 'review priority'
       END AS next_step
FROM tickets;
```

The `ELSE` branch catches missing or unexpected priorities. Without it, those rows would receive `NULL`, which might disappear in a screen or report.

## Calculate a conditional amount

```sql
SELECT order_id, subtotal,
       CASE
         WHEN subtotal >= 100 THEN subtotal * 0.90
         ELSE subtotal
       END AS amount_after_discount
FROM orders;
```

This applies a ten percent discount to orders of at least 100. It only displays a calculated value. It does not update an order. Decide how to round money and whether tax is computed before or after the discount before using this in a real checkout.

## Count a condition inside each group

```sql
SELECT customer_id,
       COUNT(*) AS all_orders,
       SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END) AS paid_orders
FROM orders
GROUP BY customer_id;
```

Every order counts in `all_orders`. Only paid orders add one to `paid_orders`. A missing status adds zero because its comparison is not true. PostgreSQL can also write the second count as `COUNT(*) FILTER (WHERE status = 'paid')`.

## Check your understanding

1. What happens to an unexpected priority in the first query?
2. Does the discount query change stored prices?
3. Why does the last query keep customers who have no paid orders?

## Further reading

- [PostgreSQL CASE and COALESCE](https://www.postgresql.org/docs/current/functions-conditional.html)
- [PostgreSQL aggregate FILTER syntax](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-AGGREGATES)
