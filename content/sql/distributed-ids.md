# Distributed IDs

An ID must keep two different records from being mistaken for the same record. With one PostgreSQL writer, an identity column or sequence is often enough. With several independent writers or shards, each writer must avoid generating the same ID as another one. The ID format is a design choice; the primary key constraint still checks for duplicates in each database.

## Choices

| Method | How it stays unique | Main limit |
| --- | --- | --- |
| One database sequence | One database assigns values | Independent databases can assign the same number |
| UUID version 4 | Random value from a large space | Values are not ordered by creation time |
| UUID version 7 | Time field plus random bits | Clock order is approximate, not a transaction order |
| Shard ID plus local number | Each shard owns a distinct namespace | The shard ID must remain stable and the format needs planning |

PostgreSQL 18 can generate version 4 UUIDs with `gen_random_uuid()` and version 7 UUIDs with `uuidv7()`. Check your server version before using `uuidv7()`. This example uses a version 7 value:

```sql
CREATE TEMP TABLE events (
  event_id uuid PRIMARY KEY DEFAULT uuidv7(),
  message text NOT NULL
);

INSERT INTO events (message) VALUES ('opened')
RETURNING event_id, message;
```

The result has one row with `opened` and a generated UUID. Its exact ID changes on each run. PostgreSQL rejects a second row with the same primary key. If writers use separate databases, each database can enforce uniqueness locally, but the application still needs an ID scheme that works across all of them.

## Numbers are not a clock

PostgreSQL sequence values are consumed even when a transaction rolls back. Gaps are normal. A higher sequence number does not prove that its transaction committed later. UUID version 7 carries time information and often improves index locality compared with random version 4 values, but clock drift and concurrent generation mean it cannot prove a strict event order either. Use a recorded timestamp and a clear tie breaker for ordered queries. Use an explicit business number system if the business truly needs gapless numbers; do not assume a primary key can provide them.

IDs exposed in URLs should not be treated as secret access tokens. Authorization must check whether the caller may read the row. If the key must remain unique after data from shards is merged, include the shard namespace or use an ID that is generated across the whole system.

## Check your understanding

1. Why can two PostgreSQL sequences on separate shards both produce `42`?
2. Why is a gap in a sequence not proof that a row was deleted?
3. Can sorting by UUID version 7 replace a rule for ordering simultaneous events?

## Further reading

- [PostgreSQL UUID type](https://www.postgresql.org/docs/current/datatype-uuid.html)
- [PostgreSQL UUID functions](https://www.postgresql.org/docs/current/functions-uuid.html)
- [PostgreSQL CREATE SEQUENCE](https://www.postgresql.org/docs/current/sql-createsequence.html)
