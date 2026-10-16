# Why Do We Need an Operating System?

An operating system lets programs use a computer without each program controlling the hardware on its own. It decides which work gets CPU time, gives programs memory, stores files, handles devices, and checks access rules. It also gives programs common ways to ask for these services.

## Start with one simple request

Suppose a photo app wants to open `picture.jpg`. The app knows the file name. It does not need to know how the storage device finds blocks, which other app is reading the drive, or how to ask the device to send data. It asks the OS to open the file. The OS checks the request, finds the data through the file system, and returns a handle the app can use to read it.

This is an **abstraction**: a file is easier to work with than raw storage blocks. A process, a virtual address space, and a network socket are other abstractions. The app can use the same basic operations across different devices, while the OS and drivers handle device-specific work.

## What the OS solves

| Problem | What the OS provides | Limit to remember |
| --- | --- | --- |
| Several programs want one CPU. | Scheduling and a way to stop and resume work. | CPU time is finite; a busy app can still feel slow. |
| Programs need memory. | Private virtual address spaces and memory management. | A program can still run out of available memory. |
| Programs use disks and devices. | File systems, drivers, and device access rules. | A failed disk still needs backups and recovery. |
| Programs should not freely change each other's data. | Memory separation and permission checks. | Two apps running as the same user may share access to that user's files. |
| Programs need to talk to hardware or each other. | System calls and communication tools such as pipes and sockets. | A system call can fail or wait. |

The OS must balance these jobs. Giving one task more CPU time leaves less for others. Keeping a copy of file data in memory can speed up reads but uses RAM. The OS makes those choices using rules and current demand, not by making resources unlimited.

## Kernel, programs, and system calls

The **kernel** is the privileged part of the OS that controls core resources. An ordinary app runs with less privilege. To open a file or create a process, it asks the kernel through a system call, often through a language library. The kernel checks the arguments and access rights, does the work, and returns a result or an error.

The app still decides what to do with that result. The OS can protect a file from a process that lacks permission, but it cannot know whether a user meant to delete a photo. It cannot prevent every data mistake inside an app. It also does not make two programs that write the same file coordinate correctly unless they use suitable rules.

Some small devices run one program directly on the hardware, with no full general-purpose OS. That can work when the tasks and hardware are limited. A laptop running a browser, editor, music player, and network services needs a much richer way to share and protect resources.

## Try it yourself

1. What work would a photo app have to do if it had to read storage blocks directly?
2. Why does a private address space help when one app has a bug?
3. Can file permissions alone stop two allowed apps from overwriting each other's changes?
4. Why can an app receive an error even when it asks the OS to open a valid file name?

## References

- [Linux `open` system call](https://man7.org/linux/man-pages/man2/open.2.html)
- [Linux `execve` system call](https://man7.org/linux/man-pages/man2/execve.2.html)
- [Linux process credentials](https://man7.org/linux/man-pages/man7/credentials.7.html)
