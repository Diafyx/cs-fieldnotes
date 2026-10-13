# Introduction to Situation-Based Questions

A situation question gives you a small story and asks what the data should show. The hard part is often deciding what one answer row means. Once that is clear, the SQL becomes easier to write and check.

The topic inventory names the next exercises only `Situation-1` through `Situation-15`. It does not give their question text. The cases on this site are original practice questions for those slots, not copies of an unseen question.

## A useful way to answer

1. Say what one output row represents. It might be a customer, an order, or a month.
2. Say which rows qualify. Define words such as "active," "paid," or "latest."
3. Check table relationships. A customer can have many orders, and an order can have many payment attempts.
4. Write the query. Give ties, missing values, and date boundaries a rule.
5. Check a tiny data set by hand. Include a row that should be excluded.

Here is a small PostgreSQL example. The question is: how many customers placed at least one order?

```sql
WITH orders(order_id, customer_id) AS (
  VALUES (10, 1), (11, 1), (12, 2)
)
SELECT COUNT(DISTINCT customer_id) AS customer_count
FROM orders;
```

The answer is `2`, not `3`. There are three orders, but customer 1 placed two of them. This is the first check to make in an interview: does the query count the thing the question asked for?

## Questions to settle before coding

If the prompt is vague, state an assumption and ask whether it matches the intended rule. Does "latest" mean latest event time or largest ID? Do failed payments count? Can a field be `NULL`? Should a customer with no orders appear with zero? A short question here can save a wrong query.

After writing SQL, explain one result row in plain words. Then test a duplicate, a missing match, a `NULL`, and a value at the boundary if they matter. If the query is correct but slow, inspect its plan and the size of each intermediate result before suggesting an index.

## Check your understanding

1. What does one row represent when a report asks for revenue per customer per month?
2. Why does the example return two customers even though it has three orders?
3. What would you ask if a prompt says "show recent customers" without defining recent?

## Further reading

- [PostgreSQL SELECT](https://www.postgresql.org/docs/current/sql-select.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
