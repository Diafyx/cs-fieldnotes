# First, Second, Third, and Boyce-Codd Normal Forms

Normal forms are checks on a table design. They ask whether a table mixes facts that depend on different keys. A higher normal form can remove some kinds of repetition, but it does not replace knowing the real business rules.

The definitions below use a **candidate key**, which is a smallest set of columns that identifies a row. A **prime attribute** appears in at least one candidate key. A **superkey** identifies a row but may contain extra columns. A dependency `X -> A` is nontrivial when `A` is not already in `X`.

| Form | Rule to check |
| --- | --- |
| 1NF | Each column holds one value from its chosen domain for each row. Do not pack a repeating list into one field when its items must be queried as separate facts. |
| 2NF | Be in 1NF, and have no nonprime attribute depend on a proper part of any candidate key. |
| 3NF | Be in 1NF, and for every nontrivial `X -> A`, either `X` is a superkey or `A` is prime. |
| BCNF | For every nontrivial `X -> A`, `X` is a superkey. |

BCNF is stricter than 3NF. If a table is in BCNF, it is also in 3NF. A table with a single-column candidate key cannot have a partial dependency on that key, so it passes the 2NF test, but it can still fail 3NF.

## 1NF: separate repeating values

`Customer(customer_id, phones)` with `phones = '111,222'` hides two phone facts in one text field. Use `CustomerPhone(customer_id, phone)` with one phone per row if the numbers need individual lookup, uniqueness, or updates. Atomicity depends on the chosen domain: a full name can be one text value if the application never needs its parts. SQL arrays and JSON can be useful, but choosing them does not make the underlying data rules disappear.

## 2NF: check every part of a composite key

Suppose `Enrollment(student_id, course_id, student_name, course_title, grade)` has key `(student_id, course_id)`. If `student_id -> student_name` and `course_id -> course_title`, the nonprime names depend on only part of the key. The table fails 2NF and repeats those names for every enrollment. Split it into `Student(student_id, student_name)`, `Course(course_id, course_title)`, and `Enrollment(student_id, course_id, grade)`.

## 3NF: check dependencies through other attributes

Now consider `Employee(employee_id, department_id, department_name)` with `employee_id -> department_id` and `department_id -> department_name`. Its key has one column, so it passes 2NF. It fails 3NF because `department_id` is not a superkey and `department_name` is not prime. Put the department name in `Department(department_id, department_name)` and keep `(employee_id, department_id)` in `Employee`.

## BCNF: every determinant must identify a row

A table can pass 3NF and still fail BCNF. Let `Teaching(student, course, instructor)` have these rules:

```text
(student, course) -> instructor
instructor -> course
```

Assume an instructor teaches only one course, while a course may have several instructors. The candidate keys are `(student, course)` and `(student, instructor)`. `course` is prime because it appears in a candidate key, so `instructor -> course` is allowed by 3NF. But `instructor` is not a superkey, so it breaks BCNF.

Split into `InstructorCourse(instructor, course)` and `StudentInstructor(student, instructor)` to remove that BCNF violation. This join is lossless under `instructor -> course`. However, the rule `(student, course) -> instructor` is no longer checked in one table. A student could be linked to two instructors for the same course. This is why a BCNF split can make a rule harder to enforce. The next page covers that tradeoff.

Do not decide normal form from a few current rows. First list all candidate keys and all business FDs. A nullable SQL column also needs care because classical FD theory assumes ordinary values with ordinary equality.

## Try it yourself

1. Which dependency causes the `Enrollment` example to fail 2NF?
2. Why does a one-column key not guarantee 3NF?
3. In the `Teaching` example, why does `instructor -> course` pass 3NF but fail BCNF?

## References

- [CMU notes on functional dependencies and decomposition](https://15445.courses.cs.cmu.edu/fall2017/notes/04-notes-functionaldependencies.pdf)
- [MIT Database Systems lecture on normalization](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/a9c47ed7d80c1bfc51d0baf7ac545398_MIT6_830F10_lec03.pdf)
