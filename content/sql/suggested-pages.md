# Suggested Pages

One simple page suggestion rule is to show pages liked by a user's friends that the user has not liked. Count how many distinct friends liked each suggested page.

## The question

For user 1, return suggested page IDs and friend counts. Sort by friend count from high to low, then page ID. Friendships are stored as directed rows from the user to each friend.

```sql
CREATE TEMP TABLE friendships (
  user_id integer NOT NULL,
  friend_id integer NOT NULL,
  PRIMARY KEY (user_id, friend_id)
);
CREATE TEMP TABLE page_likes (
  user_id integer NOT NULL,
  page_id integer NOT NULL,
  PRIMARY KEY (user_id, page_id)
);

INSERT INTO friendships VALUES (1, 2), (1, 3);
INSERT INTO page_likes VALUES
  (1, 10),
  (2, 10), (2, 20),
  (3, 20), (3, 30);
```

## A solution

```sql
SELECT liked.page_id,
       COUNT(DISTINCT f.friend_id) AS friend_count
FROM friendships AS f
JOIN page_likes AS liked ON liked.user_id = f.friend_id
LEFT JOIN page_likes AS mine
  ON mine.user_id = f.user_id AND mine.page_id = liked.page_id
WHERE f.user_id = 1
  AND mine.page_id IS NULL
GROUP BY liked.page_id
ORDER BY friend_count DESC, liked.page_id;
```

Page 20 is suggested with count 2 because both friends like it. Page 30 has count 1. Page 10 is excluded because user 1 already likes it. The left join to `mine` checks for an existing like; `mine.page_id IS NULL` keeps only pages without one.

The two primary keys prevent repeated friendship and like rows. `COUNT(DISTINCT f.friend_id)` also states that the score counts people, not raw duplicate records. This rule uses only the listed friendships. If friendship is stored in one row for an undirected pair, the query must first find friends in both directions.

## Check your understanding

1. Why is page 10 absent?
2. Why does page 20 have count 2?
3. What would need to change if friendships were stored without a fixed direction?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
