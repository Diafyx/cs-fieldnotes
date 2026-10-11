# Unique Subjects per Teacher

A teacher can teach the same subject in more than one department. Counting rows would count that subject more than once. Count distinct subject IDs inside each teacher's group.

## The question

Return each `teacher_id` and the number of different `subject_id` values they teach. The sample records one teacher, subject, and department per row.

```sql
CREATE TEMP TABLE teacher_subjects (
  teacher_id integer NOT NULL,
  subject_id integer NOT NULL,
  department_id integer NOT NULL,
  PRIMARY KEY (teacher_id, subject_id, department_id)
);

INSERT INTO teacher_subjects (teacher_id, subject_id, department_id) VALUES
  (1, 10, 1),
  (1, 10, 2),
  (1, 20, 1),
  (2, 10, 1),
  (2, 30, 2),
  (3, 40, 1);
```

## A solution

```sql
SELECT teacher_id,
       COUNT(DISTINCT subject_id) AS subject_count
FROM teacher_subjects
GROUP BY teacher_id
ORDER BY teacher_id;
```

The output is `(1, 2)`, `(2, 2)`, and `(3, 1)`. Teacher 1 has three rows but only two different subjects: 10 and 20. `COUNT(*)` would incorrectly report three for that teacher.

The sample has no `NULL` subject IDs. If `subject_id` were nullable, `COUNT(DISTINCT subject_id)` would ignore missing IDs. A teacher with no row in this table cannot appear with zero; that needs a separate teachers table and a join.

## Check your understanding

1. Why does teacher 1 have a count of two rather than three?
2. Would adding `department_id` to `GROUP BY` still give one row per teacher?
3. What extra table is needed to show teachers with no subjects?

## Further reading

- [LeetCode Number of Unique Subjects Taught by Each Teacher](https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
