# Multilevel Feedback Queue (MLFQ) Scheduling

MLFQ also has several ready queues, but a job can move between them. The scheduler watches how a job uses CPU time and changes its level. This helps give short or interactive work a quick turn without knowing every job's future burst length.

## State the rules before tracing

This small example uses one CPU and no context-switch cost:

1. New jobs enter Q0, the highest queue. Always run a job from the highest nonempty queue.
2. Q0 uses Round Robin with a two-unit quantum. A job that uses all two units without finishing moves to Q1.
3. Q1 uses Round Robin with a four-unit quantum. A job that uses all four units without finishing moves to Q2.
4. Q2 uses FCFS. A newly ready higher-queue job may preempt a lower-queue job.

These are rules for this example. Other MLFQ designs can use different quantum lengths, movement rules, and priority boosts.

## Follow a long job and a short job

Job A arrives at time 0 and needs eight CPU units. Job B arrives at time 2 and needs one. At time 2, A has used its full Q0 quantum and moves to Q1. B enters Q0 before the next choice.

| Time | Running job | Queue | Result |
| --- | --- | --- | --- |
| 0-2 | A | Q0 | Six units remain; A moves to Q1. |
| 2-3 | B | Q0 | B finishes. |
| 3-7 | A | Q1 | Two units remain; A moves to Q2. |
| 7-9 | A | Q2 | A finishes. |

B waits zero units because it gets the CPU as soon as it arrives. A completes at time 9 and spends one unit waiting while B runs. A long job is not thrown away when it moves down; it keeps its remaining work.

## Why the extra rules matter

If high-queue jobs keep arriving, a Q2 job can starve. A **priority boost** can periodically move waiting jobs back up, giving them another chance. The boost interval and exact movement rule change the resulting timeline. A job may also block for I/O before its quantum ends. If a scheduler lets every early block reset the job's full budget, a program could keep high priority by yielding just before the limit. Tracking total CPU allotment across turns can reduce that problem.

MLFQ uses past behavior as a hint, not proof that a job will stay short or long. A program can change phases. More queues and shorter top-level quanta can improve response for some work but add switches and tuning choices. Modern Linux's normal scheduler is not this exact toy MLFQ; use the rules stated in a problem when solving its Gantt chart.

## Try it yourself

1. Why does B run before A at time 2?
2. Why does A move to Q2 at time 7?
3. What happens to a Q2 job if Q0 never becomes empty and there is no boost?
4. Why should an I/O-bound job's use of CPU time be tracked across several short turns?

## References

- [OSTEP multi-level feedback queues](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf)
- [Linux EEVDF scheduler documentation](https://www.kernel.org/doc/html/latest/scheduler/sched-eevdf.html)
