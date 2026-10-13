# Situation-15

## The question

Group each user's events into sessions. A new session starts when the gap since that user's previous event is more than 30 minutes. A gap of exactly 30 minutes stays in the same session. Return each user's session number, first event time, last event time, and event count.

For a small example, `minute_mark` counts minutes from the same fixed start time. In a real system, use full timestamps so sessions can cross midnight.

```sql
CREATE TEMP TABLE activity (
  event_id integer PRIMARY KEY,
  user_id integer NOT NULL,
  minute_mark integer NOT NULL
);

INSERT INTO activity VALUES
  (1, 1, 0), (2, 1, 20), (3, 1, 50), (4, 1, 81),
  (5, 2, 0), (6, 2, 31);
```

User 1's first three events belong together: the gaps are 20 and 30 minutes. The event at minute 81 starts a new session. User 2's second event starts a new session because its gap is 31 minutes.

## Work through it

First get the previous time for each user. Then mark the start of each session. A running sum of those markers gives a session number for each event. Finally, group by user and session number.

```sql
WITH previous AS (
  SELECT user_id, event_id, minute_mark,
         LAG(minute_mark) OVER (
           PARTITION BY user_id ORDER BY minute_mark, event_id
         ) AS previous_minute
  FROM activity
), starts AS (
  SELECT user_id, event_id, minute_mark,
         CASE WHEN previous_minute IS NULL
                   OR minute_mark - previous_minute > 30
              THEN 1 ELSE 0 END AS new_session
  FROM previous
), numbered AS (
  SELECT user_id, event_id, minute_mark,
         SUM(new_session) OVER (
           PARTITION BY user_id
           ORDER BY minute_mark, event_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
         ) AS session_no
  FROM starts
)
SELECT user_id, session_no,
       MIN(minute_mark) AS first_minute,
       MAX(minute_mark) AS last_minute,
       COUNT(*) AS event_count
FROM numbered
GROUP BY user_id, session_no
ORDER BY user_id, session_no;
```

The result is `(1, 1, 0, 50, 3)`, `(1, 2, 81, 81, 1)`, `(2, 1, 0, 0, 1)`, and `(2, 2, 31, 31, 1)`. The first event for each user starts session 1 because it has no previous event. Sorting by `event_id` after the time gives a stable order when events share a time.

The rule compares each event with the previous event, not with the first event in its session. That means a session can last much longer than 30 minutes if each neighboring gap is at most 30 minutes. Late events can change earlier session boundaries and session numbers, so do not use this calculated number as a permanent ID without a plan for corrections. In production, decide which timestamp represents the event, how to handle missing or impossible times, and whether the business wants a maximum session length as a separate rule.

## Check your understanding

1. Why does user 1's event at minute 50 stay in session 1?
2. What would happen if the rule changed from "more than 30" to "at least 30" minutes?
3. Why can a late event change the session numbers of later events?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
