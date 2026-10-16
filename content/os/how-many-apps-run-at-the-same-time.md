# How Many Apps Run at the Same Time?

Many apps can be open at once, but that does not mean they all use the CPU at the same instant. To answer the question, first decide whether **run** means open, ready for CPU time, or executing an instruction right now.

## Three useful states

| State | Meaning | Example |
| --- | --- | --- |
| Open or alive | The process exists. | A music player is open. |
| Runnable | A thread can run as soon as a CPU is available. | The player has audio work ready. |
| Running | A logical processor is executing that thread now. | The player mixes the next audio block. |

A process can also be blocked while it waits for disk, network, input, or a timer. Blocked work is alive but is not competing for CPU at that moment. An app can contain several threads, so counting windows or process names does not count runnable threads.

## One CPU and several CPUs

On one logical processor, only one software thread runs at a time. The scheduler switches between runnable tasks, so A, B, and C can all make progress during one second. At one instant, only one of them is using that processor. The switch takes work, so changing tasks too often also has a cost.

On four logical processors, up to four software threads can execute at an instant. Many more apps can still be open because some are waiting and runnable ones take turns. Logical processors do not always equal full physical cores; processors that share a physical core may share execution resources. A machine's available CPU count also does not tell you how much memory, I/O, or network capacity the apps need.

For example, suppose a browser has eight tabs, a music player waits for audio data, and an editor waits for typing. There is no useful fixed answer like "ten apps". Some tabs may share processes, one app may use several processes, and most of this work may be sleeping at the moment you look. A CPU monitor shows usage over an interval, not a count of every app that exists.

## What sets the practical limit?

The OS and hardware impose limits on memory, process or thread counts, open files, and CPU time. A container or job may have an even smaller quota. When memory pressure rises, the system may reclaim cache, swap some pages, or fail a request. Too many runnable CPU-bound tasks increase waiting and can make an interactive app feel slow. Many mostly idle apps can be open with little CPU use, although each still uses some memory and other resources.

Concurrency means tasks make progress over overlapping periods. Parallelism means work actually executes at the same instant on different processing units. One logical CPU can provide concurrency by switching tasks. Several logical CPUs can provide parallelism. Neither term tells you whether the tasks share memory or whether the work is split into processes or threads.

## Try it yourself

1. On one logical CPU, can three open apps all make progress during the same second? Can all three execute at one instant?
2. Why does a process waiting for a network reply not use CPU for the whole wait?
3. Why is the number of open windows a poor measure of runnable work?
4. Why can a computer with many logical CPUs still struggle with many open apps?

## References

- [Linux scheduler documentation](https://www.kernel.org/doc/html/latest/scheduler/)
- [Linux EEVDF scheduler notes](https://www.kernel.org/doc/html/latest/scheduler/sched-eevdf.html)
- [Linux process and thread limits](https://man7.org/linux/man-pages/man2/fork.2.html)
