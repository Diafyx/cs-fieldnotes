# Filter Records Excluding a Specific Pattern

This practice question asks you to remove codes that start with the literal text `TEMP_`. The underscore is part of the code, not a one-character wildcard.

## The question

Return `item_id` and `code` for items whose code does not start with `TEMP_`. A missing code is not a usable code, so leave it out. Sort by `item_id`.

```sql
CREATE TEMP TABLE inventory_items (
  item_id integer PRIMARY KEY,
  code text
);

INSERT INTO inventory_items (item_id, code) VALUES
  (1, 'TEMP_A'),
  (2, 'TEMP_'),
  (3, 'TEMP-7'),
  (4, 'READY_A'),
  (5, NULL),
  (6, 'PRETEMP_A');
```

## A solution

```sql
SELECT item_id, code
FROM inventory_items
WHERE code NOT LIKE 'TEMP!_%' ESCAPE '!'
ORDER BY item_id;
```

The output contains IDs 3, 4, and 6. ID 3 begins with `TEMP-`, which is different from `TEMP_`. ID 6 contains `TEMP_`, but does not start with it. ID 5 is dropped because comparing a `NULL` code with a pattern gives unknown.

In the pattern, `!_` means a literal underscore. The last `%` means any number of following characters, including none. `ESCAPE '!'` chooses the escape character. Without it, `TEMP_%` would also match `TEMP-7` because `_` would stand for any one character.

If missing codes should appear in a review list, use `WHERE code NOT LIKE 'TEMP!_%' ESCAPE '!' OR code IS NULL`. Keep those rows separate in the output if a missing code needs attention.

## Check your understanding

1. Why does `TEMP-7` stay in the result?
2. Would the pattern match the code `TEMP_` with no letters after it?
3. What changes if the pattern starts with `%TEMP` instead?

## Further reading

- [PostgreSQL LIKE and ESCAPE](https://www.postgresql.org/docs/current/functions-matching.html)
