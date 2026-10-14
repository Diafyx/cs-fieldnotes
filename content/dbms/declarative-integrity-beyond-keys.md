# Declarative Integrity Beyond Keys

A key says which row is which. Many data rules need more than a key. A meeting must end after it starts. Two bookings for one room must not overlap. A child row may need to disappear when its parent is deleted. A **declarative constraint** states such a rule in the schema so every writer must follow it.

## Choose the rule that matches the fact

| Rule | Use it for | Important detail |
| --- | --- | --- |
| `NOT NULL` | A value must be present. | A `DEFAULT` does not reject an explicit `NULL`. |
| `CHECK` | A condition on the row being inserted or changed. | A check passes when its result is true or unknown. |
| `UNIQUE` | A value or group of values must not repeat. | PostgreSQL normally permits several `NULL` values. |
| Foreign key action | Decide what happens to child rows when a parent changes. | `CASCADE`, `SET NULL`, `SET DEFAULT`, and restrict or no action have different effects. |
| `EXCLUDE` | Certain pairs of rows must not coexist. | Useful for ranges that must not overlap. |

PostgreSQL 15 and later allow `UNIQUE NULLS NOT DISTINCT` when only one `NULL` should be allowed. A unique constraint across two columns checks the **pair**, not each column separately. A unique **partial index** can enforce a rule only for rows matching a condition, such as one active subscription per customer. It is an index with a uniqueness rule, not a table `UNIQUE` constraint.

## A booking example

Assume the table holds bookings for one room and the times are integer hour numbers. PostgreSQL's `int4range` value `[9, 10)` includes 9 but excludes 10. This lets one meeting end at 10 and another begin at 10.

```sql
CREATE TEMP TABLE meeting_slots (
    booking_id INTEGER PRIMARY KEY,
    starts_at INTEGER NOT NULL,
    ends_at INTEGER NOT NULL,
    CONSTRAINT valid_span CHECK (ends_at > starts_at),
    CONSTRAINT no_overlap EXCLUDE USING gist (
        int4range(starts_at, ends_at, '[)') WITH &&
    )
);

INSERT INTO meeting_slots VALUES (1, 9, 10), (2, 10, 11);

SELECT booking_id, starts_at, ends_at
FROM meeting_slots
ORDER BY booking_id;
```

The query returns `(1, 9, 10)` and `(2, 10, 11)`. The ranges touch but do not overlap. An insert of `(3, 9, 11)` would fail `no_overlap`. An insert of `(3, 11, 11)` would fail `valid_span`. The `NOT NULL` columns matter because a `CHECK` expression that becomes unknown due to `NULL` does not reject the row by itself. The exclusion constraint uses a GiST index created for it.

For several rooms, the exclusion rule must also compare room IDs. PostgreSQL often needs the `btree_gist` extension to use equality on ordinary types inside a GiST exclusion constraint. A rule for one room cannot silently be reused for many rooms.

## Timing and limits

Most constraints are checked after each statement. Some PostgreSQL `UNIQUE`, primary key, foreign key, and exclusion constraints can be declared `DEFERRABLE` and checked at transaction end. This helps with changes that are briefly invalid during a multi-statement transaction but valid before commit. `NOT NULL` and `CHECK` cannot be deferred in PostgreSQL. A deferred rule can still make `COMMIT` fail, so the application must handle that error.

A `CHECK` should use only values from the row it checks. It cannot safely enforce a sum across all rows or look up a changing value in another table. For cross-row rules, first look for a `UNIQUE` or exclusion constraint. For cross-table references, use a foreign key. If the rule needs a transaction-wide calculation, use an appropriate transaction design and isolation level. A trigger that merely queries a total can still race with another transaction unless concurrency is handled.

A domain can package a reusable value rule, such as a positive amount, but domain checks have their own `NULL` behavior. Generated columns and defaults can calculate or supply data; they do not replace a constraint that rejects invalid data. Name important constraints so an error tells you which rule failed. Before adding a rule to an existing table, check and repair old rows, then plan validation and locking for the live table.

## Try it yourself

1. Why do the two bookings in the example coexist, while a booking from 9 to 11 does not?
2. How would the rule change if bookings for different rooms may overlap?
3. Why does `CHECK (price > 0)` still need `NOT NULL` when every row must have a price?
4. What happens if a deferred foreign key is still broken at commit time?

## References

- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL CREATE TABLE and deferrable constraints](https://www.postgresql.org/docs/current/sql-createtable.html)
- [PostgreSQL partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html)
- [PostgreSQL range types](https://www.postgresql.org/docs/current/rangetypes.html)
