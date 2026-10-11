# Find Quiet Students in All Exams

A quiet student took at least one exam and was never tied for the highest or lowest score in any exam they took. Return those students. Ties at either extreme count as an extreme result.

## Sample data

```sql
CREATE TEMP TABLE students (student_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE exam_results (exam_id integer, student_id integer, score integer NOT NULL);
INSERT INTO students VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara'), (4, 'Dev');
INSERT INTO exam_results VALUES
  (10, 1, 70), (10, 2, 90), (10, 3, 50),
  (20, 1, 60), (20, 2, 40), (20, 3, 80);
```

## Solution

```sql
SELECT s.student_id, s.name
FROM students AS s
WHERE EXISTS (
  SELECT 1 FROM exam_results AS taken WHERE taken.student_id = s.student_id
)
AND NOT EXISTS (
  SELECT 1
  FROM exam_results AS r
  WHERE r.student_id = s.student_id
    AND (r.score = (SELECT MAX(x.score) FROM exam_results AS x WHERE x.exam_id = r.exam_id)
      OR r.score = (SELECT MIN(x.score) FROM exam_results AS x WHERE x.exam_id = r.exam_id))
)
ORDER BY s.student_id;
```

The answer is Ana. Her scores sit between the two extremes in both exams. Ben and Cara reach an extreme. Dev took no exam, so the first `EXISTS` excludes him. The second `NOT EXISTS` means there is no exam where the student hit either extreme.

If an exam has only one result, that score is both the highest and lowest, so its student is not quiet. A unique key on `(exam_id, student_id)` would make one score per student per exam explicit.

## Check your understanding

1. Why is Dev excluded?
2. What happens if a student ties for the highest score?
3. Why does a one-person exam disqualify its student?

## Further reading

- [PostgreSQL EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
