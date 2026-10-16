# What Happens When We Open an App?

Clicking an app icon starts a chain of work. The launcher finds what to run, the OS creates a process, and the program sets up its own state. The exact calls differ across Windows, Linux, and macOS, but the main steps are similar.

## Follow the launch

| Step | What happens |
| --- | --- |
| 1. Choose the program. | A desktop launcher, terminal, or another app asks to start an executable. |
| 2. Check access. | The OS checks the path and whether this user may run it. A missing file or denied permission can stop the launch. |
| 3. Create the process. | The OS gives the new work a process identity, an address space, and initial resources. |
| 4. Load code. | The executable's code and required shared libraries are mapped into memory. Some pages may be loaded only when used. |
| 5. Start a thread. | The first thread begins at the program's entry point. A language runtime may set up more state before the app's own code runs. |
| 6. Run and wait. | The app handles input, asks the OS for files or network data, and waits for events between bursts of CPU work. |

On Linux, one common path is to create a child process and then use `execve` to replace that child's program image with the new executable. Other launch paths exist. Python's `subprocess` chooses suitable platform APIs, so using it does not prove that every system call in the table ran in one exact order.

## Watch a child process finish

This Python example starts a second Python interpreter. It uses the current interpreter path, waits for the child to finish, and captures its output:

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-c", "print('hello from child')"],
    capture_output=True,
    text=True,
    check=True,
)

print(result.stdout.strip())
print(result.returncode)
```

The output is `hello from child` followed by `0`. The zero is the child's successful exit status. `check=True` makes Python raise an error if the child exits with a nonzero status. The child has its own process, even though the parent waits for it here. `capture_output=True` collects the child's printed text instead of showing it directly in the terminal.

A graphical app usually stays alive after showing a window. It waits for mouse, keyboard, timer, and network events. A window appearing does not mean the app has finished loading every document or network resource. If startup fails after the process begins, the OS may end that process and free its resources. The parent or launcher may get an error or exit status, but a user interface might show its own message.

## Keep creation, loading, and scheduling separate

Creating a process gives it an identity and resources. Loading prepares code to run. Scheduling decides when a runnable thread actually gets CPU time. These are related steps, but a process can exist while waiting for the CPU or for a file. Code pages may be brought into physical memory later through page faults. The whole executable need not be copied into RAM before its first instruction runs.

Closing the app usually leads to process exit and resource cleanup. The app may first save data or ask the user a question. A forced stop can skip that app-level cleanup, so important work should use durable writes and recovery rules rather than rely only on a normal close.

## Try it yourself

1. Why can a process exist before its first line of app code runs?
2. What changes in the Python example if `check=True` is removed and the child exits with an error?
3. Why can a window appear while the app is still loading data?
4. What does the OS clean up when a process ends, and what must the app save before that point?

## References

- [Python subprocess management](https://docs.python.org/3/library/subprocess.html)
- [Linux `fork` process creation](https://man7.org/linux/man-pages/man2/fork.2.html)
- [Linux `execve` program loading](https://man7.org/linux/man-pages/man2/execve.2.html)
- [Linux `wait` and child status](https://man7.org/linux/man-pages/man2/wait.2.html)
