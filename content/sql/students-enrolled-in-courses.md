# Students Enrolled in Courses

Students and courses have a many-to-many relationship: one student can take several courses, and one course can have several students. An enrollment table stores each link between them.

## The question

Return each enrolled student's name and course title. Sort by student ID and course ID. Students with no enrollment are not part of this report.

```sql
CREATE TEMP TABLE students (
  student_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE courses (
  course_id integer PRIMARY KEY,
  title text NOT NULL
);
CREATE TEMP TABLE enrollments (
  student_id integer NOT NULL,
  course_id integer NOT NULL,
  PRIMARY KEY (student_id, course_id)
);

INSERT INTO students VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara');
INSERT INTO courses VALUES (10, 'SQL'), (20, 'Networks');
INSERT INTO enrollments VALUES (1, 10), (1, 20), (2, 10);
```

## A solution

```sql
SELECT s.student_id, s.name, c.course_id, c.title
FROM enrollments AS e
JOIN students AS s ON s.student_id = e.student_id
JOIN courses AS c ON c.course_id = e.course_id
ORDER BY s.student_id, c.course_id;
```

The rows are Ana in SQL, Ana in Networks, and Ben in SQL. Cara is absent because she has no enrollment. Ana appears twice because she has two real student-course links. The composite primary key prevents the same student-course pair from being entered twice.

Adding foreign keys on the two enrollment columns would reject links to missing students or courses. To report students with no courses too, start from `students` and left join through `enrollments` to `courses`. Be careful: a `WHERE` filter on course title could then remove students with no match.

## Check your understanding

1. Why does Ana appear twice?
2. What rule stops Ana from being enrolled in SQL twice?
3. What join direction would keep Cara in a report of all students?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL multicolumn keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS)
