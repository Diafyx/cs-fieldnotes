# Multilevel Queue (MLQ) Scheduling

Multilevel Queue scheduling splits ready work into separate queues. A job is assigned to one queue by a fixed rule, such as job class. Each queue can use its own scheduling rule. A second rule decides how the queues share the CPU.

## Two levels of choice

Imagine two queues on one CPU:

| Queue | Jobs | Rule inside the queue |
| --- | --- | --- |
| Q0 | Foreground work. | Round Robin with a two-unit quantum. |
| Q1 | Background work. | FCFS. |

Now choose a rule **between** queues: Q0 has strict priority over Q1. A Q1 job runs only when Q0 is empty. If a Q0 job becomes ready, it preempts Q1. This interqueue rule matters as much as the rules inside the queues.

Suppose background job B arrives at time 0 and needs six CPU units. Foreground job F arrives at time 2 and needs two:

| Time | Job | Queue |
| --- | --- | --- |
| 0-2 | B | Q1 |
| 2-4 | F | Q0 |
| 4-8 | B | Q1 |

F preempts B at time 2. B later uses its remaining four CPU units. F starts immediately when it arrives, but B waits while F runs.

One foreground job does not show Q0's Round Robin rule, because F finishes in one quantum. If a second foreground job were ready, Q0 would alternate its ready jobs by the stated quantum. Q1 still uses FCFS for its own jobs.

## Assignment and fairness

In the basic MLQ model, a job stays in its assigned queue. The OS or application classifies it at entry. That can be useful when classes have clear needs, but a wrong classification can make a task wait in an unsuitable queue. Strict priority can starve Q1 if Q0 never empties.

Another interqueue rule gives both queues a share of CPU time, such as four units for Q0 and one for Q1 during a repeating five-unit period when both have work. The exact boundary and preemption rules must be stated before drawing a timeline. Sharing protects background progress at the cost of delaying some foreground work.

MLQ is a textbook pattern, not the name of one fixed Linux scheduler. A real OS may have several scheduling classes and more complex rules. Do not assume that the word "foreground" always maps to a particular kernel priority.

## Try it yourself

1. Why does F preempt B at time 2 in the example?
2. What would happen to B if Q0 always had at least one ready job under strict priority?
3. Which rule chooses between F and another foreground job?
4. How would a fixed CPU share change Q1's risk of starvation?

## References

- [Linux scheduling classes and policies](https://man7.org/linux/man-pages/man7/sched.7.html)
- [OSTEP multi-level feedback queue discussion](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf)
