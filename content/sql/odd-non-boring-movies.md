# Odd Non-Boring Movies

This practice question combines a number test, a text test, and a sort. Return movies whose ID is odd and whose description is not exactly `boring`. Show the highest rated movies first.

## The question

The `cinema` table stores an ID, movie name, description, and rating. Use this sample:

```sql
CREATE TEMP TABLE cinema (
  id integer PRIMARY KEY,
  movie text NOT NULL,
  description text,
  rating numeric(3, 1) NOT NULL
);

INSERT INTO cinema (id, movie, description, rating) VALUES
  (1, 'North Road', 'adventure', 8.5),
  (2, 'Blue Room', 'comedy', 9.7),
  (3, 'Quiet Hour', 'boring', 9.0),
  (5, 'Last Train', 'drama', 8.5),
  (7, 'Hidden Lake', NULL, 6.1);
```

## A solution

```sql
SELECT id, movie, description, rating
FROM cinema
WHERE id % 2 = 1
  AND description <> 'boring'
ORDER BY rating DESC, id;
```

The output is North Road, then Last Train. Their ratings tie, so `id` gives a fixed order. Blue Room has an even ID. Quiet Hour has the excluded description. Hidden Lake has no description; `NULL <> 'boring'` is unknown, so `WHERE` drops it.

The check is for the exact text `boring` under the database's active collation. If the rule should ignore letter case, PostgreSQL can use a case-insensitive comparison, but first decide whether `Boring` should count as the same description. Do not change the rule silently.

For positive IDs, `id % 2 = 1` means odd. If negative IDs were allowed, test the remainder behavior before using that expression. Movie IDs are normally positive.

## Check your understanding

1. Why does movie 3 fail even though its ID is odd?
2. Would movie 7 appear if its description were `interesting`?
3. Why add `id` after `rating DESC`?

## Further reading

- [LeetCode Not Boring Movies problem](https://leetcode.com/problems/not-boring-movies/)
- [PostgreSQL mathematical operators](https://www.postgresql.org/docs/current/functions-math.html)
- [PostgreSQL sorting rows](https://www.postgresql.org/docs/current/queries-order.html)
