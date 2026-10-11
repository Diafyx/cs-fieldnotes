# Average Experience by Project

A project can have several employees, and an employee can work on several projects. Join through assignments, then take the average experience of the assigned employees for each project.

## The question

Return every project with average years of experience rounded to two decimal places. Show `NULL` for a project with no assigned employees, since its average is unknown.

```sql
CREATE TEMP TABLE projects (
  project_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  years_experience numeric(5, 2) NOT NULL
);
CREATE TEMP TABLE assignments (
  project_id integer NOT NULL,
  employee_id integer NOT NULL,
  PRIMARY KEY (project_id, employee_id)
);

INSERT INTO projects VALUES
  (10, 'Apollo'), (20, 'Boreal'), (30, 'Cedar');
INSERT INTO employees VALUES (1, 2.00), (2, 4.00), (3, 7.00);
INSERT INTO assignments VALUES (10, 1), (10, 2), (20, 2), (20, 3);
```

## A solution

```sql
SELECT p.project_id, p.name,
       ROUND(AVG(e.years_experience), 2) AS average_years
FROM projects AS p
LEFT JOIN assignments AS a ON a.project_id = p.project_id
LEFT JOIN employees AS e ON e.employee_id = a.employee_id
GROUP BY p.project_id, p.name
ORDER BY p.project_id;
```

Apollo averages 3.00 years from employees 1 and 2. Boreal averages 5.50 years from employees 2 and 3. Cedar has no assignment, so its average is `NULL`. Employee 2 is counted once in each project, which matches the question. The composite key prevents the same employee from being assigned to one project twice.

The sample assumes every assignment points to a real employee. If an assignment points to a missing employee, `AVG` ignores the missing experience; a foreign key can prevent that bad link. Replacing Cedar's `NULL` with zero would claim an average of zero years, which is not what the data says.

## Check your understanding

1. Why does employee 2 contribute to both project averages?
2. Why is Cedar's average missing instead of zero?
3. What table rule prevents a repeated assignment within one project?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
