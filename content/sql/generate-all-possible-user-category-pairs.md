# Generate All Possible User-Category Pairs

To list every combination of users and categories, use a cross join. It pairs each user with every category, even when there is no activity for that pair.

## The question

Return each user ID and category name combination. Sort by user ID and category name.

```sql
CREATE TEMP TABLE users (
  user_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE categories (
  category_id integer PRIMARY KEY,
  category_name text NOT NULL
);

INSERT INTO users VALUES (1, 'Asha'), (2, 'Ben');
INSERT INTO categories VALUES
  (10, 'Books'), (20, 'Music'), (30, 'Games');
```

## A solution

```sql
SELECT u.user_id, c.category_name
FROM users AS u
CROSS JOIN categories AS c
ORDER BY u.user_id, c.category_name;
```

There are six rows: Books, Games, and Music for user 1, then the same three categories for user 2. Two users times three categories gives six pairs. The sorted name order is different from the insertion order; `ORDER BY` sets it.

This grid can be joined to purchases or preferences to show which combinations have no activity. Check size first: one million users and one hundred categories would make one hundred million pairs. If the report needs only active users or a few categories, filter the inputs before the cross join.

## Check your understanding

1. How many pairs would four users and five categories create?
2. Does a user need to have bought from a category to appear here?
3. Why might filtering the inputs before a large cross join help?

## Further reading

- [PostgreSQL cross joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
