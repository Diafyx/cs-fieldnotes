# Valid Triangle Check

Three positive lengths make a triangle only when the sum of every two lengths is greater than the third. Equality is not enough: a flat shape has no area.

## The question

For each row, return the lengths and `Yes` or `No` in a `triangle` column. The sample includes a valid triangle, a flat case, a zero length, and three equal lengths.

```sql
CREATE TEMP TABLE side_sets (
  set_id integer PRIMARY KEY,
  x integer NOT NULL,
  y integer NOT NULL,
  z integer NOT NULL
);

INSERT INTO side_sets (set_id, x, y, z) VALUES
  (1, 3, 4, 5),
  (2, 1, 2, 3),
  (3, 0, 3, 3),
  (4, 5, 5, 5);
```

## A solution

```sql
SELECT set_id, x, y, z,
       CASE
         WHEN x > 0 AND y > 0 AND z > 0
          AND x + y > z
          AND x + z > y
          AND y + z > x THEN 'Yes'
         ELSE 'No'
       END AS triangle
FROM side_sets
ORDER BY set_id;
```

The answers are `Yes`, `No`, `No`, and `Yes` for sets 1 through 4. Set 2 fails because 1 + 2 equals 3. Set 3 fails because one length is zero, even though some sum checks might pass.

For positive lengths, checking the largest side against the sum of the other two is enough. The three comparisons above state the full rule without first sorting the lengths. If lengths can be `NULL`, decide whether the answer should be `unknown` instead of `No`; this sample forbids missing lengths.

## Check your understanding

1. Why does `(1, 2, 3)` fail?
2. Why are positive-length checks included?
3. What should a real report say if one length is missing?

## Further reading

- [LeetCode Triangle Judgement](https://leetcode.com/problems/triangle-judgement/)
- [PostgreSQL CASE expression](https://www.postgresql.org/docs/current/functions-conditional.html#FUNCTIONS-CASE)
