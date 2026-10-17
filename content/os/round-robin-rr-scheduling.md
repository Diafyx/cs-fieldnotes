# Round Robin (RR) Scheduling

Round Robin gives each ready job at most one **time quantum**, then puts an unfinished job at the back of the ready queue. A new arrival does not normally interrupt a job halfway through its quantum. This gives waiting jobs a chance to start before one long job finishes.

## Use a two-unit quantum

Take P1 through P4 from [CPU Scheduling Basics](/topics/os/cpu-scheduling-basics.html). The quantum is `2`. At an exact quantum boundary, place new arrivals in the queue before putting the unfinished current job at the back. If no other job is ready, the same job can keep running.

| Time | Job | What happens next? |
| --- | --- | --- |
| 0-2 | P1 | Six units remain; P2 and P3 are ready. |
| 2-4 | P2 | Two units remain; P4 has arrived. |
| 4-6 | P3 | Finishes. |
| 6-8 | P1 | Four units remain. |
| 8-9 | P4 | Finishes after one unit. |
| 9-11 | P2 | Finishes. |
| 11-13 | P1 | Two units remain. |
| 13-15 | P1 | Finishes; nobody else is ready. |

At time 2, P3 arrives exactly as P1's first quantum ends. The stated queue rule puts P3 before P1 is requeued. That small tie rule matters: changing it can change the whole schedule.

| Job | Completion | Turnaround | Waiting | Response |
| --- | --- | --- | --- | --- |
| P1 | 15 | 15 | 7 | 0 |
| P2 | 11 | 10 | 6 | 1 |
| P3 | 6 | 4 | 2 | 2 |
| P4 | 9 | 6 | 5 | 5 |

Average waiting time is `5`, and average response time is `2`. P1 responds at once, then waits during other jobs' turns. P4's one-unit burst still waits until time 8 because RR follows queue order, not shortest remaining work.

## Pick a quantum with care

A small quantum lets more jobs get an early turn, but it can cause many context switches. A very large quantum behaves more like FCFS when jobs finish before their slice ends. The best value depends on the workload and switch cost. Real tasks may block before using a full slice; when they wake, the queue policy decides where they go. RR alone does not promise equal turnaround time or the same CPU share when jobs have different priorities or block often.

## Try it yourself

1. Why does P1 run again at time 13 rather than causing a useful switch?
2. How does P2's response time differ from its waiting time?
3. What happens to the schedule if the quantum is longer than every burst?
4. Why must a problem state what happens to arrivals at a quantum boundary?

## References

- [OSTEP scheduling introduction and Round Robin](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf)
- [OSTEP context switch mechanism](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-mechanisms.pdf)
