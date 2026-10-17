# Shortest Remaining Time First (SRTF) Scheduling

SRTF is the preemptive form of shortest-job scheduling. At each arrival or completion, it compares the remaining CPU time of ready jobs. A newly arrived short job can interrupt the current one. Some books call the same idea shortest time to completion first, or STCF.

## Trace the shared jobs

Use P1 through P4 from [CPU Scheduling Basics](/topics/os/cpu-scheduling-basics.html). At time 1, P1 has seven units left and P2 needs four, so P2 preempts P1. At time 2, P2 has three left and P3 needs two, so P3 preempts P2. At time 3, P3 has one left and P4 also needs one. The tie rule keeps P3 running.

| Time | Running job | Remaining work after this slice |
| --- | --- | --- |
| 0-1 | P1 | P1 has 7 left. |
| 1-2 | P2 | P2 has 3 left. |
| 2-4 | P3 | P3 finishes. |
| 4-5 | P4 | P4 finishes. |
| 5-8 | P2 | P2 finishes. |
| 8-15 | P1 | P1 finishes. |

The completion times differ sharply from FCFS:

| Job | Completion | Turnaround | Waiting | Response |
| --- | --- | --- | --- | --- |
| P1 | 15 | 15 | 7 | 0 |
| P2 | 8 | 7 | 3 | 0 |
| P3 | 4 | 2 | 0 | 0 |
| P4 | 5 | 2 | 1 | 1 |

Average waiting time is `2.75`, and average turnaround is `6.5`. P1 responds at time 0 but does not finish until time 15. This shows why response and turnaround are different measures. Waiting counts all ready-queue gaps, including the time after a job has been preempted.

## What the result leaves out

These numbers assume no cost for each switch. The trace switches more often than FCFS. With a large switch cost, its measured advantage can shrink. The rule also needs a good estimate of remaining CPU time. A real task may block for I/O, change behavior, or run longer than predicted. A stream of short arrivals can keep delaying a long job.

Under the one-CPU, known-burst, zero-overhead assumptions, choosing the shortest remaining job gives a very low average completion delay. It does not optimize every individual job or make all work fair. Do not use the table as a prediction for a live OS scheduler.

## Try it yourself

1. Why does P2 stop at time 2 even though it has already started?
2. Why does P3 keep running at time 3?
3. Why is P1's response time `0` but its waiting time `7`?
4. Which new job arrival pattern could make a long job wait much longer?

## References

- [OSTEP scheduling introduction and STCF](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf)
