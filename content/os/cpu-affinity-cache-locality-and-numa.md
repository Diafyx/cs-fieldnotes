# CPU Affinity, Cache Locality, and NUMA

CPU affinity is a rule or preference about which CPUs may run a thread. It can help a thread reuse data near a CPU, but it can also stop the scheduler from using an idle CPU. Cache locality and NUMA explain why moving a thread is not free.

## Affinity is about eligible CPUs

An **affinity mask** is a set of CPUs on which a thread may run. On Linux, a thread with mask `{0, 1}` may run on CPU 0 or CPU 1. It may not run on CPU 2, even if CPU 2 is idle. The OS can also impose limits through CPU sets, and a CPU can be offline. A requested mask does not override those limits.

Schedulers often prefer to run a thread on the CPU where it last ran when that is practical. This is sometimes called soft affinity. Pinning a thread to a small allowed set is a stronger limit. A preference can yield to load balancing; a hard limit cannot be ignored just to make a chart look balanced.

## Why staying near a CPU may help

CPUs keep recently used data in caches. If a thread resumes on the same CPU, some of its working data may still be nearby. If it moves, the new CPU may have to fetch that data. Hardware cache coherence keeps shared memory correct when CPUs exchange data, but it does not make a cold cache free to refill.

Consider a thread that repeatedly reads a large table. It runs on CPU 0, pauses, then resumes. If it stays on CPU 0, it may reuse some cached table data. If it moves to CPU 1, that core may need to fetch the data again. Whether this matters depends on the table size, other work that used the cache, and the CPU's cache layout. Affinity is a possible performance tool, not a promise of speed.

## NUMA adds memory distance

**NUMA** means nonuniform memory access. A machine has groups of CPUs and memory called nodes. A CPU can usually reach its node's memory faster than memory on a distant node. Threads can still use remote memory, but it may cost more time and interconnect traffic.

Imagine node 0 has CPUs 0 and 1 and node 1 has CPUs 2 and 3. A thread on CPU 0 fills a large array allocated near node 0. If it later runs on CPU 2 while the array stays on node 0, many reads may become remote. Keeping the thread near its memory could help. Moving the memory, changing allocation policy, or moving other work might help instead. Which choice wins depends on the whole workload.

## When pinning can hurt

| Situation | Possible result |
| --- | --- |
| One thread is pinned to a busy CPU while another is idle. | It waits even though spare CPU time exists. |
| A thread stays near its cached data. | It may avoid some cache misses. |
| A thread stays near memory on its NUMA node. | It may avoid slower remote memory access. |
| Too many threads are pinned to one small CPU set. | They compete there while other CPUs go unused. |

Do not pin threads just because a machine has many cores. First check whether migration or remote memory access is an actual cost for the workload. On Linux, `sched_getaffinity` reads a thread's allowed CPUs, and `sched_setaffinity` requests a new mask. These are Linux interfaces, not portable Java scheduling controls. The effective CPUs can be further limited by the system.

## Try it yourself

1. If a thread's mask is `{0, 1}`, why can CPU 2 stay idle while that thread waits?
2. Does cache coherence mean a moved thread will find its data in the new CPU's cache?
3. In the two-node example, why might CPU 2 be a poor place for a thread using node 0's large array?
4. What should you measure before pinning a thread to one CPU?

## References

- [Linux CPU affinity manual](https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html)
- [Linux NUMA overview](https://docs.kernel.org/mm/numa.html)
- [OSTEP multiprocessor scheduling](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-multi.pdf)
