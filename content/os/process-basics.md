# Process Basics

A process is a running instance of a program. It has an identity, memory it can use, resources such as open files, and at least one thread that can do work. The OS tracks it so it can schedule its work, check its access rights, and clean up when it ends.

## One program, two processes

Imagine opening the same text editor twice. Both windows may use the same program file on disk, but each running instance has its own process state. One can open `notes.txt` while the other opens `plan.txt`. If one crashes, the other may keep running. The exact number of processes depends on how that editor is built; some apps put several windows in one process, while others start more than one process for one window.

| Part of a process | Why it matters |
| --- | --- |
| Process ID, or PID | Lets the OS and other programs name the process while it exists. |
| Virtual address space | Gives the process its own view of memory. |
| Threads | Carry out instructions; the OS schedules runnable threads. |
| Open file and socket handles | Let the process keep using resources it has opened. |
| Credentials | Help the OS decide what the process may access. |
| State and accounting | Record whether work can run, must wait, or has ended. |

A PID is not a permanent name for an app or a user. The OS can reuse a PID after the old process is gone. A process can also start child processes, so one app may have several PIDs. On Linux, process details such as PID, parent PID, state, thread count, and memory sizes can be read from `/proc/<pid>/status` when permission allows.

## Active does not always mean using the CPU

Suppose the editor asks the OS to read a file. Its thread may wait while the storage work finishes. During that wait, another runnable thread can use the CPU. When the read completes, the editor becomes ready to run again. A process can therefore stay alive for hours while using almost no CPU between user actions.

The OS normally keeps processes from writing directly into each other's private memory. A process can still share data on purpose through files, pipes, sockets, or shared memory. Two processes that update the same file need their own coordination rule. Separate address spaces do not make shared data changes safe by themselves.

## A small trace to check

| Time | Editor A | Editor B |
| --- | --- | --- |
| 1 | Ready to handle a key press. | Waiting for a file read. |
| 2 | Running on a CPU. | Still waiting. |
| 3 | Waiting for the next key press. | Ready because its file read finished. |

At time 2, A uses the CPU and B does not. At time 3, B can run when a CPU is available. The table shows states, not a promise about the exact order a real scheduler will choose.

## Try it yourself

1. Why can the same editor program have two different PIDs?
2. At time 1 in the trace, which process is ready to use the CPU?
3. Does a process waiting for a file read stop existing?
4. Why should an app not store a PID as a permanent identity for a user?

## References

- [Linux process status fields](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)
- [Linux process creation](https://man7.org/linux/man-pages/man2/fork.2.html)
- [Linux process credentials](https://man7.org/linux/man-pages/man7/credentials.7.html)
