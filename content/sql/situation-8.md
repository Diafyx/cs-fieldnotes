# Situation-8

## The question

An audit table gives each account's events a sequence number. Find gaps between stored numbers for each account. Return the account ID, the first missing number, and the last missing number in each gap. Sort by account and first missing number.

```sql
CREATE TEMP TABLE audit_events (
  account_id integer NOT NULL,
  sequence_no integer NOT NULL,
  PRIMARY KEY (account_id, sequence_no)
);

INSERT INTO audit_events VALUES
  (1, 1), (1, 2), (1, 4), (1, 7),
  (2, 10), (2, 12);
```

Account 1 is missing 3, then 5 and 6. Account 2 is missing 11 between its stored rows.

## Work through it

For each account, compare a number with the previous stored number. `LAG` reads that previous row inside the account's ordered group.

```sql
WITH numbered AS (
  SELECT account_id, sequence_no,
         LAG(sequence_no) OVER (
           PARTITION BY account_id ORDER BY sequence_no
         ) AS previous_no
  FROM audit_events
)
SELECT account_id,
       previous_no + 1 AS missing_from,
       sequence_no - 1 AS missing_through
FROM numbered
WHERE sequence_no > previous_no + 1
ORDER BY account_id, missing_from;
```

The rows are `(1, 3, 3)`, `(1, 5, 6)`, and `(2, 11, 11)`. The first stored number for an account has no previous row, so `previous_no` is `NULL` and it does not pass the `WHERE` test.

This finds gaps only between observed rows. It cannot tell whether account 2 should have started at 1 rather than 10. That needs a separate starting rule. A gap may mean a missing event, a delayed import, or a number intentionally skipped by a sequence. The query finds the gap; it does not explain its cause. The primary key prevents duplicate sequence numbers within one account.

## Check your understanding

1. Why is the gap from 5 through 6 returned as one row?
2. Why does the query not report 1 through 9 for account 2?
3. What additional data would help decide whether a gap is an error?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL sequence behavior](https://www.postgresql.org/docs/current/functions-sequence.html)
