# Case Conditional Logic

`CASE` chooses a result from a set of rules. It is an expression, so it can appear in a `SELECT` list, an `ORDER BY`, or inside an aggregate. It does not change stored data unless you use it in a write statement.

## Read rules from top to bottom

```sql
SELECT order_id, amount,
       CASE
         WHEN amount >= 100 THEN 'large'
         WHEN amount >= 50 THEN 'medium'
         ELSE 'small'
       END AS size_label
FROM orders;
```

An amount of 120 is `large`, not `medium`, even though both comparisons are true. `CASE` uses the first true `WHEN`. An amount of 50 is `medium`. A `NULL` amount reaches `ELSE` and becomes `small` in this query, which may be misleading. Add `WHEN amount IS NULL THEN 'unknown'` first if missing amounts need a separate label.

## Keep the output type clear

All result branches must be convertible to one output type. In the example, every branch returns text. For a numeric bonus, use numeric results in every branch:

```sql
SELECT employee_id,
       CASE WHEN active THEN salary * 0.10 ELSE 0 END AS bonus
FROM employees;
```

If `active` is `NULL`, the condition is not true and the result is zero here. Whether a missing active flag should count as inactive is a business decision.

## CASE compared with WHERE

`WHERE` removes rows. `CASE` keeps rows and chooses an output for each one. To count how many orders meet a rule while keeping all orders in the group, put `CASE` inside `SUM` or use PostgreSQL's aggregate `FILTER` clause.

## Check your understanding

1. What label does an amount of 120 get in the first query?
2. Why might `ELSE 'small'` be wrong for a missing amount?
3. Does adding a `CASE` expression remove rows from the result?

## Further reading

- [PostgreSQL CASE expression](https://www.postgresql.org/docs/current/functions-conditional.html#FUNCTIONS-CASE)
- [PostgreSQL aggregate FILTER syntax](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-AGGREGATES)
