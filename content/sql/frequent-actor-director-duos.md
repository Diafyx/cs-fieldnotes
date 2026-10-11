# Frequent Actor-Director Duos

An actor and a director can work together more than once. Group by both IDs to count each pair's collaborations. Then keep pairs whose count reaches the threshold.

## The question

Each row in `collaborations` is one recorded collaboration event. Return actor and director pairs with at least three events. Sort by actor ID, then director ID.

```sql
CREATE TEMP TABLE collaborations (
  event_id integer PRIMARY KEY,
  actor_id integer NOT NULL,
  director_id integer NOT NULL
);

INSERT INTO collaborations (event_id, actor_id, director_id) VALUES
  (1, 10, 20),
  (2, 10, 20),
  (3, 10, 20),
  (4, 10, 30),
  (5, 10, 30),
  (6, 11, 20),
  (7, 11, 20),
  (8, 11, 20);
```

## A solution

```sql
SELECT actor_id, director_id
FROM collaborations
GROUP BY actor_id, director_id
HAVING COUNT(*) >= 3
ORDER BY actor_id, director_id;
```

The output is `(10, 20)` and `(11, 20)`. The pair `(10, 30)` has only two events. Grouping only by actor would mix an actor's work with different directors. Grouping only by director would mix different actors.

The query assumes one event row means one collaboration. If the source can record the same film more than once for a pair, decide whether the question means events or distinct films. For distinct films, store a film ID and count distinct film IDs. `DISTINCT` on the final output cannot fix a count that was inflated before `HAVING`.

## Check your understanding

1. Why are two columns needed in `GROUP BY`?
2. Does pair `(10, 30)` meet the threshold?
3. What source key would you need to count distinct films instead of events?

## Further reading

- [LeetCode Actors and Directors Who Cooperated At Least Three Times](https://leetcode.com/problems/actors-and-directors-who-cooperated-at-least-three-times/)
- [PostgreSQL HAVING clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-HAVING)
