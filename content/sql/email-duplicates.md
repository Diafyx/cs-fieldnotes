# Email Duplicates

Find email values that appear on more than one contact row. Group rows by email, count the rows in each group, and keep groups whose count is greater than one.

## The question

Return each repeated `email` and its `row_count`. Emails in this exercise are present and already stored in the form the business wants to compare. Sort by email.

```sql
CREATE TEMP TABLE contacts (
  contact_id integer PRIMARY KEY,
  email text NOT NULL
);

INSERT INTO contacts (contact_id, email) VALUES
  (1, 'a@example.com'),
  (2, 'b@example.com'),
  (3, 'a@example.com'),
  (4, 'c@example.com'),
  (5, 'c@example.com'),
  (6, 'c@example.com');
```

## A solution

```sql
SELECT email, COUNT(*) AS row_count
FROM contacts
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY email;
```

The output is `(a@example.com, 2)` and `(c@example.com, 3)`. `b@example.com` has one row and does not pass `HAVING`. `SELECT DISTINCT email` would give one row per email but would not tell you which email was repeated.

Real email data may contain different letter cases or stray spaces. Decide whether those forms should count as the same address before grouping. For example, `LOWER(TRIM(email))` changes the grouping rule and can combine values the plain query keeps apart. It is safer to define and enforce one storage rule than to apply an unexplained change inside a report. Duplicate email values also do not prove that two contact records are the same person.

## Check your understanding

1. Why does `b@example.com` not appear?
2. What does `SELECT DISTINCT email` fail to answer here?
3. What rule would you need before treating `A@example.com` and `a@example.com` as duplicates?

## Further reading

- [LeetCode Duplicate Emails](https://leetcode.com/problems/duplicate-emails/)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
