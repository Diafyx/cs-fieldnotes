# Operating System as a Manager

The OS manages resources that many programs need at once. A manager must know who owns a resource, who is waiting, and what to do when a request cannot be met. The OS also protects shared resources so one program does not take control of another program's work by accident.

## Match each resource to a decision

| Resource | Decision the OS makes | Example |
| --- | --- | --- |
| CPU time | Which runnable task gets a logical processor next? | Let an editor respond while a download continues. |
| Memory | Which virtual pages belong to each process, and where are they backed? | Keep one app's private writes from changing another app's private memory. |
| Storage | How are file names, data blocks, and permissions handled? | Open a document and update its contents. |
| Devices | Which driver handles a request, and who may use the device? | Send sound to an audio device. |
| Network | Which socket receives arriving data? | Deliver a web response to the right process. |

The OS does not make all these decisions at one place or at one time. A CPU scheduler chooses runnable work. Memory management maps addresses and handles page faults. A file system finds data and checks operations. Drivers speak to devices. These parts cooperate, but each has a different job.

## A one-core example

Imagine A edits a document and B downloads a file on a computer with one logical CPU:

| Moment | CPU work | What the other app is doing |
| --- | --- | --- |
| 1 | A handles a key press. | B waits for network data. |
| 2 | B handles arriving data. | A waits for another key press. |
| 3 | The OS runs A again. | B writes data or waits for more. |

Only one task executes on that CPU at a given instant, but both apps can make progress over time. A task waiting for the network is not using the CPU for that wait. If both tasks are runnable, the scheduler shares CPU time according to its policy. The table is an example order, not a promise that a real scheduler alternates A and B in this pattern.

**Mechanism** is how the OS switches work, maps memory, or opens a file. **Policy** is the rule for choosing which runnable task goes next or how much memory to reclaim. A policy that improves response time for interactive work may give less immediate CPU time to a background task. Modern systems also account for priorities, CPU affinity, energy use, and machine load.

## What the manager cannot guarantee

If memory is full, the OS may reclaim cached pages, move some memory to swap, or fail a new request. If a disk is full, a file write can fail. If a program asks to read a file it cannot access, the OS should reject the request. The program must handle these outcomes. A good OS reduces conflict and provides predictable rules, but it cannot promise that every request succeeds.

The OS manages access to hardware and system resources. It does not know an application's business rule. For example, it can give two programs safe access to a file as separate operations, yet those programs can still lose an update if they both read an old value and write a new one without coordination.

## Try it yourself

1. In the table, why can B be open but use no CPU at moment 1?
2. Which OS part decides when A runs again?
3. What is the difference between the mechanism for switching tasks and the policy for choosing the next task?
4. Why can a valid file write still fail?

## References

- [Linux scheduler documentation](https://www.kernel.org/doc/html/latest/scheduler/)
- [Linux `open` errors](https://man7.org/linux/man-pages/man2/open.2.html)
- [Linux resource limits](https://man7.org/linux/man-pages/man2/getrlimit.2.html)
