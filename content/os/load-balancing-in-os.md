# Load Balancing in OS

Load balancing moves runnable work among CPUs so that one CPU does not sit idle while another has work waiting. It matters most when a scheduler uses separate CPU queues or when threads wake on different CPUs. The goal is useful progress, not perfectly equal queue lengths at every instant.

## A case where moving helps

Assume two equal CPUs. Two independent jobs, A and B, each need four CPU units. Both are initially on CPU 0's queue. CPU 1 has no work.

| Plan | CPU 0 | CPU 1 | Both jobs done |
| --- | --- | --- | --- |
| Leave queues alone. | A from 0-4, B from 4-8. | Idle. | Time 8. |
| Move B at time 0. | A from 0-4. | B from 0-4. | Time 4. |

This example ignores migration cost. On a real machine, moving B takes scheduler work and may lose cached data. It is still likely useful here because it avoids four units of idle CPU time. If B had only a tiny amount of work left, moving it might cost more than waiting.

## How a scheduler can balance

A busy CPU can **push** a runnable thread to another CPU, or an idle CPU can **pull** work from a busy one. The scheduler can also choose a suitable CPU when a thread wakes. A new thread does not have to begin on the same CPU as its parent.

Looking at every CPU after every small event would itself use CPU time. Looking rarely can leave one CPU idle for too long. Linux groups CPUs into scheduling domains so it can consider nearby CPUs and wider groups at different points. A machine with several NUMA nodes may prefer a nearby CPU before moving work farther away.

## What counts as load?

Two queues with two threads each are not necessarily balanced. One queue might hold threads blocked on input most of the time; the other might hold CPU bound work. Only **runnable** work is waiting for CPU service. Threads also differ in priority, allowed CPUs, recent CPU use, and how much work they are likely to do.

Affinity masks and CPU sets can forbid a move. If B may run only on CPU 0, CPU 1 must stay idle in the example even though B is waiting. A scheduler must obey the allowed CPU set. It cannot fix a limit by ignoring it.

Balancing is a tradeoff. Moving work can improve CPU use and finish times. Keeping it in place can preserve caches and local memory access. The right choice changes with the workload and machine.

## Try it yourself

1. Why does moving B cut the finish time in the example?
2. If B may use only CPU 0, can the scheduler still reach time 4? Why?
3. Why is counting every thread, including blocked threads, a poor load measure?
4. What could go wrong if the scheduler checks for imbalance too often?

## References

- [OSTEP multiprocessor scheduling](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-multi.pdf)
- [Linux CPU sets and load balancing](https://docs.kernel.org/admin-guide/cgroup-v1/cpusets.html)
- [Linux scheduler domains](https://docs.kernel.org/scheduler/sched-domains.html)
