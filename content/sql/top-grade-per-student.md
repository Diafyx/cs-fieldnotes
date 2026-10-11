# Top Grade per Student

Return one best grade for each student. If a student has the same highest grade in several courses, choose the smallest course ID.

## Sample data

```sql
CREATE TEMP TABLE grades (
  student_id integer NOT NULL,
  course_id integer NOT NULL,
  grade integer NOT NULL
);
INSERT INTO grades VALUES
  (1, 10, 90), (1, 20, 90), (1, 30, 70),
  (2, 20, 75), (2, 30, 65);
```

## Solution

```sql
SELECT student_id, course_id, grade
FROM (
  SELECT g.student_id, g.course_id, g.grade,
         ROW_NUMBER() OVER (
           PARTITION BY g.student_id
           ORDER BY g.grade DESC, g.course_id ASC
         ) AS position
  FROM grades AS g
) AS ranked
WHERE position = 1
ORDER BY student_id;
```

The rows are `(1, 10, 90)` and `(2, 20, 75)`. The inner query ranks grades for each student. Course 10 wins the grade tie for student 1. The outer query keeps one row per student. `MAX(grade)` alone finds the score but does not say which tied course to show.

If more than one grade row can exist for the same student and course, add a stable grade record ID to the ordering or decide how to combine attempts. A student without grades is absent because the query starts from `grades`.

## Check your understanding

1. Why is course 20 not shown for student 1?
2. How would you show every course tied at the top grade?
3. What extra rule is needed if a student can have two attempts in one course?

## Further reading

- [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html)
