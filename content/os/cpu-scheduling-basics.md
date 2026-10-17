# CPU Scheduling Basics

CPU scheduling chooses which ready job runs next. Textbook algorithms let us compare choices on a small timeline. Real systems schedule threads, but the examples in this module call each independent CPU burst a **job**. A burst is the time that job needs on the CPU before it finishes or blocks.

## Use one clear set of assumptions

The examples on the next pages use one CPU, no I/O, no context-switch cost, and these jobs:

| Job | Arrival time | CPU burst |
| --- | --- | --- |
| P1 | 0 | 8 |
| P2 | 1 | 4 |
| P3 | 2 | 2 |
| P4 | 3 | 1 |

Time units can be milliseconds or any equal unit. A job cannot run before arrival. If two choices tie, keep the current job when there is one; otherwise choose the earlier arrival, then the lower job number. Each algorithm page states any extra queue or quantum rule it needs.

## Measure the result

| Measure | Formula | What it asks |
| --- | --- | --- |
| Completion time | Time the job finishes. | When is its work done? |
| Turnaround time | Completion minus arrival. | How long from arrival to finish? |
| Waiting time | Turnaround minus CPU burst here. | How long was it ready but not running? |
| Response time | First start minus arrival. | How long until it first gets CPU time? |

The waiting formula works for these one-burst jobs with no I/O. If a job blocks, turnaround also includes I/O waiting, so subtracting only the CPU burst no longer gives ready-queue waiting time. Response time here measures first CPU service, not how long an app takes to show a visible reply.

For a simple first-come-first-serve schedule, P1 runs `0-8`, P2 `8-12`, P3 `12-14`, and P4 `14-15`. P2 arrives at 1 and starts at 8, so its response time and ready-queue wait are `7`. It completes at 12, so its turnaround is `12 - 1 = 11`.

## What a good policy depends on

Short average turnaround helps batch work. Low response time helps interactive work. Fairness matters when long-running jobs must still make progress. Throughput counts completed jobs per unit time. CPU utilization measures how much time the CPU is doing useful work, though switching and other overhead matter in real systems. No one simple rule minimizes every measure on every workload.

**Preemptive** policies can stop a job before it finishes its burst. **Nonpreemptive** policies let the selected job keep the CPU until it finishes or blocks. Preemption can help a new short or urgent job, but adds switching and can delay other work. Textbook SJF and SRTF also assume known burst lengths; an OS usually estimates future work instead of knowing it exactly.

## Try it yourself

1. In the given first-come-first-serve schedule, what are P3's turnaround and waiting times?
2. Why do waiting time and response time match for P2 in that schedule?
3. If P1 blocked for disk I/O, why would the simple waiting formula need changing?
4. Why might a policy with low average turnaround still feel slow to a user?

## References

- [OSTEP scheduling introduction and metrics](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf)
- [Linux scheduling policies](https://man7.org/linux/man-pages/man7/sched.7.html)
