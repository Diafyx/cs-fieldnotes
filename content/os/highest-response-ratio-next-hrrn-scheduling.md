# Highest Response Ratio Next (HRRN) Scheduling

HRRN chooses the ready job with the highest **response ratio** when the CPU becomes free. The ratio uses both waiting time and estimated service time, so a job's chance improves as it waits. HRRN is normally shown as a nonpreemptive rule.

## Calculate the ratio

`response ratio = (waiting time + service time) / service time`

Here, service time means the next CPU burst length, and waiting time means time already spent ready for that burst. A new job has ratio `1`. A short job's ratio rises quickly, but a long job's ratio also rises if it waits. This is different from **response time**, which measures the delay before first CPU service.

Use this example to see the aging effect:

| Job | Arrival | Burst |
| --- | --- | --- |
| A | 0 | 4 |
| B | 0 | 8 |
| C | 3 | 2 |
| D | 5 | 2 |

At time 0, A and B both have ratio `1`. Break the tie by the shorter burst, so A runs `0-4`. At time 4, B has waited four units: `(4 + 8) / 8 = 1.5`. C has waited one unit: `(1 + 2) / 2 = 1.5`. Break this tie by the shorter burst, so C runs `4-6`.

At time 6, B's ratio is `(6 + 8) / 8 = 1.75`, while D's is `(1 + 2) / 2 = 1.5`. B now runs before D. The full schedule is:

| Time | Job | Ratio when chosen |
| --- | --- | --- |
| 0-4 | A | 1, tied with B. |
| 4-6 | C | 1.5, tied with B. |
| 6-14 | B | 1.75. |
| 14-16 | D | 5.5. |

The order is `A -> C -> B -> D`. B gets service ahead of a newer short job because it has waited longer.

| Job | Completion | Waiting |
| --- | --- | --- |
| A | 4 | 0 |
| B | 14 | 6 |
| C | 6 | 1 |
| D | 16 | 9 |

Average waiting time is `(0 + 6 + 1 + 9) / 4 = 4`. D still waits a long time because HRRN does not interrupt B after it starts. The ratio is recalculated when choosing a new job, not every time another job arrives.

## Where the rule gets hard

The scheduler needs an estimate of each job's service time. A poor estimate can pick the wrong job. HRRN reduces the risk of a long job waiting forever compared with always taking the shortest new job, but a simple ratio does not make every wait short. A real system also has I/O bursts, priorities, and unknown future arrivals. Work through the ready jobs at each decision point instead of sorting the whole table once.

## Try it yourself

1. Why does B not preempt A when its ratio grows during A's run?
2. Why does C beat B at time 4 under the stated tie rule?
3. At time 6, what makes B beat D despite its longer burst?
4. What would change if B's burst estimate were `16` instead of `8`?

## References

- [UC Davis HRRN scheduling example](https://nob.cs.ucdavis.edu/classes/ecs150-2022-02/handouts/sched1.html)
- [OSTEP scheduling introduction and starvation trade-offs](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf)
