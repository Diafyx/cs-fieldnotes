# Shadow Paging, Backup, and Point-in-Time Recovery

Shadow paging is another way to make a group of page changes atomic. Backup and point-in-time recovery (PITR) solve a wider problem: they help when the current database files are lost or when a bad change was committed. These ideas belong together because a crash-safe write method does not replace a separate copy of the data.

## How shadow paging works

Think of a page table as a map from a logical page name to a physical page. The current committed map points to stable pages. A transaction that changes a page writes a **new physical page** and builds a new map. It does not overwrite the old page while readers may still need it.

| Stage | Map for logical page A | Value a new reader gets |
| --- | --- | --- |
| Before update | A points to physical page 4. | `100` |
| New page prepared | New map points A to physical page 9, which holds `120`. The committed map still points to page 4. | `100` |
| Commit | The durable root pointer switches to the new map. | `120` |

If a crash happens before the root switch, recovery follows the old map. If it happens after a durable switch, recovery follows the new map. This assumes the new pages and map are made durable **before** the root pointer is changed, and that the pointer update is atomic or protected by another safe mechanism. Without those rules, a pointer could refer to an incomplete map. Old pages can be reclaimed only when no reader or recovery path still needs them.

Copying changed pages and maps can use extra space, scatter related pages, and complicate concurrent transactions. The technique is useful for understanding copy-on-write storage, but PostgreSQL's normal table recovery uses WAL rather than this simple shadow-page scheme.

## What each PostgreSQL backup gives you

| Method | What it contains | Typical use | Limit |
| --- | --- | --- | --- |
| `pg_dump` | A logical export of one database. | Move or restore selected database objects. | It cannot be combined with physical WAL replay for PITR. |
| `pg_dumpall` | Logical exports plus cluster-wide objects such as roles. | Export a whole cluster logically. | Restore can take time and is not physical PITR. |
| `pg_basebackup` | Physical files for a PostgreSQL cluster, with needed WAL according to its options. | Restore a cluster or start a standby. | A single base backup alone cannot reach every later time. |
| Base backup plus archived WAL | Physical files and a continuous log history. | Restore the cluster to a chosen point after the backup. | Missing WAL breaks the replay chain. |

PostgreSQL PITR restores a base backup, then replays the required WAL up to a chosen target. The target can be a time or a named restore point. The base backup must be old enough for that target, and the needed WAL must form an unbroken sequence from the backup. A logical dump is useful, but it is not a physical base backup for WAL replay. Physical PITR restores a cluster, not just one table.

## Choose the right point

Suppose a base backup finishes at `09:00`. Good transactions commit at `09:10` and `09:20`. A bad `DROP TABLE` commits at `09:30`. If the WAL from the backup onward is available, recovery can stop after the `09:20` work but before the `09:30` commit. Work committed after the chosen point is absent from that restored copy, even if it was valid. Check the target and the restored data on a separate system before deciding what to bring back into service.

When recovery finishes and new writes begin, PostgreSQL creates a new **timeline**. The old history and the restored history then have different future WAL records. Keep the timeline history files along with the WAL needed for future restores. An archive gap, a backup taken after the target, or a target chosen on the wrong timeline can prevent the restore you wanted.

## Make a backup plan usable

Decide how much data loss and downtime are acceptable. Take backups often enough for that goal, keep the WAL needed for the whole retention period, and watch for archiving failures. Keep copies away from the database machine and control who can read them because backups hold the data too. Store the configuration and any needed secrets through a separate secure process; WAL archiving does not copy manually edited configuration files.

Check that a physical backup has its files and required WAL. PostgreSQL provides `pg_verifybackup` for backups with a manifest, but a verification command cannot prove that the restored application works. Regularly restore into a separate environment, run a few known queries, and time the process. This tests both the backup and the instructions for using it. A standby replica can reduce downtime, but it may faithfully repeat an accidental deletion, so keep independent backups.

## Try it yourself

1. In the shadow-page example, what must be durable before the root pointer changes?
2. Why can `pg_dump` not be paired with archived WAL for physical PITR?
3. In the `09:30` mistake example, what good work is lost if recovery stops at `09:15`?
4. Why is a successful backup job alone not proof that recovery will work?

## References

- [Database System Concepts chapter on recovery and shadow paging](https://codex.cs.yale.edu/avi/db-book/Previous-editions/db5/slide-dir/ch17.pdf)
- [PostgreSQL backup methods](https://www.postgresql.org/docs/current/backup.html)
- [PostgreSQL continuous archiving and PITR](https://www.postgresql.org/docs/current/continuous-archiving.html)
- [PostgreSQL base backup tool](https://www.postgresql.org/docs/current/app-pgbasebackup.html)
- [PostgreSQL backup verification](https://www.postgresql.org/docs/current/app-pgverifybackup.html)
