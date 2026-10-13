# Situation-10

## The question

An activity feed shows two rows per page, newest first. Several rows can share a creation time. A new row may arrive while a user moves to the next page. Write the first and second page queries so the second page does not repeat a row from the first.

```sql
CREATE TEMP TABLE feed_events (
  event_id integer PRIMARY KEY,
  created_at timestamp NOT NULL,
  message text NOT NULL
);

INSERT INTO feed_events VALUES
  (1, '2026-01-02 10:00:00', 'one'),
  (2, '2026-01-02 10:00:00', 'two'),
  (3, '2026-01-01 09:00:00', 'three'),
  (4, '2026-01-01 09:00:00', 'four');
```

## Work through it

Sort by time and then by the unique ID. The ID gives rows with equal times a stable order.

```sql
SELECT event_id, created_at
FROM feed_events
ORDER BY created_at DESC, event_id DESC
LIMIT 2;
```

The first page has event 2, then event 1. Save the sort values from the last row, `(2026-01-02 10:00:00, 1)`, as the cursor. Now a new event arrives:

```sql
INSERT INTO feed_events VALUES
  (5, '2026-01-02 10:00:00', 'five');
```

The next page asks for rows after the saved cursor in descending order:

```sql
SELECT event_id, created_at
FROM feed_events
WHERE (created_at, event_id) < ('2026-01-02 10:00:00', 1)
ORDER BY created_at DESC, event_id DESC
LIMIT 2;
```

The second page has event 4, then event 3. Event 1 does not repeat. If the application used `OFFSET 2` after event 5 arrived, it would skip the first two rows of the new order and show event 1 again. An index on `(created_at DESC, event_id DESC)` can help the database find the next rows without scanning all earlier pages.

The cursor must contain every value used to break ties. Use query parameters for cursor values in application code. Both columns are `NOT NULL` here; nullable sort columns need an explicit ordering and cursor rule. This method gives a stable continuation for rows already behind the cursor, but it is not a fixed snapshot of the whole feed. A newly inserted row with an older time can still appear on a later page. If a report needs one frozen view, use a separate snapshot or export design.

## Check your understanding

1. Why is `event_id` part of both the sort and the cursor?
2. Which row would `OFFSET 2` repeat after event 5 is inserted?
3. Can this cursor promise that no new backdated row will appear later?

## Further reading

- [PostgreSQL row comparisons](https://www.postgresql.org/docs/current/functions-comparisons.html#ROW-WISE-COMPARISON)
- [PostgreSQL SELECT and LIMIT](https://www.postgresql.org/docs/current/sql-select.html)
