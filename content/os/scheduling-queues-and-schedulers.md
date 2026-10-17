# Scheduling Queues and Schedulers

When several threads can run, the OS needs a way to choose one. It keeps track of work that is ready for a CPU and work that is waiting for something else. A **scheduler** applies a rule to the ready work. A **dispatcher** carries out the switch to the chosen thread.

## Where work waits

| Place | What it holds | What moves work out? |
| --- | --- | --- |
| Ready queue or run queue | Threads that can use a CPU now. | The scheduler chooses one to run. |
| I/O or event wait queue | Threads waiting for a disk read, network reply, lock, or other event. | The event occurs, so a thread becomes ready. |
| Admission list, in some textbook models | Jobs that have not yet been admitted to run. | A long-term admission decision. |

Suppose A is running and asks to read a file. It blocks, so it leaves the CPU. B is ready and can run. When A's read finishes, A becomes ready again. It does not jump straight from waiting to running if B still has the CPU; a scheduling decision must put it there. One process can have several threads in different states.

A ready queue need not be one literal first-in-first-out list. A kernel may use several queues, trees, or per-CPU structures. The key idea is that it can find runnable work and apply its policy. On a multicore machine, each logical CPU may have local runnable work, and the OS may move work between CPUs.

## Which scheduler is being discussed?

In a textbook, a **short-term scheduler** chooses the next ready thread for the CPU. A **long-term scheduler** decides which jobs enter the system, often in a batch-work model. A **medium-term scheduler** may suspend and later resume work to manage memory pressure. These are useful roles, not a promise that every modern OS has three separate components with those exact names. Opening an app on a desktop is not usually described by a visible batch admission queue.

The dispatcher saves the old execution context when needed, restores the new one, and lets the selected thread run. The time spent choosing and switching is overhead. A policy that switches too often can waste CPU time, even if it responds quickly to new work.

## Check the transitions

| Time | A | B | CPU choice |
| --- | --- | --- | --- |
| 0 | Running. | Ready. | A. |
| 2 | Requests I/O and waits. | Ready. | B can run. |
| 5 | I/O finishes; A becomes ready. | Running. | The policy decides whether to keep B or preempt it. |

At time 5, A's I/O completion makes it eligible. It does not by itself prove A will run immediately. Priority, time slices, and preemption rules decide that.

## Try it yourself

1. Why does a thread waiting for disk data leave the ready queue?
2. What event moves it back to ready?
3. At time 5, what extra rule would you need to know to predict the running thread?
4. Why can a system use more than one ready queue?

## References

- [Linux scheduling policies](https://man7.org/linux/man-pages/man7/sched.7.html)
- [Linux scheduler documentation](https://www.kernel.org/doc/html/latest/scheduler/)
- [OSTEP scheduling introduction](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf)
