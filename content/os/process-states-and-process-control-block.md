# Process States and Process Control Block

A process changes state as it runs, waits, and ends. The OS needs to remember enough about it to resume its work after another task uses the CPU. Textbooks call this saved information a **process control block**, or **PCB**. Real kernels may split the information among several structures and track threads separately.

## Follow a simple state model

| State | Meaning | Common next move |
| --- | --- | --- |
| New | The OS is setting up the process. | Become ready. |
| Ready | A thread can run but has no CPU right now. | The scheduler chooses it to run. |
| Running | A CPU is executing one of its threads. | Continue, wait, or return to ready. |
| Waiting or blocked | Work cannot continue until an event, such as I/O completion. | Become ready when the event arrives. |
| Terminated | The process has finished or was stopped. | The OS releases or records its remaining state. |

Suppose a program starts, prints a prompt, waits for a key, then prints a reply. Its path can be `new -> ready -> running -> waiting -> ready -> running -> terminated`. It may move between ready and running many times. A waiting thread does not become running just because the I/O completes; it becomes ready, then waits for a CPU.

This is a teaching model. Some systems also show stopped or suspended states. Linux's `/proc/<pid>/status` uses names such as `R` for running or runnable, `S` for interruptible sleep, `D` for disk sleep, `T` for stopped, and `Z` for zombie. Linux's `R` does not separate the textbook's ready and running states. A process can have several threads in different states, so one label cannot tell the whole story.

## What must the OS remember?

| Information | Why it is needed |
| --- | --- |
| Identity and parent link | Name the process and connect it to its parent. |
| Execution state | Know whether a thread may be scheduled or must wait. |
| Saved CPU context | Resume a thread at the right instruction with its register and stack state. |
| Memory map | Know which virtual addresses are valid and how to access them. |
| Open resources | Keep track of file descriptors, sockets, and other handles. |
| Credentials and limits | Check permissions and enforce resource rules. |
| Scheduling and accounting data | Decide when it runs and record resource use. |

The saved instruction position and registers belong to a thread's execution context. Threads in one process may share the memory map and open files while keeping separate stacks and saved CPU contexts. The word PCB is useful for exams, but do not assume that every OS stores exactly one fixed record with every field in it. On Linux, the kernel tracks tasks and the resources they share.

## A state transition to reason about

At time 1, thread A is running and asks to read from a slow device. It blocks. Thread B is ready, so it can run next. When A's read completes, A becomes ready; it may still wait while B runs. This is why a blocked process is different from a ready one, and why an I/O completion does not mean the process used CPU during the wait.

After a child process exits on Linux, it can appear as a **zombie** until its parent collects the exit status. It has stopped running; the kernel keeps only enough information for the parent to collect that result. This is different from a sleeping process, which can wake and continue work.

## Try it yourself

1. Why does a completed disk read move a waiting thread to ready rather than directly to running?
2. Which saved data lets a thread resume after a CPU switch?
3. Why can Linux show `R` even when a task is not executing at that instant?
4. Can a zombie process start running again? What is its parent expected to do?

## References

- [Linux process status fields and states](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)
- [Linux waiting for a child process](https://man7.org/linux/man-pages/man2/wait.2.html)
- [Linux POSIX threads](https://man7.org/linux/man-pages/man7/pthreads.7.html)
