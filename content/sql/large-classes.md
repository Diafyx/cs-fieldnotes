# Large Classes

This exercise calls a class large when it has at least five enrolled students. Group enrolments by class, count students, and use `HAVING` to keep classes that reach five.

## The question

Each row in `enrolments` is one student's place in one class. Return `class_name` and `student_count` for classes with at least five students. Sort by class name.

```sql
CREATE TEMP TABLE enrolments (
  student_id integer NOT NULL,
  class_name text NOT NULL,
  PRIMARY KEY (student_id, class_name)
);

INSERT INTO enrolments (student_id, class_name) VALUES
  (1, 'math'),
  (2, 'math'),
  (3, 'math'),
  (4, 'math'),
  (5, 'math'),
  (1, 'history'),
  (2, 'history'),
  (3, 'history'),
  (4, 'history'),
  (6, 'art');
```

## A solution

```sql
SELECT class_name, COUNT(*) AS student_count
FROM enrolments
GROUP BY class_name
HAVING COUNT(*) >= 5
ORDER BY class_name;
```

The only output row is `(math, 5)`. History has four students, and art has one. Five is included because the rule says "at least five," not "more than five."

The primary key prevents one student from appearing twice in the same class. If the source permits duplicate enrolment rows, `COUNT(*)` may overstate class size. Decide whether duplicates are errors or whether `COUNT(DISTINCT student_id)` is needed. A class with no enrolment row will not appear; listing empty classes requires a separate class table and a join.

## Check your understanding

1. Would history appear after one more student enrolled?
2. Why is the threshold in `HAVING` rather than `WHERE`?
3. How could duplicate enrolment rows change `COUNT(*)`?

## Further reading

- [LeetCode Classes With at Least 5 Students](https://leetcode.com/problems/classes-with-at-least-5-students/)
- [PostgreSQL HAVING clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-HAVING)
