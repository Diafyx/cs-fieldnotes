# Types of Kernel Structures

A kernel structure describes where operating system services run and how they talk to each other. The main boundary is between privileged kernel code and less privileged user processes. The names below are design patterns. A real OS can mix ideas from several patterns.

## Monolithic kernel

In a monolithic design, many core services run in kernel mode. They can call each other directly. Linux is a common example. Its kernel includes scheduling and memory management, and it can load drivers and other code as kernel modules.

Direct calls can avoid some message passing between processes. The cost is that a bug in privileged code can damage the whole kernel. **Monolithic** does not mean the source code is one file or that every feature must be built into one fixed binary. A loadable Linux module still runs with kernel privilege.

## Microkernel

A microkernel keeps a smaller set of mechanisms in kernel mode. Other services, such as file systems or drivers, can run as separate user mode servers. They send messages to the microkernel or to each other. MINIX 3 uses this approach.

Suppose an app needs a file. The request may pass to a file server, which may ask a driver server to read storage. Separate processes can limit what one failed server can change. The tradeoff is extra communication and more care in designing those interfaces. A small kernel does not guarantee that every system built on it is fast or free of bugs.

## Hybrid, modular, and layered designs

**Hybrid** is a loose name for a kernel that borrows ideas from more than one structure. It is more useful to name the actual parts than to argue whether a system fits one label. Windows, for example, has user mode components and many kernel mode services and drivers. Microsoft's documentation describes the boundary and its executive layer in detail.

**Modular** means a system can add or replace some components through defined interfaces. Linux loadable kernel modules show why modular and monolithic are not opposites: a module can be separate code yet run inside the kernel's address space.

**Layered** means components call services in lower layers through defined interfaces. Layers can make responsibilities clearer, but a design may need shortcuts or shared facilities. Layers describe organization; they do not by themselves tell you which code runs in kernel mode.

An **exokernel** is a research design that protects and shares raw hardware resources while leaving many higher level abstractions to application libraries. It is useful for seeing that an OS does not have to choose only between a large kernel and user mode servers.

## Compare one file request

| Question | Monolithic design | Microkernel design |
| --- | --- | --- |
| Where can file system code run? | In kernel mode. | In a user mode server. |
| How can components communicate? | Often direct kernel calls. | Often messages between processes. |
| What happens if that code fails? | It may damage the kernel. | Process isolation may contain the failure, though the service can still stop. |

This table shows common designs, not a rule for every implementation. Performance and reliability depend on the full system, its workload, and the quality of its code.

## Try it yourself

1. Why does loading a driver as a Linux kernel module not make it a user mode server?
2. What extra step might a microkernel system need during a file read?
3. Can a layered system also use a monolithic kernel? Why?
4. Why is "hybrid" alone a weak answer to a question about fault isolation?

## References

- [MINIX 3 architecture](https://wiki.minix3.org/doku.php?id=developersguide%3Aoverviewofminixarchitecture)
- [Windows user mode and kernel mode](https://learn.microsoft.com/en-us/windows-hardware/drivers/gettingstarted/user-mode-and-kernel-mode)
- [Windows executive layer](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/windows-kernel-mode-executive-support-library)
- [MIT exokernel project](https://pdos.csail.mit.edu/archive/exo/)
