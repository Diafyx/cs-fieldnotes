# Most Experienced Employees in Each Project

For each project with assigned employees, return everyone tied for the most years of experience. The experience value belongs to the employee, and the project assignment decides which employees are compared.

## Sample data

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  experience_years integer NOT NULL
);
CREATE TEMP TABLE assignments (
  project_id integer NOT NULL,
  employee_id integer NOT NULL,
  PRIMARY KEY (project_id, employee_id)
);
INSERT INTO employees VALUES (1, 5), (2, 5), (3, 2), (4, 8);
INSERT INTO assignments VALUES
  (10, 1), (10, 2), (10, 3),
  (20, 3), (20, 4);
```

## Solution

```sql
SELECT project_id, employee_id, experience_years
FROM (
  SELECT a.project_id, e.employee_id, e.experience_years,
         RANK() OVER (
           PARTITION BY a.project_id ORDER BY e.experience_years DESC
         ) AS place
  FROM assignments AS a
  JOIN employees AS e ON e.employee_id = a.employee_id
) AS ranked
WHERE place = 1
ORDER BY project_id, employee_id;
```

The result is `(10, 1, 5)`, `(10, 2, 5)`, and `(20, 4, 8)`. Employees 1 and 2 tie for project 10. Employee 4 leads project 20. `RANK` keeps both tied winners. `ROW_NUMBER` would choose one winner and need an extra tie rule.

The assignment primary key stops one employee from appearing twice in one project. If an employee has no experience value, decide whether that means zero years or unknown before ranking. A project with no assignments cannot appear in this query because it starts from `assignments`.

## Check your understanding

1. Why are two employees returned for project 10?
2. What would a duplicate assignment do without the primary key?
3. Why is a project with no assigned employee absent?

## Further reading

- [PostgreSQL ranking functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
