# GATE and Semester Problem Track

The official GATE 2027 CS database syllabus names ER modeling, the relational model, relational algebra, tuple calculus, SQL, integrity constraints, normal forms, file organization, indexing, transactions, and concurrency control. A semester course may add recovery, distributed systems, or vendor-specific SQL. Check your own course outline for those extra units. The questions below are original practice questions, not past GATE questions.

GATE 2027 uses multiple-choice, multiple-select, and numerical-answer questions. This page uses short written answers first because showing the reason helps you catch a lucky guess. After solving, set a time limit and check the answer without looking at the explanation. Keep separate notes for wrong concepts and careless arithmetic.

## 1. ER mapping and keys

An `Order` can have many `OrderLine` records. Each line has a number that is unique only inside its order. What is the line's full key, and where is its foreign key?

**Answer:** Use `(order_id, line_no)` as the line's key. `order_id` also refers to the parent order. Line number 1 can appear in many orders, so `line_no` alone is not a key. An order can still exist without lines unless another rule prevents it.

**Common error:** Treating a locally unique line number as globally unique.

## 2. Functional dependencies and normal forms

Let `R(A, B, C)` have dependencies `A -> B` and `B -> C`. Find `A+`, name the candidate key, and decide whether `R` is in BCNF. If not, give a lossless decomposition that preserves both dependencies.

**Answer:** Start with `{A}`. `A -> B` adds B, and `B -> C` adds C, so `A+ = {A, B, C}`. A is a candidate key. B is not a superkey of `R`, so `B -> C` breaks BCNF. Decompose into `R1(B, C)` and `R2(A, B)`. Their common attribute B determines `R1`, so the join is lossless. Each original dependency is checked inside one of the new relations.

**Common error:** Seeing that A is a key does not make every determinant a key. Test the left side of each nontrivial dependency.

## 3. SQL and NULL

A one-column table contains `5`, `NULL`, and `7`. What are `COUNT(*)`, `COUNT(x)`, and the number of rows returned by `WHERE x <> 5`?

**Answer:** `COUNT(*) = 3`; `COUNT(x) = 2`; `WHERE x <> 5` returns one row, the row with `7`. A comparison with `NULL` is unknown and is not kept by `WHERE`. Use `IS NULL` to find the missing value.

**Common error:** Treating `NULL` as zero or as a value that is unequal to every number.

## 4. Relational algebra and tuple calculus

Given `Student(sid, name)`, `Enrollment(sid, cid)`, and `Course(cid, title)`, write an algebra expression for the names of students enrolled in a course titled `DBMS`.

**Answer:** `π_name(Student ⋈ Enrollment ⋈ σ_title='DBMS'(Course))`, where both joins match columns with the same names. Filter the course first, join on `cid` and `sid`, then project the name. Under set-based relational algebra, repeated names collapse; SQL needs `DISTINCT` if the same set result is wanted.

In tuple calculus, the same result can be written as `{s.name | Student(s) and there exist e, c such that Enrollment(e), Course(c), e.sid = s.sid, e.cid = c.cid, and c.title = 'DBMS'}`. The phrase after the bar states the condition each returned name must satisfy.

**Common error:** Joining `Student` directly to `Course` without the enrollment relation, which records who took which course.

## 5. File search and B+ tree height

A heap file has 1,000 data pages and no useful index. In the worst case, how many data pages might an equality search scan? If a separate B+ tree path visits three index pages and points to one heap page, how many page reads does that path take when nothing is cached?

**Answer:** A heap scan may read all 1,000 data pages. The indexed lookup reads three index pages plus one heap page, for four reads. This simplified count ignores caching, duplicate matches, and whether an index-only scan can avoid the heap. A clustered or sorted file has different search costs.

**Common error:** Calling the B+ tree height the entire cost of fetching a row from a separate heap.

Now consider a different B+ tree question. It has room for at most three data keys per leaf and at most four child pointers per internal node. It stores 100 distinct keys. What is the smallest possible number of levels, counting the root and leaves? Assume all leaves are filled as much as possible.

**Answer:** At least `ceil(100 / 3) = 34` leaves are needed. Their parents need at least `ceil(34 / 4) = 9` nodes, then `ceil(9 / 4) = 3`, then one root. The smallest height is **four levels**. Real trees may have more leaves because pages need not be full.

**Common error:** Counting only internal levels or silently using a different definition of tree order.

## 6. Conflict serializability

Consider the schedule `r1(X), r2(Y), w1(Y), w2(X)`. Is it conflict serializable?

**Answer:** No. `r1(X)` before `w2(X)` gives an edge from T1 to T2. `r2(Y)` before `w1(Y)` gives an edge from T2 to T1. The precedence graph has a cycle, so no conflict-equivalent serial order exists. This says nothing by itself about which transaction would be stopped by a particular database.

**Common error:** Ignoring read-write conflicts because the transactions write different rows.

## 7. Recovery state

Initially A is `100` and B is `50`. T1 writes A as `80` and commits. T2 writes B as `70` but has no commit record when the system crashes. What values must a correct recovery leave visible?

**Answer:** A is `80` and B is `50`. T1's committed effect remains. T2's unfinished effect does not become a committed result. A particular recovery algorithm may redo history and then undo losers, or use another safe method, but the final transaction outcome is the same.

**Common error:** Assuming every value already written to a data page must survive as a committed value.

## Use this as a study loop

For each wrong answer, name the exact missing rule, then solve a changed version. Change the dependency in question 2, add another `NULL` in question 3, or reverse one operation in question 6. For a semester exam, add the professor's notation and units. For GATE, use the current official syllabus and official paper pattern; topics and wording can change from year to year. This site leaves out DSA and C++ by choice, so it does not cover the whole CS exam.

## References

- [Official GATE 2027 CS syllabus](https://gate2027.iitm.ac.in/static/doc/GATE2027_Syllabus/CS_GATE2027_Syllabus.pdf)
- [Official GATE 2027 question paper pattern](https://gate2027.iitm.ac.in/question_paper_pattern)
- [PostgreSQL NULL and three-valued logic](https://www.postgresql.org/docs/current/functions-comparison.html)
