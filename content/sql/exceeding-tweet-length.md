# Exceeding Tweet Length

This exercise marks a post invalid when its content has more than 15 characters. A post with exactly 15 characters is valid. Use a character count, not a byte count.

## The question

Return the IDs of posts whose content exceeds 15 characters, sorted by ID. Every row has content.

```sql
CREATE TEMP TABLE posts (
  post_id integer PRIMARY KEY,
  content text NOT NULL
);

INSERT INTO posts (post_id, content) VALUES
  (1, '123456789012345'),
  (2, '1234567890123456'),
  (3, 'café');
```

## A solution

```sql
SELECT post_id
FROM posts
WHERE CHAR_LENGTH(content) > 15
ORDER BY post_id;
```

The only result is post 2. Post 1 sits exactly on the limit and stays valid. Post 3 has four characters in a UTF-8 PostgreSQL database, although its text takes more than four bytes. `OCTET_LENGTH` would answer a different question.

The rule here counts database characters. A real social platform may count some visible symbols, combined marks, or links in its own way. If this query enforces a product limit, match the product's exact counting rule. A missing content value is excluded by the table's `NOT NULL` rule.

## Check your understanding

1. Why is post 1 valid?
2. Which function would count bytes instead of characters in PostgreSQL?
3. Why might a product's visible-character rule differ from `CHAR_LENGTH`?

## Further reading

- [LeetCode Invalid Tweets](https://leetcode.com/problems/invalid-tweets/)
- [PostgreSQL string functions](https://www.postgresql.org/docs/current/functions-string.html)
