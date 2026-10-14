# Checkpoints and ARIES Intuition

A checkpoint gives crash recovery a useful place to start. Without one, a database might have to inspect a very long history of log records. A checkpoint does not mean that every transaction has committed. It records enough state, or makes enough pages durable, to limit the work needed after a crash.

## Checkpoints in PostgreSQL

PostgreSQL writes dirty data pages and a checkpoint record. After a completed checkpoint, changes before its redo point are already represented in the data files. On restart, PostgreSQL finds the latest valid checkpoint and replays WAL from the recorded redo point. Normal commits do **not** wait for a checkpoint. They rely on durable WAL.

PostgreSQL starts checkpoints based on time or WAL volume. More frequent checkpoints can shorten crash replay, but they write pages more often and can create more full page images in WAL. A checkpoint is a recovery and performance tradeoff, not a substitute for a backup. Old WAL can be recycled only when it is no longer needed for crash recovery, archiving, or other uses such as replication slots.

In PostgreSQL 18, these read-only queries show the current WAL position and checkpoint counts:

```sql
SELECT pg_current_wal_lsn();

SELECT num_timed, num_requested, num_done, buffers_written
FROM pg_stat_checkpointer;
```

The LSN is a position, not a count of transactions. `num_timed` and `num_requested` count checkpoint requests; `num_done` counts completed checkpoints. Their values depend on server activity and when statistics were reset. Older PostgreSQL releases may expose checkpoint statistics in a different view. You do not need to run `CHECKPOINT` just to inspect these values.

## Why ARIES is taught

ARIES is a recovery algorithm described in database research. It explains how a system can let uncommitted dirty pages reach disk (**steal**) and still avoid writing every changed page at commit (**no-force**). It uses WAL and three restart passes:

| Pass | Question it answers | Main result |
| --- | --- | --- |
| Analysis | Which transactions were active, and which pages might be dirty? | A transaction table and dirty page table. |
| Redo | Which logged changes are missing from data pages? | The database state is brought forward to the crash point, including some uncommitted work. |
| Undo | Which transactions never committed? | Their effects are removed. |

The **dirty page table** records pages that may have changes missing from disk. Its `recLSN` is the first log record that made a page dirty since it was last known clean. Redo can start at the smallest relevant `recLSN`. A page's `pageLSN` tells recovery which log record is already reflected on that page. Recovery checks these values instead of blindly writing every log record again.

ARIES can use a **fuzzy checkpoint**. It records a snapshot of useful tables while transactions and page writes continue. The checkpoint is a starting hint for analysis; it does not freeze the whole database. This differs from the simple idea that every dirty page must be forced to disk at each checkpoint. Do not assume PostgreSQL runs ARIES's three passes. PostgreSQL has its own WAL and MVCC recovery design.

## Work through a small ARIES log

Start with durable pages `A = 100` and `B = 50`. Assume the checkpoint is before the following log records, and that all listed records are durable when the server crashes.

| LSN | Record |
| --- | --- |
| 20 | T1 sets A to `80`. |
| 30 | T2 sets B to `60`. |
| 40 | T1 commits. |
| 50 | T2 sets A to `85`. |
| Crash | Some changed pages may or may not have reached disk. |

Analysis finds T1 committed and T2 unfinished. Redo repeats any changes the pages still need, so it can temporarily reconstruct `A = 85` and `B = 60`. Undo then reverses T2's LSN `50` and `30`. The final committed state is `A = 80`, `B = 50`. The actual page writes before the crash do not change that answer because redo checks what each page already has.

When ARIES undoes a change, it writes a **compensation log record** (CLR). The CLR records that an undo step happened and where undo should continue. If the server crashes again during recovery, redo can repeat the CLR and undo can resume without undoing that same action a second time. A CLR is not itself undone. This is one reason ARIES can recover from a crash during recovery.

## Common mistakes

- A checkpoint is not a commit. A transaction open at a checkpoint can still abort later.
- Redo in ARIES is not limited to committed transactions. It repeats history first; undo handles the losers afterward.
- A smaller checkpoint interval is not always faster overall. It can increase normal I/O and WAL volume.
- `pageLSN` is a page's progress marker, while `recLSN` points to the oldest possibly missing change for a dirty page.

## Try it yourself

1. Why does the example redo T2's changes if T2 never committed?
2. Which ARIES pass decides that T2 needs undo?
3. What would a second crash during undo require if there were no compensation log records?

## References

- [Original ARIES paper from IBM Research](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging)
- [PostgreSQL checkpoint and WAL configuration](https://www.postgresql.org/docs/current/wal-configuration.html)
- [PostgreSQL checkpoint statistics](https://www.postgresql.org/docs/current/monitoring-stats.html)
- [PostgreSQL WAL internals](https://www.postgresql.org/docs/current/wal-internals.html)
