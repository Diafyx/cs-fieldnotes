# Armstrong’s Axioms, Attribute Closure, and Minimal Cover

Functional dependencies can imply other dependencies. Armstrong's axioms are three sound rules for finding them. Together they are complete for ordinary functional dependencies: if an FD follows from a set of FDs, these rules can derive it.

Use letters for attribute sets. In `X -> Y`, the left side determines the right side.

| Rule | If you know | You can conclude |
| --- | --- | --- |
| Reflexivity | `Y` is part of `X` | `X -> Y` |
| Augmentation | `X -> Y` | `XZ -> YZ` |
| Transitivity | `X -> Y` and `Y -> Z` | `X -> Z` |

Useful shortcuts follow from these rules. If `X -> Y` and `X -> Z`, then `X -> YZ` (union). If `X -> YZ`, then `X -> Y` and `X -> Z` (decomposition). The letters stand for sets, so `XZ` means the union of `X` and `Z`.

## Work out a closure

Take `R(A, B, C, D, E)` with these FDs:

```text
A -> BC
B -> C
AB -> D
D -> E
```

To find `A+`, start with `{A}`. `A -> BC` adds `B` and `C`. Now `AB -> D` adds `D`. Finally `D -> E` adds `E`. So `A+ = {A, B, C, D, E}`. `A` is a key because it determines every attribute. `B+ = {B, C}`, so `B` is not a key. In this example, no FD produces `A`, so every key must contain `A`; the only candidate key is `{A}`.

Closure is also a way to test an FD: `X -> Y` follows from the known FDs exactly when every attribute in `Y` is in `X+`. Repeat the scan until a full pass adds nothing. One pass may not be enough if an FD becomes usable only after another FD fires.

## Remove extra parts: a minimal cover

A minimal cover is an equivalent set of FDs with one attribute on each right side, no extra attribute on a left side, and no FD that can be removed without changing the implied rules. More than one minimal cover can exist.

For the example, split `A -> BC` into `A -> B` and `A -> C`. `A -> C` is redundant because `A -> B` and `B -> C` already imply it. In `AB -> D`, `B` is extra: starting with `A`, we get `B`, then use `AB -> D`. Replace it with `A -> D`. One minimal cover is:

```text
A -> B
B -> C
A -> D
D -> E
```

This smaller set still implies all the original rules. Check equivalence in both directions: every old FD must follow from the new set, and every new FD must follow from the old set. Removing a line merely because it looks similar to another line can lose a real rule.

Here is a small Python closure function. It uses sets, so it works for single attributes and groups of attributes:

```python
fds = [
    ({'A'}, {'B'}),
    ({'B'}, {'C'}),
    ({'A'}, {'D'}),
    ({'D'}, {'E'}),
]

def closure(start, dependencies):
    found = set(start)
    while True:
        before = len(found)
        for left, right in dependencies:
            if left <= found:
                found.update(right)
        if len(found) == before:
            return found

print(sorted(closure({'A'}, fds)))
print(sorted(closure({'B'}, fds)))
```

The first line prints `['A', 'B', 'C', 'D', 'E']`. The second prints `['B', 'C']`. This checks the closure calculation for the minimal cover. The business rules themselves still need to come from the domain, not from the program.

## Try it yourself

1. With the original FDs, what is `D+`?
2. Show why `A -> E` follows without listing every row in a table.
3. If you delete `D -> E` from the minimal cover, which original rule stops following?

## References

- [CMU lecture notes on functional dependencies](https://15445.courses.cs.cmu.edu/fall2017/notes/04-notes-functionaldependencies.pdf)
- [MIT Database Systems lecture on schema design](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/a9c47ed7d80c1bfc51d0baf7ac545398_MIT6_830F10_lec03.pdf)
