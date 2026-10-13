# Relationships, Cardinality and Optionality

Cardinality says how many rows can be related. Optionality says whether a related row is required. A customer can have many orders, a student can take many courses, and a student may have no profile yet. These are different rules and need different table structures.

## A many-to-many relationship

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
  student_id integer NOT NULL REFERENCES students(student_id),
  course_id integer NOT NULL REFERENCES courses(course_id),
  enrolled_on date NOT NULL,
  PRIMARY KEY (student_id, course_id)
);

INSERT INTO students VALUES (1, 'Ada'), (2, 'Ben');
INSERT INTO courses VALUES (10, 'SQL'), (20, 'Networks');
INSERT INTO enrollments VALUES
  (1, 10, '2026-01-03'), (1, 20, '2026-01-04');

SELECT s.name, c.title
FROM students AS s
LEFT JOIN enrollments AS e ON e.student_id = s.student_id
LEFT JOIN courses AS c ON c.course_id = e.course_id
ORDER BY s.student_id, c.course_id;
```

The result is `(Ada, SQL)`, `(Ada, Networks)`, and `(Ben, NULL)`. Each enrollment links exactly one student and one course. The pair is unique, so Ada cannot enroll in the same course twice. A student can have no enrollments, and a course can have no students. The left joins keep Ben in this report.

## One-to-many and one-to-one

From a student to enrollments, this is one-to-many: one student can have several enrollment rows, but each enrollment names one student. The foreign key sits in the many side. For an optional one-to-one profile, use the student's key as both the profile primary key and a foreign key:

```sql
CREATE TEMP TABLE student_profiles (
  student_id integer PRIMARY KEY REFERENCES students(student_id),
  timezone text NOT NULL
);

INSERT INTO student_profiles VALUES (1, 'Asia/Kolkata');

SELECT s.name, p.timezone
FROM students AS s
LEFT JOIN student_profiles AS p ON p.student_id = s.student_id
ORDER BY s.student_id;
```

Ada has one profile. Ben has none. The profile primary key stops a second profile for Ada. A plain foreign key without `UNIQUE` or a primary key would allow several profiles.

`NOT NULL` on a foreign key requires a value in that child row. A nullable foreign key permits a child row without a parent link. Neither choice requires every parent to have a child. For example, the enrollment foreign keys do not force every course to have at least one student. Enforcing that rule needs a careful workflow or another database mechanism.

Deletion rules are part of the relationship. PostgreSQL can reject a parent delete, cascade it, or set child foreign keys to null when their definitions allow it. Choose based on the meaning of the data. Do not cascade enrollment or order history without deciding whether that history should disappear.

## Check your understanding

1. What stops Ada from enrolling in SQL twice?
2. Why can Ben exist without an enrollment or profile?
3. Why does a foreign key on `enrollments.course_id` not require every course to have students?

## Further reading

- [PostgreSQL foreign keys and delete actions](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Chen's entity and relationship model](https://doi.org/10.1145/320434.320440)
