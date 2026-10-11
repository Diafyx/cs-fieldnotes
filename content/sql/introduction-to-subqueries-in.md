# Introduction to Subqueries (IN)

`IN (SELECT ...)` asks whether a value matches any value returned by the inner query. The subquery must return one column for a single-value comparison. Duplicate values in that result do not duplicate outer rows.

## Find customers with orders

```sql
WITH customers(customer_id, name) AS (
  VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara')
), orders(order_id, customer_id) AS (
  VALUES (10, 1), (11, 1), (12, 3)
)
SELECT c.customer_id, c.name
FROM customers AS c
WHERE c.customer_id IN (
  SELECT o.customer_id FROM orders AS o
)
ORDER BY c.customer_id;
```

The answer is Ana and Cara. Ana has two orders, but appears once because the outer query selects from `customers`. An inner query that returns no rows makes `IN` false for every outer row.

## Watch for NULL

If the outer value is `NULL`, or the inner result contains `NULL` with no match, `IN` can return unknown rather than false. A `WHERE` clause keeps only true rows. `NOT IN` is especially easy to misuse: one `NULL` in the inner result can prevent apparently unmatched rows from passing the filter. Use `NOT EXISTS` with a matching condition when you mean “there is no related row.”

`IN` can also compare row values, such as `(department_id, salary) IN (SELECT department_id, MAX(salary) ... )`. Each side must have the same number of columns. Think through `NULL` and ties before using row comparisons for a final answer.

## Check your understanding

1. Why does Ana appear once despite two orders?
2. What happens when the inner query returns no rows?
3. Why can `NOT IN` fail to show an unmatched customer when the inner result contains `NULL`?

## Further reading

- [PostgreSQL IN and NOT IN subqueries](https://www.postgresql.org/docs/current/functions-subquery.html)
