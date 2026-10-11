# Boolean Expression Evaluator

Each expression names two stored variables and one comparison operator. Return whether that comparison is true. This example supports only `=`, `>`, and `<` on integer values.

## Sample data

```sql
CREATE TEMP TABLE variables (name text PRIMARY KEY, value integer NOT NULL);
CREATE TEMP TABLE expressions (
  expression_id integer PRIMARY KEY,
  left_name text NOT NULL,
  operator text NOT NULL,
  right_name text NOT NULL
);
INSERT INTO variables VALUES ('X', 1), ('Y', 0);
INSERT INTO expressions VALUES
  (1, 'X', '=', 'Y'), (2, 'X', '>', 'Y'),
  (3, 'Y', '<', 'X'), (4, 'X', '=', 'X');
```

## Solution

```sql
SELECT e.expression_id,
       CASE
         WHEN e.operator NOT IN ('=', '>', '<') THEN NULL
         WHEN (e.operator = '=' AND l.value = r.value)
           OR (e.operator = '>' AND l.value > r.value)
           OR (e.operator = '<' AND l.value < r.value) THEN 'true'
         ELSE 'false'
       END AS result
FROM expressions AS e
JOIN variables AS l ON l.name = e.left_name
JOIN variables AS r ON r.name = e.right_name
ORDER BY e.expression_id;
```

The results are `false`, `true`, `true`, and `true` for expression IDs 1 through 4. The two joins look up each named variable. The `CASE` chooses the requested comparison. An unsupported operator returns `NULL` instead of being silently treated as false.

An expression with a missing variable disappears because these are inner joins. If that is possible, use left joins and report missing names as invalid input. Do not build SQL text from an untrusted operator; a fixed `CASE` like this keeps the allowed operations explicit.

## Check your understanding

1. Why does `X = Y` return false?
2. What happens if an expression names an absent variable?
3. Why is an unknown operator different from a valid comparison that returns false?

## Further reading

- [PostgreSQL CASE](https://www.postgresql.org/docs/current/functions-conditional.html)
- [PostgreSQL joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
