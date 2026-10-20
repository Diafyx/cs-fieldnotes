# Kernel in OS

The kernel is the part of an operating system that can use the computer's protected hardware controls. It manages resources that programs must share, such as CPU time, memory, and devices. A browser or text editor cannot safely decide on its own which memory belongs to another program or which bytes may be written to a disk.

An operating system includes more than its kernel. It also has system programs, libraries, and often a user interface. The kernel remains in use even when no desktop is shown.

## User mode and kernel mode

Modern processors provide a less privileged mode for ordinary programs and a privileged mode for the kernel. A program in user mode cannot directly change page tables or handle a hardware interrupt as if it owned the machine. It asks the operating system to do protected work through a **system call**. The processor then enters kernel mode at a defined entry point. The kernel checks the request, does the work if allowed, and returns a result.

This boundary protects the kernel and other processes from an ordinary program's mistakes. It does not make every program safe. A program can still corrupt its own data, and a bug in privileged kernel code can affect the whole system. Some device drivers run in kernel mode, while other drivers can run in user mode. The exact split depends on the OS.

## What the kernel does

| Job | Example |
| --- | --- |
| Manage processes and threads. | Choose a runnable thread when a CPU becomes free. |
| Manage memory. | Give a process virtual memory and stop it from reading another process's private pages. |
| Handle devices and interrupts. | Notice that a disk request has finished. |
| Provide controlled access to files and other resources. | Check access before opening a file. |
| Provide communication between processes. | Carry data through a pipe or socket. |

The details vary. For example, a microkernel may leave much file system work to a server in user mode. The kernel still supplies the protected mechanisms that let the server do its job.

## Follow one file read

Here is a small Python example:

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("hello")

with open("notes.txt", encoding="utf-8") as file:
    print(file.read())
```

It prints `hello`. Python asks the OS to open, write, and read the file. The kernel checks whether the process may access it. For the read, the kernel may return bytes already held in memory, or it may ask a storage device for data and put the thread to sleep while the device works. When the data is ready, the thread becomes runnable again. The scheduler later gives it CPU time. Python decodes the returned bytes as UTF-8 text before `print` receives the string.

This is a path through several kernel jobs, not a promise that every read goes to a disk. A cached read may need no device access. The library call may also make more than one system call.

## Kernel, process, and shell

A **process** is a running program with its own resources. A **shell** is a program that lets a user start other programs. Neither is the kernel. Closing a shell does not stop the kernel. A process can request a service from the kernel, but it does not become privileged just because it made a system call.

## Try it yourself

1. When a program asks to read a file, which part checks whether access is allowed?
2. Why can a file read finish without waiting for a disk?
3. What changes when the processor enters kernel mode for a system call?
4. Why can a faulty kernel mode driver be more damaging than a faulty text editor?

## References

- [Windows user mode and kernel mode](https://learn.microsoft.com/en-us/windows-hardware/drivers/gettingstarted/user-mode-and-kernel-mode)
- [OSTEP introduction to operating systems](https://pages.cs.wisc.edu/~remzi/OSTEP/intro.pdf)
- [MINIX 3 architecture](https://wiki.minix3.org/doku.php?id=developersguide%3Aoverviewofminixarchitecture)
