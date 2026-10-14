# Conflict and View Serializability

A schedule is **serializable** if it has the same relevant effect as some order in which transactions run one at a time. This lets transactions overlap without giving up the meaning of a serial run. Two common tests are conflict serializability and view serializability. They are related, but they do not accept exactly the same schedules.

## Conflict serializability

Two operations conflict when they belong to different transactions, touch the same item, and at least one is a write. Read-read pairs do not conflict. The order of each pair of conflicting operations must match the order in an equivalent serial schedule.

Build a **precedence graph** with one node per transaction. Add `T1 -> T2` if a conflicting operation by T1 appears before one by T2. If the graph has no cycle, the schedule is conflict serializable. A topological order of the graph gives a valid serial order.

```text
r1(A), w1(A), r2(A), w2(B)
```

The operations on `A` give an edge `T1 -> T2`. There is no edge back, so this schedule is conflict serializable in the order T1 then T2. The write to `B` adds no cross-transaction conflict because T1 does not touch `B`.

Now consider:

```text
r1(A), r2(A), w1(A), w2(A)
```

`r2(A)` before `w1(A)` gives `T2 -> T1`. `r1(A)` before `w2(A)`, and `w1(A)` before `w2(A)`, give `T1 -> T2`. The cycle means this schedule is not conflict serializable. This is the read-then-write shape behind a lost update.

## View serializability

Two schedules are **view equivalent** when each read sees a value from the same writer, reads of the initial value stay initial reads, and the final writer of each item is the same. A schedule is view serializable if it is view equivalent to a serial schedule. Every conflict-serializable schedule is view serializable, but some view-serializable schedules fail the conflict graph test.

Here is a small example with **blind writes**, which write without first reading the item:

```text
w1(X), w2(X), w1(X), c2, c1
```

The graph has `T1 -> T2` and `T2 -> T1`, so it fails conflict serializability. There are no reads to match. T1 makes the final write, as it would in the serial order T2 then T1. It is therefore view serializable. The example explains the difference between the two definitions; it is not a recommendation to overwrite uncommitted data in a real database.

## What the tests do not say

Serializability and recoverability ask different questions. A conflict-serializable schedule can still read uncommitted data and commit in a bad order. Check the commit and read rules separately. Also, this simple read/write graph is for the classical single-version schedule model. PostgreSQL uses multiple row versions and a serializable isolation implementation with additional dependency tracking. Do not infer a live PostgreSQL transaction's safety only by drawing a graph from a few visible SQL statements.

## Try it yourself

1. Is `r1(A), r2(B), w1(A), w2(B)` conflict serializable? Which serial orders work?
2. Which two operations make the second example's `T2 -> T1` edge?
3. Why can blind writes create a view-serializable schedule with a cyclic conflict graph?

## References

- [UIC database course notes on conflict serializability](https://www.cs.uic.edu/~bglavic/cs480/2025-spring/schedule/notes/)
- [MIT transaction and locking lecture](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/10b223dc3daf6fda4001272799b153a0_MIT6_830F10_lec10.pdf)
