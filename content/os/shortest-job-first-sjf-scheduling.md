# Shortest Job First (SJF) Scheduling

SJF chooses the ready job with the shortest next CPU burst. This page uses the **nonpreemptive** form: once chosen, a job runs until that burst ends or it blocks. The rule looks ahead only at jobs that have already arrived.

## Choose at each free CPU time

Use the four jobs from [CPU Scheduling Basics](/topics/os/cpu-scheduling-basics.html). At time 0, only P1 has arrived, so P1 must run even though shorter jobs will arrive later. At time 8, all other jobs are ready. Their bursts are P2 `4`, P3 `2`, and P4 `1`.

| Time | Choice | Reason |
| --- | --- | --- |
| 0-8 | P1 | The only ready job at time 0. |
| 8-9 | P4 | Shortest of the waiting jobs. |
| 9-11 | P3 | Shortest of the two left. |
| 11-15 | P2 | Last job. |

P2 starts at 11 even though it arrived at 1. Its wait is `10`. Here are all the results:

| Job | Completion | Turnaround | Waiting | Response |
| --- | --- | --- | --- | --- |
| P1 | 8 | 8 | 0 | 0 |
| P2 | 15 | 14 | 10 | 10 |
| P3 | 11 | 9 | 7 | 7 |
| P4 | 9 | 6 | 5 | 5 |

Average waiting time is `(0 + 10 + 7 + 5) / 4 = 5.5`. It is lower than FCFS's `7` for this workload, but P2 waits longer. Average turnaround is `9.25`. The average is not a promise that every job improves.

## What SJF needs to know

The scheduler cannot usually know a future CPU burst exactly. It can estimate from past bursts, but a wrong estimate changes the order. SJF also cannot choose a job that has not arrived. If short jobs keep appearing whenever the CPU becomes free, a long job may wait for a very long time. This is **starvation** if it never gets service.

When all jobs are already ready and their lengths are known, running short jobs first minimizes average waiting time under this simple single-CPU model. With different arrival times, do not sort every job by burst at time 0. Work through each decision point. SRTF adds preemption and can interrupt P1 when a new, shorter job arrives.

## Try it yourself

1. Why does P1 run first even though it has the longest burst?
2. Why is P2 worse off under SJF than under FCFS in this example?
3. What information would a real scheduler have to estimate to use this rule?
4. If P1 blocked at time 3, which ready job would SJF choose next?

## References

- [OSTEP scheduling introduction and SJF](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf)
