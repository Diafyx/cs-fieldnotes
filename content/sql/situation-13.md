# Situation-13

## The question

An event source may deliver the same sale more than once. Each event has a source name and an event ID that is unique within that source. Store each sale once and report the total for its event date. A duplicate delivery must not increase the total.

```sql
CREATE TEMP TABLE sale_events (
  source_name text NOT NULL,
  event_id text NOT NULL,
  occurred_on date NOT NULL,
  amount numeric(10, 2) NOT NULL CHECK (amount >= 0),
  PRIMARY KEY (source_name, event_id)
);
```

## Work through it

Let the primary key decide whether a delivery is new. `RETURNING` tells the caller whether a row was inserted.

```sql
INSERT INTO sale_events VALUES ('register-a', 'e-1', '2026-01-05', 40.00)
ON CONFLICT (source_name, event_id) DO NOTHING
RETURNING event_id;
```

This returns `e-1`. The same event arrives again:

```sql
INSERT INTO sale_events VALUES ('register-a', 'e-1', '2026-01-05', 40.00)
ON CONFLICT (source_name, event_id) DO NOTHING
RETURNING event_id;
```

This returns no row. A different event from the same source is stored:

```sql
INSERT INTO sale_events VALUES ('register-a', 'e-2', '2026-01-05', 60.00)
ON CONFLICT (source_name, event_id) DO NOTHING
RETURNING event_id;
```

This returns `e-2`. The report reads the stored events:

```sql
SELECT occurred_on, SUM(amount) AS sale_total
FROM sale_events
GROUP BY occurred_on
ORDER BY occurred_on;
```

The result is January 5 with 100.00. The duplicate did not create a second row. The unique key also protects against two workers inserting the same event at the same time.

`DO NOTHING` is safe only when a repeated key means the same event. If `e-1` arrives again with a different amount or date, compare it with the stored payload and raise an error or follow an explicit correction rule. Silently ignoring a changed payload can hide a data problem. Use the event's date for the report, not its arrival date, so a late delivery is counted in the correct day.

If the event also changes another table, put the event insert and that change in one transaction and apply the change only when the insert is new. An external email or payment call cannot be rolled back with the database; give that work its own idempotency key and retry plan. This design prevents duplicate database effects for this key. It does not promise that a network delivers an event exactly once.

## Check your understanding

1. Which SQL result tells the caller that an event was already stored?
2. Why is `(source_name, event_id)` the key rather than `event_id` alone?
3. What should happen if a duplicate key arrives with a different amount?

## Further reading

- [PostgreSQL INSERT and ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html)
- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
