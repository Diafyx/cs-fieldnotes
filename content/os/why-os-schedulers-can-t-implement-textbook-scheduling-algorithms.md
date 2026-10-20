# Why OS Schedulers Can't Implement Textbook Scheduling Algorithms

Textbook scheduling examples give a small set of jobs, known CPU burst lengths, and a clear moment when each job arrives. A real OS sees threads that wake, sleep, make system calls, and share several CPUs. It must decide quickly with incomplete information. It can implement a simple rule such as Round Robin, but it cannot meet every ideal assumption used to show that a rule is best.

## The missing future

Shortest Job First (SJF) chooses the ready job with the shortest next CPU burst. In a worksheet, the burst length is written in a table. A general purpose OS usually cannot know how long a new thread will run before it blocks or finishes.

Imagine one CPU and these jobs:

| Job | Arrival | Actual CPU work |
| --- | --- | --- |
| A | 0 | 8 time units |
| B | 1 | 2 time units |

At time 0, only A is ready. A nonpreemptive scheduler starts A. B arrives at time 1 and cannot run until A finishes at time 8. B completes at time 10. A rule with knowledge of future arrivals could wait for B, but an ordinary scheduler cannot see B before it arrives. Even after B arrives, the OS does not know its actual two-unit burst. Preemptive SRTF would need estimates, not the numbers in the table.

An OS can estimate bursts from past behavior, but an estimate can be wrong. A thread that looked interactive may start a long computation. A CPU heavy thread may suddenly wait for input. A scheduling rule must cope when its guess fails.

## More than one goal

SJF can lower average waiting time for a known workload. Round Robin can give a quick first response. Priority scheduling can favor urgent work. None of those goals alone covers all users and tasks. A desktop may need smooth input, a server may need fair shares, and a real time task may need a deadline. A very short job should not automatically ignore a higher priority safety task.

Every context switch also costs time. A one-unit quantum in a worksheet might look fair, but if switching uses a noticeable part of that unit, less time remains for useful work. Cache data can be lost when a thread moves to another CPU. The scheduler itself must use CPU time and protect its shared data.

## Things the table leaves out

- A thread may block for disk, network, or a lock. Its next CPU burst starts only when it becomes runnable again.
- New threads can appear at any time. A scheduler cannot sort the complete future job list.
- Several CPUs can run threads at once. Placement and load balancing matter as well as run order.
- Users, groups, affinity rules, and real time policies may limit which thread may run where.
- The OS must handle interrupts and kernel work, not only the jobs drawn in a timeline.

Linux is an example of a real system with several scheduling policies. Its normal fair scheduling work has been moving from CFS toward EEVDF since Linux 6.6. EEVDF uses virtual runtime and virtual deadlines to make choices among eligible tasks. That is a policy for a real workload, not a way to know every task's future CPU burst.

The useful way to read a textbook algorithm is: **Which problem does this rule expose, and which assumptions make its result possible?** FCFS explains queue order. SJF shows the value of short jobs. Round Robin shows the response and switching tradeoff. Real schedulers borrow these ideas while handling more constraints.

## Try it yourself

1. At time 0 in the example, why can the OS not choose B?
2. If B arrives at time 1, what extra fact would SRTF need to know before choosing to preempt A?
3. Why can a smaller Round Robin quantum make performance worse?
4. Which goal might conflict with always running the shortest estimated job first?

## References

- [OSTEP scheduling introduction](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf)
- [Linux EEVDF scheduler](https://docs.kernel.org/scheduler/sched-eevdf.html)
- [Linux scheduling policies](https://man7.org/linux/man-pages/man7/sched.7.html)
