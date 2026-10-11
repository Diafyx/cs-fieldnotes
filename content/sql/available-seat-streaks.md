# Available Seat Streaks

A group needs at least three free seats next to each other in the same hall. A self join can check the next two seat numbers. A check on the previous seat makes each longer free run appear once.

## The question

Return the hall ID and first seat number for each run of at least three consecutive free seats. Sort by hall and first seat.

```sql
CREATE TEMP TABLE seats (
  hall_id integer NOT NULL,
  seat_no integer NOT NULL,
  is_free boolean NOT NULL,
  PRIMARY KEY (hall_id, seat_no)
);

INSERT INTO seats VALUES
  (1, 1, true), (1, 2, true), (1, 3, true),
  (1, 4, true), (1, 5, false), (1, 6, true),
  (2, 1, true), (2, 2, false),
  (2, 3, true), (2, 4, true), (2, 5, true);
```

## A solution

```sql
SELECT s1.hall_id, s1.seat_no AS first_seat
FROM seats AS s1
JOIN seats AS s2
  ON s2.hall_id = s1.hall_id
 AND s2.seat_no = s1.seat_no + 1
 AND s2.is_free = true
JOIN seats AS s3
  ON s3.hall_id = s1.hall_id
 AND s3.seat_no = s1.seat_no + 2
 AND s3.is_free = true
WHERE s1.is_free = true
  AND NOT EXISTS (
    SELECT 1 FROM seats AS previous
    WHERE previous.hall_id = s1.hall_id
      AND previous.seat_no = s1.seat_no - 1
      AND previous.is_free = true
  )
ORDER BY s1.hall_id, first_seat;
```

The answer is `(1, 1)` and `(2, 3)`. Hall 1 has four free seats from 1 to 4, but only seat 1 starts that run. Hall 2's run starts at seat 3. A missing seat number breaks a streak, since the next numbered seat must exist and be free.

This query gives run starts, not the run's final seat or length. A report that needs full lengths can group consecutive free seats using window functions. The primary key keeps one row per hall and seat number.

## Check your understanding

1. Why is hall 1 seat 2 not returned as another start?
2. What happens if seat 3 is missing between free seats 2 and 4?
3. Which condition stops a streak from crossing into another hall?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html#FUNCTIONS-SUBQUERY-EXISTS)
