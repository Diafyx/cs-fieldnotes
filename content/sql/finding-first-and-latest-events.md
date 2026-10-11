# Finding First and Latest Events

For each user, first and latest usually mean the earliest and latest event times. If two events share a time, choose a rule for which event row wins. A timestamp alone does not identify one row in a tie.

## Sample data

```sql
CREATE TEMP TABLE events (
  event_id integer PRIMARY KEY,
  user_id integer NOT NULL,
  happened_at timestamp NOT NULL
);
INSERT INTO events VALUES
  (10, 1, '2026-01-01 09:00:00'),
  (11, 1, '2026-01-02 10:00:00'),
  (12, 1, '2026-01-02 10:00:00'),
  (20, 2, '2026-01-03 08:00:00');
```

## Solution

```sql
WITH ranked AS (
  SELECT e.user_id, e.event_id,
         ROW_NUMBER() OVER (
           PARTITION BY e.user_id ORDER BY e.happened_at, e.event_id
         ) AS first_position,
         ROW_NUMBER() OVER (
           PARTITION BY e.user_id ORDER BY e.happened_at DESC, e.event_id DESC
         ) AS last_position
  FROM events AS e
)
SELECT user_id,
       MAX(CASE WHEN first_position = 1 THEN event_id END) AS first_event_id,
       MAX(CASE WHEN last_position = 1 THEN event_id END) AS latest_event_id
FROM ranked
GROUP BY user_id
ORDER BY user_id;
```

The rows are `(1, 10, 12)` and `(2, 20, 20)`. Event 12 is chosen over event 11 because the example uses the larger ID to break a latest-time tie. A user with one event has the same first and latest event. A user with no event is absent because the query starts from `events`.

If the task needs only the first and latest *times*, `MIN(happened_at)` and `MAX(happened_at)` are simpler. If it needs every tied event, use `RANK()` and keep rank 1 instead of choosing one ID. An event ID is only a tie breaker here; do not assume a larger ID always means a later real-world event.

## Check your understanding

1. Why does user 1's latest event have ID 12?
2. What would `MAX(happened_at)` fail to tell you?
3. How could you include users who have never had an event?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
