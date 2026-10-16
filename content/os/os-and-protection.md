# OS and Protection

Protection is the OS's job of deciding which actions a program may take. It keeps a normal app from directly changing the kernel, another process's private memory, or a file it has no right to open. Protection makes shared computers usable, but the exact rules depend on the OS, user account, and application setup.

## Where checks happen

| Boundary | Typical check | What can fail |
| --- | --- | --- |
| App to kernel | Is this system call allowed, and are its arguments valid? | A request may return an error. |
| Process to memory | Is this address mapped with the needed access? | An invalid access may fault and end the process. |
| Process to file | Do its credentials allow this operation? | Opening a private file can be denied. |
| Process to device or service | Does it have the needed permission or capability? | A network or device operation can be refused. |

Ordinary applications run in a less privileged CPU mode than the kernel. They cannot simply execute privileged instructions or write kernel memory. A system call enters the kernel through a controlled path. The kernel checks the request before doing privileged work. This boundary matters because an app can be buggy or hostile.

## A file permission example

Imagine `notes.txt` is owned by Ana. It allows Ana to read and write, allows members of a study group to read, and allows everyone else no access. A process running with the study group's rights may read it but should not write it. A process outside that group should be denied both actions. On Linux, the kernel uses process credentials and the file's access rules when checking a request such as `open`.

This is a simplified example. Directory permissions, access control lists, administrator rights, Linux capabilities, and other security rules can change the result. A path can exist and still fail to open. The program must handle the denied request; seeing a file name is not the same as having permission to read the file.

## Separation has limits

Private process memory helps stop one ordinary process from reading or writing another process's private addresses directly. It does not automatically stop two apps running under the same account from reading the same user files. An app with your file access can still delete or upload data it is allowed to open. Some platforms add app sandbox rules and prompts for specific resources, but those rules are separate from basic process memory isolation.

Use the least access an app needs. Give a service its own account when its data should be separate. Check file and directory permissions, and remove unneeded privileges. Passwords, backups, and encryption address other risks; OS permissions alone do not cover a stolen disk or every bug in a privileged program.

## Try it yourself

1. Why does an app use a system call instead of reading disk hardware directly?
2. Why can two apps under the same user account still share access to a file?
3. In the `notes.txt` example, which process can read but not write?
4. What is the difference between private process memory and file permissions?

## References

- [Linux process credentials](https://man7.org/linux/man-pages/man7/credentials.7.html)
- [Linux `open` permission errors](https://man7.org/linux/man-pages/man2/open.2.html)
- [Linux capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [Linux kernel self-protection](https://docs.kernel.org/security/self-protection.html)
