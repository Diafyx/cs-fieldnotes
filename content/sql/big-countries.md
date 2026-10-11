# Big Countries

This practice question uses `OR` to join two rules. A country counts as big when its area is at least 3,000,000 square kilometres or its population is at least 25,000,000. It only needs to meet one rule.

## The question

The `world` table has `name`, `area_km2`, and `population`. Return those three columns for big countries. Sort by name so the sample output is easy to check.

Try these rows:

```sql
CREATE TEMP TABLE world (
  name text PRIMARY KEY,
  area_km2 integer NOT NULL,
  population integer NOT NULL
);

INSERT INTO world (name, area_km2, population) VALUES
  ('Alder', 3000000, 1200000),
  ('Birch', 900000, 25000000),
  ('Cedar', 2000000, 12000000),
  ('Dune', 4000000, 40000000);
```

The names are made up. Alder meets the area rule exactly. Birch meets the population rule exactly. Cedar meets neither. Dune meets both.

## A solution

```sql
SELECT name, area_km2, population
FROM world
WHERE area_km2 >= 3000000
   OR population >= 25000000
ORDER BY name;
```

The output contains Alder, Birch, and Dune, in that order. `>=` includes the boundary values. `OR` includes a row if either side is true. Dune appears only once because the query reads each source row once. No `DISTINCT` is needed.

Using `AND` would be wrong here: it would keep only Dune. Using `>` would lose Alder and Birch because they sit exactly on a boundary.

If either measure could be `NULL`, a row may still pass when the other measure meets its rule. If the other measure does not pass, the result can be unknown and `WHERE` drops it. The sample table uses `NOT NULL` to keep the exercise clear.

## Check your understanding

1. Would a country with area 2,999,999 and population 25,000,000 appear?
2. Why is `DISTINCT` unnecessary in the solution?
3. How would the result change if `OR` became `AND`?

## Further reading

- [LeetCode Big Countries problem](https://leetcode.com/problems/big-countries/)
- [PostgreSQL logical operators](https://www.postgresql.org/docs/current/functions-logical.html)
