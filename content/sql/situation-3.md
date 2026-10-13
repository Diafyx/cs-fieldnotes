# Situation-3

## The question

A feedback table has one row per submitted form. A rating may be missing. Report the number of forms, the number with a rating, and the average of the ratings that were given.

```sql
CREATE TEMP TABLE feedback (
  form_id integer PRIMARY KEY,
  rating smallint CHECK (rating BETWEEN 1 AND 5)
);

INSERT INTO feedback VALUES (1, 5), (2, NULL), (3, 1);
```

There are three forms. Two have ratings, 5 and 1. Their average is 3.

## Work through it

`COUNT(*)` counts rows. `COUNT(rating)` counts non-null ratings. `AVG(rating)` also skips `NULL` values.

```sql
SELECT COUNT(*) AS form_count,
       COUNT(rating) AS rated_count,
       AVG(rating) AS average_rating
FROM feedback;
```

The result is one row: `3`, `2`, and `3`. PostgreSQL returns a numeric value for the average of integer ratings. The displayed number of decimal places depends on the client.

Do not replace a missing rating with zero unless the question says it means a zero rating. This table allows ratings from 1 to 5, so zero is not even a valid rating. If every rating is `NULL`, `AVG(rating)` returns `NULL`, not zero, because there is no value to average. If the table has no rows, the counts are zero and the average is also `NULL`.

If forms may be duplicated during import, the primary key in this sample stops duplicate `form_id` values. Without a reliable form key, `COUNT(*)` may count repeated imports as separate forms. Decide how to identify a real submission before fixing the count with `DISTINCT`.

## Check your understanding

1. What happens to the average if another form with no rating is added?
2. Why is `COUNT(rating)` smaller than `COUNT(*)` here?
3. What does `AVG(rating)` return if all forms have missing ratings?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL null values](https://www.postgresql.org/docs/current/ddl-constraints.html)
