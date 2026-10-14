# Recoverable, Cascadeless, and Strict Schedules

Serializability asks whether concurrent work has a serial meaning. **Recoverability** asks whether the database can deal with a transaction abort without leaving a committed transaction dependent on work that was undone. A schedule can pass one test and fail the other.

Use `w1(X)` for transaction 1 writing item `X`, `r2(X)` for transaction 2 reading the value written by T1, `c1` for T1 committing, and `a1` for T1 aborting.

## Three levels of protection

| Class | Rule |
| --- | --- |
| Recoverable | If T2 reads a value written by T1, T2 cannot commit before T1 commits. |
| Cascadeless | T2 cannot read T1's written value until T1 commits. |
| Strict | Until T1 commits or aborts, no other transaction can read **or overwrite** a value T1 wrote. |

Every strict schedule is cascadeless, and every cascadeless schedule is recoverable. The reverse statements are false.

## Check four short schedules

```text
A: w1(X), r2(X), c2, a1
B: w1(X), r2(X), c1, c2
C: w1(X), c1, r2(X), c2
D: w1(X), w2(X), c1, c2
```

In A, T2 commits based on T1's value before T1 aborts. That is not recoverable. In B, T2 waits to commit until after T1, so it is recoverable. But T2 read uncommitted data. If T1 had aborted instead of committing, T2 would also need to abort. That is a **cascading abort**, so B is not cascadeless.

In C, T2 reads only after T1 commits. It is cascadeless and, in this simple schedule, strict. In D, there is no dirty read, so the cascadeless read rule is satisfied. But T2 overwrites X while T1's write is uncommitted, so D is not strict. A real database commonly blocks this kind of dirty write.

Strict schedules make undo simpler because no other transaction has observed or overwritten an uncommitted value. A strict locking protocol usually holds write locks until the writer finishes. PostgreSQL also uses row versions and locks so ordinary transactions do not read uncommitted writes; it does not expose all of these classroom schedules as possible SQL runs.

## A careful distinction

The word "strict" here describes a schedule's read and write order. It is not the same as choosing PostgreSQL's `SERIALIZABLE` isolation level. A schedule might be strict yet fail serializability because its committed operations form a cycle. Conversely, checking only for a serial order does not show that an abort can be handled safely.

## Try it yourself

1. Why is B recoverable but not cascadeless?
2. Which rule does D break even though nobody reads an uncommitted value?
3. Can a schedule be conflict serializable and still not recoverable? Build a short example.

## References

- [UIC database course notes on schedule classes](https://www.cs.uic.edu/~bglavic/cs480/2025-spring/schedule/notes/)
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
