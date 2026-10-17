# Process Creation and Termination

A program can ask the OS to start another process. The new process gets its own identity and can run alongside the parent. Later it ends by returning from its main work, calling an exit operation, failing, or being stopped. The parent may need to collect the child's result.

## How a child starts

On Linux, a common path has two distinct steps. `fork` creates a child process with a new PID and a separate address space that initially looks like the parent's. Linux uses copy-on-write pages so it does not need to copy every data page at once. Then `execve` can replace the child's program image with another program. `execve` does **not** create a second new process; the child keeps its PID across that call.

Windows has different process creation APIs, and Python may choose among several launch methods. Do not assume every app start literally calls `fork` followed by `execve`. The general idea is still the same: create a process, prepare a program for it, and let the OS schedule its threads.

## Start and collect a child in Python

This example creates a child Python process, reads its output, and waits for its exit status. The child exits with status `3` on purpose.

```python
import subprocess
import sys

child = subprocess.Popen(
    [sys.executable, "-c", "import sys; print('child ran'); sys.exit(3)"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

stdout, stderr = child.communicate()
print(stdout.strip())
print(child.returncode)
```

The output is `child ran` and then `3`. `Popen` does not raise an exception merely because the child chose a nonzero exit status. `communicate()` waits and drains the captured output, so it is safer than waiting while a child might fill an output pipe. In a real app, inspect `stderr` and decide what the exit code means for that program.

## What ending a process means

When a process ends, the OS releases its running resources, such as its private address space and open handles. An exit status records success or failure for the parent. On Linux, a child that has ended can remain as a zombie until the parent calls a wait operation to collect that status. A long-lived parent should collect its children. If the parent dies first, another process may adopt and collect them.

An orderly exit gives the app a chance to close work. A forced stop can skip app cleanup. The OS can reclaim memory and handles, but it cannot undo an email already sent or a file already changed. Apps that need durable results must plan for a crash between steps.

Creation can also fail before the child runs, for example when a path is missing or the system refuses a new process. Always handle launch errors as well as child exit errors. A PID can be reused after the old process is gone, so an old PID by itself is not proof that a later process is the same child.

## Try it yourself

1. Which call in the common Linux path creates a new PID, and which one replaces the program image?
2. Why does `communicate()` matter when output is captured through a pipe?
3. Why can a child with exit status `3` still have printed text first?
4. What can the OS clean up after a forced stop, and what external action can it not undo?

## References

- [Linux `fork` process creation](https://man7.org/linux/man-pages/man2/fork.2.html)
- [Linux `execve` program replacement](https://man7.org/linux/man-pages/man2/execve.2.html)
- [Linux `wait` and zombie processes](https://man7.org/linux/man-pages/man2/wait.2.html)
- [Python subprocess management](https://docs.python.org/3/library/subprocess.html)
