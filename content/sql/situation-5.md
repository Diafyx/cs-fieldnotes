# Situation-5

## The question

Return the most recent activity row for each customer who has activity. If two rows have the same activity time, choose the row with the larger `activity_id`. Return the customer ID, activity ID, and activity time. Sort by customer ID.

```sql
CREATE TEMP TABLE activity (
  activity_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  happened_at timestamp NOT NULL
);

INSERT INTO activity VALUES
  (10, 1, '2026-01-10 09:00:00'),
  (11, 1, '2026-01-12 10:00:00'),
  (12, 1, '2026-01-12 10:00:00'),
  (20, 2, '2026-01-11 08:00:00');
```

Customer 1's latest time is shared by activities 11 and 12, so the stated tie rule picks 12. Customer 2 has only activity 20.

## Work through it

Number each customer's rows from newest to oldest. Include the activity ID in the sort so the choice is stable when times tie.

```sql
WITH ranked AS (
  SELECT customer_id, activity_id, happened_at,
         ROW_NUMBER() OVER (
           PARTITION BY customer_id
           ORDER BY happened_at DESC, activity_id DESC
         ) AS position
  FROM activity
)
SELECT customer_id, activity_id, happened_at
FROM ranked
WHERE position = 1
ORDER BY customer_id;
```

The result has `(1, 12, 2026-01-12 10:00:00)` and `(2, 20, 2026-01-11 08:00:00)`. `PARTITION BY` starts the numbering again for each customer. The outer query keeps the first row from each group.

`MAX(happened_at)` alone finds the latest time but does not choose one full activity row. Joining rows back on that time would return both 11 and 12 for customer 1. The larger ID is a tie breaker chosen by this question; it does not prove that activity 12 happened later in real time. If the product needs a true event order, store an ordering value with that meaning.

Customers with no activity are absent because the query starts from `activity`. To include them, start from a customer table and left join the chosen activity row.

## Check your understanding

1. Why does customer 1 have one output row rather than two?
2. What would happen if the tie rule were removed?
3. How would you change the query to return every row tied for the latest time?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL SELECT](https://www.postgresql.org/docs/current/sql-select.html)
