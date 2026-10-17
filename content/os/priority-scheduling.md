# Priority Scheduling

Priority scheduling chooses a ready job using an assigned priority. The rule must say whether a larger or smaller number means higher priority, whether a new high-priority job can preempt the current job, and how equal priorities are ordered. Without those rules, one job table can have several valid schedules.

## Use a preemptive example

Take the shared P1 through P4 jobs from [CPU Scheduling Basics](/topics/os/cpu-scheduling-basics.html). Add these priorities, where **smaller numbers mean higher priority**:

| Job | Arrival | Burst | Priority |
| --- | --- | --- | --- |
| P1 | 0 | 8 | 3 |
| P2 | 1 | 4 | 1 |
| P3 | 2 | 2 | 2 |
| P4 | 3 | 1 | 0 |

At time 1, P2 preempts P1. At time 3, P4 preempts P2. After P4 finishes, P2 resumes because it has higher priority than P3 and P1.

| Time | Running job |
| --- | --- |
| 0-1 | P1 |
| 1-3 | P2 |
| 3-4 | P4 |
| 4-6 | P2 |
| 6-8 | P3 |
| 8-15 | P1 |

P1 completes at `15` and waits for `15 - 0 - 8 = 7` units. P4 arrives at 3 and starts right away, so its response time is `0`. If the same priority rule were **nonpreemptive**, P1 would keep the CPU until time 8, then the order would be P4, P2, P3. State which form a question asks for.

## Keep low-priority work moving

A constant stream of high-priority work can keep a low-priority job ready but never running. This is starvation. **Aging** raises a waiting job's effective priority over time so it can eventually be chosen. Another policy can reserve some CPU share for lower classes. An aging rule needs a rate and limit; the word alone does not determine a schedule.

Priority can also cause **priority inversion**. A high-priority thread may wait for a lock held by a low-priority thread while medium-priority work keeps the lock holder from running. A technique such as priority inheritance can temporarily raise the lock holder's priority. This is a lock problem as well as a scheduling problem.

The numbers in this example are only a teaching convention. Linux has several scheduling classes with different priority rules; its real-time priorities use higher numbers for higher static priority. Do not copy this table's number direction into a real API without checking that API.

## Try it yourself

1. Why does P3 not preempt P2 when it arrives at time 2?
2. Which job runs just after P4 finishes, and why?
3. How would the timeline change if the rule were nonpreemptive?
4. How can aging help P1 if high-priority jobs keep arriving?

## References

- [Linux scheduling policy and priority rules](https://man7.org/linux/man-pages/man7/sched.7.html)
- [OSTEP multi-level feedback queue and priority changes](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf)
