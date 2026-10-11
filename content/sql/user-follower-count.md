# User Follower Count

Each follow row connects one user to one follower. Group by the user being followed, then count that user's follow rows.

## The question

Return `user_id` and `followers_count` for users present in `follows`. Sort by user ID. A pair cannot appear twice because it is the primary key.

```sql
CREATE TEMP TABLE follows (
  user_id integer NOT NULL,
  follower_id integer NOT NULL,
  PRIMARY KEY (user_id, follower_id)
);

INSERT INTO follows (user_id, follower_id) VALUES
  (10, 1),
  (10, 2),
  (11, 1),
  (13, 2),
  (13, 3),
  (13, 4);
```

## A solution

```sql
SELECT user_id, COUNT(*) AS followers_count
FROM follows
GROUP BY user_id
ORDER BY user_id;
```

The output is `(10, 2)`, `(11, 1)`, and `(13, 3)`. User 12 is absent because no follow row for that user exists in the sample. To include every account with a zero count, start from a separate `users` table and left join its follow rows.

Count by `user_id`, not `follower_id`. Grouping by `follower_id` would tell you how many people each follower follows, which is a different question. If your source permits duplicate follow rows, fix that rule or use `COUNT(DISTINCT follower_id)` for a report of unique followers.

## Check your understanding

1. What would grouping by `follower_id` measure?
2. Why does user 12 not appear?
3. What protects this table from counting the same follow pair twice?

## Further reading

- [LeetCode Find Followers Count](https://leetcode.com/problems/find-followers-count/)
- [PostgreSQL GROUP BY clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-GROUPBY)
