# Schedules and Concurrency Anomalies

A **schedule** is the order in which operations from several transactions actually occur. A serial schedule finishes one transaction before starting the next. A concurrent schedule interleaves their operations. Interleaving can improve throughput, but some orders give an answer that no correct one-at-a-time run would give.

We can write `r1(X)` for transaction 1 reading item `X`, `w2(X)` for transaction 2 writing it, `c1` for transaction 1 committing, and `a1` for its abort. The notation describes an order of actions. It does not say which database isolation level would permit it.

## A lost update

Suppose an account starts at `100`. Transaction 1 plans to subtract `10`; transaction 2 plans to subtract `20`. Both read `100` before either writes:

```text
r1(X = 100)
r2(X = 100)
w1(X = 90)
w2(X = 80)
c1
c2
```

The final value is `80`, so transaction 1's subtraction has been lost. If both changes took effect in either serial order, the answer would be `70`. This short Python model checks the arithmetic:

```python
balance = 100
first_read = balance
second_read = balance
balance = first_read - 10
balance = second_read - 20
print(balance)
```

It prints `80`. This is an application-style read, calculate, then write pattern. In PostgreSQL `READ COMMITTED`, an update written as `UPDATE accounts SET balance = balance - 20 WHERE account_id = 1` waits for a conflicting writer and applies its expression to the updated row. A stale value calculated in application code and later written as a constant is different. Use a row lock, a version check, a suitable isolation level, or one guarded SQL update when the rule needs protection.

## Other anomalies

| Name | What happens |
| --- | --- |
| Dirty read | A transaction reads a value another transaction wrote but has not committed. If that writer aborts, the read was based on a value that never became final. |
| Nonrepeatable read | The same row is read twice and has a different committed value the second time. |
| Phantom read | Repeating a predicate query finds a different set of matching rows after another transaction changes that set. |
| Write skew | Two transactions read the same rule across several rows, then update different rows so the combined result breaks the rule. |
| Dirty write | One transaction overwrites a value another transaction wrote before that other transaction finishes. |

For write skew, imagine two doctors on call. The rule is that at least one must remain on call. Each transaction sees both doctors on call and turns off a different doctor. The writes touch different rows, so a simple same-row write conflict does not stop both. If both commit under snapshot isolation, nobody remains on call. A constraint or serializable execution is needed to protect this rule.

PostgreSQL does not allow dirty reads, even when `READ UNCOMMITTED` is requested. Its default `READ COMMITTED` can show a nonrepeatable or phantom read across two statements. Its `REPEATABLE READ` keeps a stable snapshot but can still allow a serialization anomaly such as write skew. The exact outcome of a live test also depends on locks, constraints, and the order in which statements run.

## Try it yourself

1. What final balance should both subtractions produce in a serial run?
2. How is a phantom read different from rereading one changed row?
3. Why can a same-row lock fail to protect the two-doctor rule?

## References

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [UIC database course notes on schedules](https://www.cs.uic.edu/~bglavic/cs480/2025-spring/schedule/notes/)
