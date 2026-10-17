# Program vs. Process vs. Thread

A **program** is code stored as a file or installed package. A **process** is one running instance of that program. A **thread** is a path of execution inside a process. One process begins with at least one thread and may create more.

## Keep the three apart

| Question | Program | Process | Thread |
| --- | --- | --- | --- |
| Is it running work? | No, it is stored code. | It holds a running instance's resources. | It executes instructions when scheduled. |
| Does it have an OS identity? | A file path or package name. | A PID while it exists. | A thread identity within the OS. |
| What memory does it use? | Bytes stored on disk or another medium. | A virtual address space. | Its own stack, with access to its process's shared memory. |
| Can there be several from one program? | One file may be reused. | Yes, several instances can run. | Yes, a process can have several threads. |

Two processes running the same program normally have separate private memory. Threads inside one process share much of that process's memory and open resources, but each thread has its own execution state and stack. Sharing makes communication easy, yet it also means two threads can race while changing one value. Processes can share memory deliberately, so "separate processes" does not mean sharing is impossible.

## Check identities with Python

This example starts one thread and one child process. `join()` waits for the thread. `check_output()` waits for the child and collects its printed PID.

```python
import os
import subprocess
import sys
import threading

parent_pid = os.getpid()
thread_pids = []

thread = threading.Thread(target=lambda: thread_pids.append(os.getpid()))
thread.start()
thread.join()

child_pid = int(subprocess.check_output(
    [sys.executable, "-c", "import os; print(os.getpid())"],
    text=True,
).strip())

print("thread shares process:", thread_pids == [parent_pid])
print("child has another PID:", child_pid != parent_pid)
```

Both lines print `True`. The thread calls `os.getpid()` inside the parent's process. The child has a different PID because it is a separate process while the parent is alive. The actual PID numbers change between runs. Python's runtime and OS may schedule threads differently across systems; this example checks identity, not which work ran at the same instant.

## Choose the right unit in a question

If asked "How many programs are installed?", count stored programs. If asked "How many instances are open?", count processes for the app, while remembering an app may use several processes. If asked "What does the CPU schedule?", think of runnable threads or tasks. On Linux, threads in one process share a process ID as a group but have separate thread IDs.

Starting a child process is not the same as creating a thread. It needs its own process setup and communication path. A thread shares more state, so a bug in one thread can damage data used by other threads in that process. A crash of one process is more isolated, but it can still affect other processes through shared files, services, or explicit shared memory.

## Try it yourself

1. Why can a program file exist when no process is running it?
2. Why does the thread in the Python example report the parent's PID?
3. If two threads update one list, what extra problem can arise that two private process lists would not have?
4. Can two processes share data without being the same process? Name one method.

## References

- [Linux POSIX threads](https://man7.org/linux/man-pages/man7/pthreads.7.html)
- [Linux process and thread status](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)
- [Python threading](https://docs.python.org/3/library/threading.html)
- [Python subprocess management](https://docs.python.org/3/library/subprocess.html)
