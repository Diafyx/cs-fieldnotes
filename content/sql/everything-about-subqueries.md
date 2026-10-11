# Everything about Subqueries

A subquery is a `SELECT` inside another SQL statement. The inner query can supply one value, a set of values, or a table of rows. Start by asking what shape the outer query needs.

## Three useful shapes

Suppose `orders` has `customer_id` and `amount` columns:

```sql
WITH orders(customer_id, amount) AS (
  VALUES (1, 20), (1, 40), (2, 10)
)
SELECT customer_id, amount
FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders)
ORDER BY customer_id, amount;
```

The inner aggregate returns one value, about 23.33. Only `(1, 40)` is above it. This is a **scalar subquery**. It must return one column and at most one row. No rows give `NULL`; more than one row is an error in PostgreSQL.

Use `IN (SELECT ...)` when the inner query returns a set of one-column values. Use `EXISTS (SELECT ...)` when only the presence of a matching row matters. A subquery in `FROM` acts like a table and should have an alias. A subquery in `SELECT` can compute a value for each output row. The inner query can also refer to a column from the outer query; that is a correlated subquery.

## Choose a form for the question

`IN` is good for membership. `EXISTS` is good for checking whether a related row exists and does not duplicate the outer row when several matches exist. `NOT EXISTS` is usually easier to reason about than `NOT IN` when the inner column may contain `NULL`. A join can be clearer when you need columns from both sides. A window function can be clearer for ranking rows within groups. These are choices about meaning first; use `EXPLAIN` on real data when speed matters.

Parentheses show where the inner query begins and ends. Always qualify columns in a correlated query so a new column in the inner table cannot silently change what a name means. Add `ORDER BY` when the result needs a predictable order. An inner `ORDER BY` alone does not order the outer result.

## Check your understanding

1. What happens if a scalar subquery returns two rows?
2. Which form asks only whether a related row is present?
3. Why does `ORDER BY` inside a subquery not promise the order of the final rows?

## Further reading

- [PostgreSQL subquery expressions](https://www.postgresql.org/docs/current/functions-subquery.html)
- [PostgreSQL scalar subqueries](https://www.postgresql.org/docs/current/sql-expressions.html#SQL-SYNTAX-SCALAR-SUBQUERIES)
- [PostgreSQL table expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html)
