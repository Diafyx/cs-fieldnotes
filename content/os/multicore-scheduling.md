# Multicore Scheduling

Multicore scheduling decides which runnable threads use the available CPU cores. On one CPU, the scheduler chooses the next thread. With several CPUs, it must also choose **where** each thread runs. Threads on different cores can run at the same time, but they may need to share data and compete for memory.

A core is a physical execution unit. Some cores offer more than one logical CPU through hardware threads. Two logical CPUs on the same core share more hardware than two separate cores, so counting logical CPUs alone does not tell you how much work can run at full speed.

## Start with a small schedule

Assume two equally fast CPUs and three independent, CPU bound jobs. A, B, and C each need four units of CPU time. There is no switching cost.

| Time | CPU 0 | CPU 1 |
| --- | --- | --- |
| 0-4 | A | B |
| 4-8 | C | Idle |

All three jobs finish by time 8. On one CPU they would need 12 units in total. Two CPUs cannot finish them by time 4 because the total work is 12 CPU units and only eight CPU units fit into four time units. Another order could change which job finishes first, but it cannot remove the work.

If these were three threads of one program, they could also block each other on a lock. A program with only one runnable thread cannot run its own sequential instructions on two cores at once. More cores help only when there is separate runnable work and enough other resources to support it.

## One queue or several queues

A simple model keeps every runnable thread in one shared queue. An idle CPU takes the next thread. This makes it easy to see all work, but many CPUs may contend while updating the same queue. A thread can also bounce between CPUs and lose useful cache data.

Another model keeps a queue for each CPU. Each CPU mostly chooses from its own queue. This can reduce queue contention and keep a thread near its cached data. But one queue may become crowded while another CPU is idle. The scheduler then needs load balancing. Real systems may combine shared rules, CPU local queues, and topology aware placement.

## Correctness and locality

When two cores change shared data, the program needs synchronization. Hardware cache coherence helps cores see valid memory values; it does not make a sequence of several reads and writes atomic. The scheduler also has to protect its own queues when several CPUs touch them.

Moving a thread can help an idle CPU do work, but it can cost cache warmth and, on a NUMA machine, make memory access slower. The best placement depends on workload, CPU topology, and which threads can run on which CPUs. There is no promise that twice as many cores make a program twice as fast.

## Try it yourself

1. In the example, why does CPU 1 become idle after time 4?
2. What is the earliest finish time for the three jobs on three equal CPUs under the stated assumptions?
3. Why might a queue per CPU need a way to move work between queues?
4. Why does cache coherence alone not make two threads' updates to one counter safe?

## References

- [OSTEP multiprocessor scheduling](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-multi.pdf)
- [Linux scheduler domains](https://docs.kernel.org/scheduler/sched-domains.html)
