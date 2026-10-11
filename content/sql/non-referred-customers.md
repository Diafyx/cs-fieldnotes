# Non-Referred Customers

The title can mean two different things: customers with no referrer at all, or customers who were not referred by one particular person. This exercise uses the second meaning. It asks for customers who were not referred by customer 2, including customers with no referrer.

## The question

The `customers` table stores each person's ID, name, and optional `referee_id`. Return the names of customers whose `referee_id` is not 2 or is missing. Sort by name.

```sql
CREATE TEMP TABLE customers (
  id integer PRIMARY KEY,
  name text NOT NULL,
  referee_id integer
);

INSERT INTO customers (id, name, referee_id) VALUES
  (1, 'Anya', NULL),
  (2, 'Ben', NULL),
  (3, 'Cara', 2),
  (4, 'Dev', 1),
  (5, 'Eli', 2),
  (6, 'Faye', NULL);
```

## A solution

```sql
SELECT name
FROM customers
WHERE referee_id <> 2
   OR referee_id IS NULL
ORDER BY name;
```

The output is Anya, Ben, Dev, and Faye. Cara and Eli were referred by customer 2. Dev was referred by someone else. The other three have no recorded referrer.

`referee_id <> 2` alone would drop Anya, Ben, and Faye. A comparison with `NULL` is unknown, so the `OR referee_id IS NULL` part is needed. PostgreSQL can state the same test as `referee_id IS DISTINCT FROM 2`.

If the question truly means "customers with no referrer," use only `WHERE referee_id IS NULL`. That returns Anya, Ben, and Faye, but not Dev. Read the requested meaning before choosing a filter.

## Check your understanding

1. Why does Dev appear in the main solution?
2. What result would `WHERE referee_id IS NULL` give?
3. Why does `referee_id <> 2` alone miss customers with no referrer?

## Further reading

- [LeetCode Find Customer Referee problem](https://leetcode.com/problems/find-customer-referee/)
- [PostgreSQL NULL comparisons](https://www.postgresql.org/docs/current/functions-comparison.html)
