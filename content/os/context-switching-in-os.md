# Context Switching in OS

A **context switch** stops one running thread and lets another run on the same CPU. The OS saves enough of the first thread's CPU state to resume it later, then restores the state of the next thread. This is how several tasks share one CPU over time.

## What changes during a switch?

A thread's CPU state includes registers, an instruction position, and a stack pointer. The kernel also needs to know which address space and other resources belong to the next task. When switching between processes, memory mapping information may change. Some cached data may become less useful, adding a cost after the switch as well as during it. The exact steps depend on the processor and OS.

| Cause | What the OS may do |
| --- | --- |
| A task waits for I/O. | Run another ready task instead of leaving the CPU idle. |
| A time slice ends. | Preempt the task and choose another ready task. |
| A more urgent task becomes ready. | Preempt the current task if the policy calls for it. |
| A task exits. | Run a different ready task. |

For example, A runs from time 0 to 3 and then waits for a disk read. B starts at time 3. If A's read completes at time 5, A becomes ready; it runs next only if the scheduling policy chooses it. The switch at time 3 lets useful work continue while A waits.

## A system call is not always a switch

An app enters the kernel when it makes a system call. The CPU changes privilege level, but the same thread may return and continue. That is a **mode change**, not necessarily a switch to another task. A timer interrupt also does not force a switch every time; the scheduler may let the current task keep running. Keep the two events separate when tracing a timeline.

The cost of a context switch includes kernel work to save and restore state. It may also disturb CPU caches or address translation caches, though the amount varies. In textbook Gantt charts, switching time is often set to zero so the scheduling rule is easy to see. For a real workload, many tiny time slices can spend noticeable time on switching. A longer slice reduces that cost but can delay a newly ready task.

Switching threads inside one process can reuse more shared state than switching between unrelated processes, but it is not free. The scheduler still has to manage execution contexts. On several CPUs, a thread may move to another CPU and lose useful local cache state. That is why CPU affinity and load balancing matter later.

## Try it yourself

1. Why must A's instruction position be saved before B runs?
2. Why does a blocking file read often lead to a context switch?
3. Can a system call finish without switching to another thread?
4. Why might a very small time slice hurt throughput even if it improves response time?

## References

- [OSTEP limited direct execution and context switches](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-mechanisms.pdf)
- [Linux scheduling policies](https://man7.org/linux/man-pages/man7/sched.7.html)
- [Linux CPU idle management](https://www.kernel.org/doc/html/latest/admin-guide/pm/cpuidle.html)
