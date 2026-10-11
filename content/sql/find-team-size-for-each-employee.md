# Find Team Size for Each Employee

First count members in each team. Then join those team counts back to employees so every employee gets their team's size.

## The question

Return each employee ID, team ID, and team size. Every employee belongs to one team. Sort by employee ID.

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  team_id integer NOT NULL
);

INSERT INTO employees VALUES
  (1, 10), (2, 10),
  (3, 20), (4, 20), (5, 20);
```

## A solution

```sql
SELECT e.employee_id, e.team_id, t.team_size
FROM employees AS e
JOIN (
  SELECT team_id, COUNT(*) AS team_size
  FROM employees
  GROUP BY team_id
) AS t ON t.team_id = e.team_id
ORDER BY e.employee_id;
```

Employees 1 and 2 get size 2. Employees 3, 4, and 5 get size 3. The grouped query has one row per team, so joining it back does not multiply employee rows. This makes the level of each step clear: count at the team level, then report at the employee level.

An empty team with no employees is not in this report, because the report starts from employees. If team IDs could be `NULL`, a group for missing IDs would not match back with ordinary `=`, so this sample requires a team ID for every employee. If a person can belong to several teams, use a membership table and decide whether team size counts distinct people.

## Check your understanding

1. Why does employee 4 get size 3?
2. Why does the grouped query return only one row per team?
3. What extra table would you need if employees could belong to several teams?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL grouping](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP)
