# Decomposition Quality and Normalization Algorithms

Decomposition splits one relation into smaller relations. A good split must let us recover every valid original row without inventing rows. It should also make important rules easy to enforce. These are two different checks.

| Check | Question |
| --- | --- |
| Lossless join | Does joining the pieces give exactly the original relation for every valid state? |
| Dependency preservation | Can the original FDs be checked using rules within individual pieces, without joining them? |
| Redundancy | Are facts still repeated in ways that cause update anomalies? |

Lossless join is essential. Dependency preservation is also valuable because a database can often enforce a local key or uniqueness rule directly. A split into BCNF can be lossless yet lose dependency preservation.

## See a lossy split

Take `R(A, B, C)` with these two rows:

```text
(1, x, p)
(2, x, q)
```

Projecting to `(A, B)` gives `(1, x)` and `(2, x)`. Projecting to `(B, C)` gives `(x, p)` and `(x, q)`. Joining those pieces on `B` gives four rows, including the false pairs `(1, x, q)` and `(2, x, p)`. The split lost information about which `A` belonged with which `C`.

If the FD `A -> B` holds, split instead into `(A, B)` and `(A, C)`. Their common attribute `A` is a key for `(A, B)`, so this two-way split is lossless. More generally, a binary split into `R1` and `R2` is lossless under the FDs if the shared attributes determine all of `R1` or all of `R2`.

## A safe SQL example

Here, `employee_id -> department_id`, so the shared employee ID is a key for the employee-to-department piece.

```sql
CREATE TEMP TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT NOT NULL
);

CREATE TEMP TABLE employee_departments (
    employee_id INTEGER PRIMARY KEY REFERENCES employees(employee_id),
    department_id INTEGER NOT NULL
);

INSERT INTO employees VALUES (1, 'Mina'), (2, 'Dev');
INSERT INTO employee_departments VALUES (1, 10), (2, 20);

SELECT e.employee_id, e.employee_name, d.department_id
FROM employees AS e
JOIN employee_departments AS d ON d.employee_id = e.employee_id
ORDER BY e.employee_id;
```

The result is `(1, Mina, 10)` and `(2, Dev, 20)`. The join does not invent a new combination because `employee_departments.employee_id` is unique. The schema still allows an employee with no department row, so whether this is a complete model depends on the business rule. Losslessness of a theoretical decomposition and mandatory participation in a real SQL schema are separate questions.

## How normalization algorithms work

For **3NF synthesis**, start from a minimal cover with one attribute on each right side. Create a relation for each FD's left and right attributes. Merge relations with the same determinant if useful, remove any relation contained in another, and add a relation containing a candidate key if none of the pieces has one. This construction gives a lossless, dependency-preserving 3NF decomposition for the stated FDs.

For **BCNF decomposition**, find a nontrivial FD `X -> Y` whose left side is not a superkey. Split `R` into `X union Y` and `R minus (Y minus X)`. Then repeat on any piece that still breaks BCNF, using the FDs that hold on that piece. The split is lossless. It may fail to preserve an FD whose attributes end up spread across pieces.

For example, the `Teaching(student, course, instructor)` design from the normal forms page has `(student, course) -> instructor` and `instructor -> course`. Splitting on `instructor -> course` gives `InstructorCourse(instructor, course)` and `StudentInstructor(student, instructor)`. It is lossless, but a rule about `(student, course)` cannot be checked in either piece alone.

Algorithms work only with the FDs you give them. Verify the business rules, candidate keys, optional rows, and the actual SQL constraints after a split. Do not assume a normal form label proves a full application design is correct.

## Try it yourself

1. Which false rows appear when `(A, B)` and `(B, C)` from the example are joined?
2. Why is a relation containing a candidate key added during 3NF synthesis if none exists yet?
3. What does the BCNF split of `Teaching` lose even though its join is lossless?

## References

- [CMU notes on schema decompositions](https://15445.courses.cs.cmu.edu/fall2017/notes/04-notes-functionaldependencies.pdf)
- [MIT Database Systems schema design lecture](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/a9c47ed7d80c1bfc51d0baf7ac545398_MIT6_830F10_lec03.pdf)
