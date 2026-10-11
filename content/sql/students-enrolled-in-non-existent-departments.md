# Students Enrolled in Non-Existent Departments

A student row can contain a department ID that is not present in the department table when a foreign key was not enforced. A left join can expose those broken references.

## The question

Return students whose non-null `department_id` has no matching department. Sort by student ID.

```sql
CREATE TEMP TABLE departments (
  department_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE students (
  student_id integer PRIMARY KEY,
  name text NOT NULL,
  department_id integer NOT NULL
);

INSERT INTO departments VALUES (10, 'Computing'), (20, 'Math');
INSERT INTO students VALUES
  (1, 'Ana', 10), (2, 'Ben', 99),
  (3, 'Cara', 20), (4, 'Dev', 98);
```

## A solution

```sql
SELECT s.student_id, s.name, s.department_id
FROM students AS s
LEFT JOIN departments AS d
  ON d.department_id = s.department_id
WHERE d.department_id IS NULL
ORDER BY s.student_id;
```

The result is Ben with department 99 and Dev with department 98. Their student rows survive the left join, but no department matches. Ana and Cara match real departments and are filtered out.

`students.department_id` is required here, so a missing right key means a broken reference. If the student department could be `NULL`, this query would also show students who had no department assigned. You would need an extra condition such as `s.department_id IS NOT NULL` to separate those cases.

A foreign key from `students.department_id` to `departments.department_id` would prevent these broken references in new data. Finding bad rows helps with cleanup; adding the constraint helps keep them from returning.

## Check your understanding

1. Why are Ben and Dev in the result?
2. What extra condition is needed if a student may have a `NULL` department ID?
3. Which table rule could stop new invalid department IDs?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
