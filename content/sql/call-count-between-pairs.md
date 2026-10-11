# Call Count Between Pairs

A call between person 1 and person 2 is the same pair whichever person started it. To count calls by pair, put the smaller ID first and the larger ID second before grouping.

## The question

Each row in `calls` is one completed call. Return the two person IDs in ascending order, the number of calls, and total minutes for that pair. Both IDs are present and a person does not call themselves.

```sql
CREATE TEMP TABLE calls (
  call_id integer PRIMARY KEY,
  caller_id integer NOT NULL,
  receiver_id integer NOT NULL,
  minutes integer NOT NULL,
  CHECK (caller_id <> receiver_id)
);

INSERT INTO calls (call_id, caller_id, receiver_id, minutes) VALUES
  (1, 1, 2, 5),
  (2, 2, 1, 7),
  (3, 1, 3, 10),
  (4, 3, 1, 2),
  (5, 2, 3, 4);
```

## A solution

```sql
SELECT LEAST(caller_id, receiver_id) AS person1,
       GREATEST(caller_id, receiver_id) AS person2,
       COUNT(*) AS call_count,
       SUM(minutes) AS total_minutes
FROM calls
GROUP BY LEAST(caller_id, receiver_id),
         GREATEST(caller_id, receiver_id)
ORDER BY person1, person2;
```

The output is `(1, 2, 2, 12)`, `(1, 3, 2, 12)`, and `(2, 3, 1, 4)`. Reversing caller and receiver does not create a new group. `COUNT(*)` counts call records, while `SUM(minutes)` adds their lengths.

If the business needs separate counts by who called whom, group by `caller_id, receiver_id` instead. If calls can have missing IDs, decide whether to reject those records or report them separately before using `LEAST` and `GREATEST`.

## Check your understanding

1. Why do calls `(1, 2)` and `(2, 1)` become one group?
2. What would grouping by caller and receiver without normalization return?
3. Why is `call_id` useful even though it is not selected?

## Further reading

- [PostgreSQL GREATEST and LEAST](https://www.postgresql.org/docs/current/functions-conditional.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
