# CASE Basics

`CASE` has two common forms. A searched `CASE` checks full conditions. A simple `CASE` compares one expression to a list of values. Both return the result beside the first match.

## Searched CASE

```sql
SELECT score,
       CASE
         WHEN score IS NULL THEN 'not graded'
         WHEN score >= 80 THEN 'high'
         WHEN score >= 50 THEN 'middle'
         ELSE 'low'
       END AS band
FROM exams;
```

For scores 85, 50, 20, and `NULL`, the labels are `high`, `middle`, `low`, and `not graded`. The order matters: the 80 rule must come before the 50 rule.

## Simple CASE

```sql
SELECT status,
       CASE status
         WHEN 'P' THEN 'pending'
         WHEN 'S' THEN 'shipped'
         ELSE 'other'
       END AS status_label
FROM orders;
```

This form is useful for exact matches. It cannot directly express `score >= 80`; use searched `CASE` for ranges. A `NULL` status does not equal a `WHEN NULL` value. Use searched `CASE` with `IS NULL` when missing status needs its own branch.

## ELSE and result types

Without `ELSE`, an unmatched row gets `NULL`. That may be right, but it should be intentional. Each `THEN` and `ELSE` result must fit one common type. Mixing text labels with numeric results usually causes a type error or unwanted conversion.

`CASE` returns one value per input row. It does not create extra rows. Name the result with `AS` so the output is easy to read.

## Check your understanding

1. Which form of `CASE` fits a score range?
2. What does an unmatched row return when `ELSE` is omitted?
3. Why does `WHEN NULL` in a simple `CASE` not find missing values?

## Further reading

- [PostgreSQL CASE expression](https://www.postgresql.org/docs/current/functions-conditional.html#FUNCTIONS-CASE)
