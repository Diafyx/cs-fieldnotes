# First Come First Serve (FCFS) Scheduling

FCFS runs ready jobs in the order they arrive. Once a job gets the CPU, it keeps running until its CPU burst ends or it blocks. It is simple to trace because a later arrival does not interrupt the current job.

## Run the shared jobs

The [CPU Scheduling Basics](/topics/os/cpu-scheduling-basics.html) page gives P1 through P4 and the one-CPU assumptions. At time 0, only P1 is ready. P2, P3, and P4 arrive while P1 runs, so they wait in that order.

| Time | Running job | Why next? |
| --- | --- | --- |
| 0-8 | P1 | Arrived first. |
| 8-12 | P2 | First waiting job. |
| 12-14 | P3 | Next in the ready queue. |
| 14-15 | P4 | Last waiting job. |

The order is `P1 -> P2 -> P3 -> P4`. Use completion minus arrival for turnaround, then subtract the burst for waiting time:

| Job | Completion | Turnaround | Waiting | Response |
| --- | --- | --- | --- | --- |
| P1 | 8 | 8 | 0 | 0 |
| P2 | 12 | 11 | 7 | 7 |
| P3 | 14 | 12 | 10 | 10 |
| P4 | 15 | 12 | 11 | 11 |

Average waiting time is `(0 + 7 + 10 + 11) / 4 = 7`. Average turnaround time is `10.75`. Waiting and response are equal here because each job runs once, without preemption or I/O, after entering the ready queue.

## Why the simple rule can feel slow

P4 needs only one time unit but waits eleven units after arriving. The long P1 burst keeps every later job behind it. This is often called the **convoy effect**. A short interactive task can respond slowly even while the CPU stays busy. If P1 blocked for I/O before using all eight units, FCFS would choose another ready job; nonpreemptive does not mean a blocked task keeps the CPU.

In a real OS, a task can leave and return to the ready queue many times. Its place then depends on the policy's enqueue rule. FCFS in a textbook problem needs the arrival and ready-queue order stated clearly. It is not the same as giving the oldest installed program permanent first choice.

## Try it yourself

1. If P4 arrived at time 0 before P1, what would change in the first CPU choice?
2. Why is P3's wait `10` rather than its turnaround `12`?
3. What happens to the queue if P1 blocks at time 3?
4. Which result in the table best shows the convoy effect?

## References

- [OSTEP scheduling introduction](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf)
