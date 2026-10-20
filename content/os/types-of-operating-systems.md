# Types of Operating Systems

Operating systems are grouped by what they are built to do and how they share work. These groups overlap. One OS can serve many users, run on many CPUs, and meet some real time needs. A label tells you which property is being discussed; it does not name a complete design.

## By how users and jobs share the machine

| Type | Main idea | Example of the goal |
| --- | --- | --- |
| Batch system | Run submitted jobs with little direct interaction while they run. | Process a nightly set of reports. |
| Time sharing system | Switch CPU time among active users or programs so each can make progress. | Keep an editor responsive while another program compiles. |
| Single user system | Designed around one signed-in user at a time. | A small personal device. |
| Multiuser system | Keep several users' sessions and resources separate. | A shared server. |

Batch and time sharing describe **how work is served**. Single user and multiuser describe **who uses the system**. They are different questions. A modern server can process batch jobs and serve interactive users at the same time.

Time sharing does not mean every program runs at the exact same instant. On one CPU, the OS can switch among runnable threads. On several CPUs, some threads can truly run in parallel. A thread waiting for input does not need a CPU until it becomes runnable.

## By timing and device needs

An **embedded OS** runs inside a device built for a particular purpose. It may need little memory, quick startup, or direct control of sensors. A thermostat and a phone are both devices, but their software needs differ greatly. Embedded does not automatically mean real time.

A **real time OS** is designed to make the timing of important work predictable. In a hard real time task, missing a deadline is a system failure. In a soft real time task, a late result is less useful but may still be usable. A fast average response is not enough if the deadline sometimes slips. The application, hardware, interrupts, and OS all affect whether a deadline can be met.

For example, a controller may need to sample a sensor every 10 milliseconds. If a sample comes at 40 milliseconds, the average speed of the last hour does not repair that missed deadline. A normal music player has timing needs too, but one late buffer may cause a short glitch rather than a failed safety action.

## By where resources live

A **network OS** lets machines share services over a network, such as files or logins. Users can often still see which machine hosts a service. A **distributed OS** tries to manage resources on several machines as one system, hiding some location details. Real systems use different levels of this idea. A shared network folder alone does not turn several computers into one distributed OS.

A **multiprocessor OS** can schedule work on more than one CPU. This label says something about hardware use. It does not say whether the OS is batch, interactive, embedded, or real time.

## Pick the useful label

Imagine a factory controller with two CPUs. It reads a sensor at fixed intervals and sends logs to a server. It is embedded and multiprocessor. Its sensor task may have a hard deadline. Its network logging can have a softer deadline. Calling the whole machine only a "real time OS" hides these other facts.

When comparing systems, ask which property matters: number of users, response to deadlines, number of CPUs, or the place where services run. Avoid treating these labels as a single ranking from simple to advanced.

## Try it yourself

1. Can a multiuser server also run batch jobs? Explain.
2. Why does a quick average response fail to prove a hard deadline will be met?
3. Is a laptop that opens a network folder necessarily running a distributed OS?
4. Which two labels would describe a sensor device with several CPU cores?

## References

- [OSTEP introduction and history of time sharing](https://pages.cs.wisc.edu/~remzi/OSTEP/intro.pdf)
- [Linux real time preemption](https://docs.kernel.org/core-api/real-time/theory.html)
- [Zephyr introduction for embedded systems](https://docs.zephyrproject.org/latest/introduction/index.html)
- [Tanenbaum on network and distributed systems](https://www.cs.vu.nl/~ast/books/ds1/01.pdf)
