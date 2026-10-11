# Swap Consecutive Seats

Seats are numbered from 1 without gaps. Swap the people in seats 1 and 2, then 3 and 4, and so on. If the last seat has no partner, leave it alone. Return the new seat number and the person's name.

## Sample data

```sql
CREATE TEMP TABLE seats (seat_id integer PRIMARY KEY, name text NOT NULL);
INSERT INTO seats VALUES
  (1, 'Ana'), (2, 'Ben'), (3, 'Cara'), (4, 'Dev'), (5, 'Ema');
```

## Solution

```sql
SELECT CASE
         WHEN s.seat_id % 2 = 1 AND EXISTS (
           SELECT 1 FROM seats AS next_seat WHERE next_seat.seat_id = s.seat_id + 1
         ) THEN s.seat_id + 1
         WHEN s.seat_id % 2 = 0 THEN s.seat_id - 1
         ELSE s.seat_id
       END AS new_seat_id,
       s.name
FROM seats AS s
ORDER BY new_seat_id;
```

The rows are `(1, 'Ben')`, `(2, 'Ana')`, `(3, 'Dev')`, `(4, 'Cara')`, and `(5, 'Ema')`. An odd seat moves right only when the next seat exists. An even seat moves left. The last unpaired person stays put.

This query changes the displayed seat IDs; it does not update the table. The even-seat rule assumes IDs begin at 1 and have no gaps. If seats can be missing, first define whether to swap adjacent *numbers* or adjacent *occupied positions*; those are different tasks.

## Check your understanding

1. Why does Ema stay in seat 5?
2. Does this query modify `seats`?
3. Why would a gap in seat numbers need a new rule?

## Further reading

- [PostgreSQL conditional expressions](https://www.postgresql.org/docs/current/functions-conditional.html)
- [PostgreSQL EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html#FUNCTIONS-SUBQUERY-EXISTS)
