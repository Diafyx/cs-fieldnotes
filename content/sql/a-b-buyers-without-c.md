# A & B Buyers Without C

This exercise finds users who bought both products A and B but never bought C. Self joins on purchases can prove the first two facts; a left join can rule out C.

## The question

Return matching user IDs once, sorted by ID. A user may buy the same product more than once.

```sql
CREATE TEMP TABLE purchases (
  purchase_id integer PRIMARY KEY,
  user_id integer NOT NULL,
  product text NOT NULL
);

INSERT INTO purchases VALUES
  (1, 1, 'A'), (2, 1, 'B'),
  (3, 2, 'A'), (4, 2, 'B'), (5, 2, 'C'),
  (6, 3, 'A'),
  (7, 4, 'B'),
  (8, 5, 'A'), (9, 5, 'A'), (10, 5, 'B');
```

## A solution

```sql
SELECT DISTINCT a.user_id
FROM purchases AS a
JOIN purchases AS b
  ON b.user_id = a.user_id AND b.product = 'B'
LEFT JOIN purchases AS c
  ON c.user_id = a.user_id AND c.product = 'C'
WHERE a.product = 'A'
  AND c.purchase_id IS NULL
ORDER BY a.user_id;
```

The result is users 1 and 5. User 2 bought C, so the left join finds a C row and the `IS NULL` test rejects them. User 3 lacks B, and user 4 lacks A. User 5 bought A twice; `DISTINCT` keeps their ID once after the two A rows match B.

This query tests whether a user has *ever* bought C in the available data. It does not ask whether C was bought before or after A and B. A time-based rule needs purchase timestamps. With many repeat purchases, `EXISTS` and `NOT EXISTS` can express these membership tests without making repeated join pairs.

## Check your understanding

1. Why is user 2 excluded?
2. Why is `DISTINCT` useful for user 5?
3. What extra column would be needed for a rule about purchase order?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html#FUNCTIONS-SUBQUERY-EXISTS)
