# Minimum Distance Between Points

To compare every pair of points in one table, join the table to itself. Use an ID order to keep each unordered pair once and to avoid pairing a point with itself.

## The question

Return the IDs of the closest pair and their straight-line distance rounded to three decimal places. If distances tie, choose the pair with the smaller first ID, then smaller second ID.

```sql
CREATE TEMP TABLE points (
  point_id integer PRIMARY KEY,
  x numeric NOT NULL,
  y numeric NOT NULL
);

INSERT INTO points VALUES
  (1, 0, 0),
  (2, 3, 4),
  (3, 1, 1);
```

## A solution

```sql
SELECT a.point_id AS first_id,
       b.point_id AS second_id,
       ROUND(SQRT((a.x - b.x) * (a.x - b.x) +
                  (a.y - b.y) * (a.y - b.y)), 3) AS distance
FROM points AS a
JOIN points AS b ON a.point_id < b.point_id
ORDER BY (a.x - b.x) * (a.x - b.x) +
         (a.y - b.y) * (a.y - b.y),
         a.point_id, b.point_id
LIMIT 1;
```

The answer is points 1 and 3, with distance about 1.414. Their x and y differences are both 1, so the distance is the square root of 2. Sorting by squared distance gives the same nearest pair without rounding before the comparison. The later ID columns settle a tie.

With fewer than two points, the join has no pairs and the query returns no row. Two points at the same coordinates have distance zero if their IDs differ. The number of pairs grows quickly as points are added, so this direct self join fits small data better than a large spatial search.

## Check your understanding

1. Why does `a.point_id < b.point_id` prevent both duplicate pairs and self pairs?
2. Why is the query sorted by squared distance instead of rounded distance?
3. What does the query return if the table has one point?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL mathematical functions](https://www.postgresql.org/docs/current/functions-math.html)
