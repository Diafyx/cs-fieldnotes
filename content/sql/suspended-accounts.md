# Suspended Accounts

A suspension has a start date and may have an end date. Join accounts to suspension records to find which accounts were suspended on a chosen day.

## The question

Return account IDs and names suspended on January 5, 2026. Both the start and end date count as suspended days. A `NULL` end date means the suspension is still open. Sort by account ID.

```sql
CREATE TEMP TABLE accounts (
  account_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE suspensions (
  suspension_id integer PRIMARY KEY,
  account_id integer NOT NULL,
  starts_on date NOT NULL,
  ends_on date
);

INSERT INTO accounts VALUES
  (1, 'Asha'), (2, 'Ben'), (3, 'Cara'), (4, 'Dev');
INSERT INTO suspensions VALUES
  (10, 1, '2026-01-01', '2026-01-10'),
  (11, 2, '2025-12-01', '2025-12-31'),
  (12, 4, '2026-01-05', NULL);
```

## A solution

```sql
SELECT DISTINCT a.account_id, a.name
FROM accounts AS a
JOIN suspensions AS s ON s.account_id = a.account_id
WHERE s.starts_on <= '2026-01-05'
  AND (s.ends_on IS NULL OR s.ends_on >= '2026-01-05')
ORDER BY a.account_id;
```

The result is Asha and Dev. Asha's suspension includes the chosen date. Dev's starts that day and has no end. Ben's ended earlier. Cara has no suspension record. `DISTINCT` keeps an account once if bad or overlapping suspension data gives it two matching records.

This question uses dates, so both ends are inclusive. A timestamp-based suspension needs a clear time zone and boundary rule. For example, an end timestamp might mean the first instant the account is active again, which calls for `<` rather than `<=` on that boundary.

## Check your understanding

1. Why is Dev included?
2. Why is Ben excluded?
3. Why might a timestamp rule use a different comparison at the end boundary?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
