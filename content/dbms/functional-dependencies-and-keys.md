# Functional Dependencies and Keys

A functional dependency, or FD, is a rule about possible rows. `X -> Y` means that any two rows with the same values for attributes `X` must also have the same values for attributes `Y`. It does not say that a value in `X` causes a value in `Y`. It says `X` is enough to determine `Y` in every valid state of the relation.

Consider `Enrollment(student_id, course_id, student_name, course_title, grade)`. Assume these business rules:

```text
student_id -> student_name
course_id -> course_title
(student_id, course_id) -> grade
```

Two rows for student `1` must use the same student name. Two rows for course `10` must use the same course title. A student has at most one grade per course. The last rule says nothing about whether two students can get the same grade.

## Find the keys

A set of attributes is a **superkey** if it determines every attribute in the relation. A **candidate key** is a superkey with no unnecessary attribute. In this example, `(student_id, course_id)` determines the student name, course title, and grade. Neither ID alone determines all five attributes, so the pair is a candidate key. `(student_id, course_id, grade)` is a superkey, but not a candidate key because `grade` is extra.

To find keys, compute an attribute closure. Start with the chosen attributes and repeatedly add attributes determined by known FDs. If the closure includes every attribute, the chosen set is a superkey. To prove it is a candidate key, remove each attribute in turn and show that the smaller set is not a superkey. A schema may have more than one candidate key.

An FD is **trivial** if its right side is already part of its left side, such as `(student_id, course_id) -> student_id`. A nontrivial FD can reveal repeated facts or a useful key. FDs describe rules that must hold for every valid row set. Seeing an FD in today's data does not prove it will always hold. For instance, unique names in a sample do not make `student_name` a key.

## Put the rules into tables

```sql
CREATE TEMP TABLE students (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL
);

CREATE TEMP TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_title TEXT NOT NULL
);

CREATE TEMP TABLE enrollments (
    student_id INTEGER NOT NULL REFERENCES students(student_id),
    course_id INTEGER NOT NULL REFERENCES courses(course_id),
    grade TEXT NOT NULL,
    PRIMARY KEY (student_id, course_id)
);

INSERT INTO students VALUES (1, 'Mina'), (2, 'Dev');
INSERT INTO courses VALUES (10, 'Databases'), (20, 'Networks');
INSERT INTO enrollments VALUES
    (1, 10, 'A'),
    (1, 20, 'B'),
    (2, 10, 'A');

SELECT s.student_name, c.course_title, e.grade
FROM enrollments AS e
JOIN students AS s ON s.student_id = e.student_id
JOIN courses AS c ON c.course_id = e.course_id
ORDER BY e.student_id, e.course_id;
```

The result is `(Mina, Databases, A)`, `(Mina, Networks, B)`, and `(Dev, Databases, A)`. The three primary keys enforce the chosen identifiers. The foreign keys stop an enrollment from naming a missing student or course.

SQL constraints do not express every FD directly. A `UNIQUE` constraint can enforce a determinant when the relevant columns cannot be `NULL`, but it does not make arbitrary cross-table rules automatic. Also, ordinary SQL `NULL` complicates the classical definition of equality used in FD theory. Start the reasoning with clear, non-null identifiers and handle optional facts explicitly.

## Try it yourself

1. Why is `course_id` alone not a key for the original `Enrollment` relation?
2. Could two students have the same name without breaking the stated FDs?
3. If a student can retake a course, what should change in the enrollment key and grade rule?

## References

- [CMU lecture notes on functional dependencies](https://15445.courses.cs.cmu.edu/fall2017/notes/04-notes-functionaldependencies.pdf)
- [PostgreSQL unique and primary key constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
