# Storage Hierarchy, Pages, Records, and Buffers

A database keeps more data than can fit in memory. It stores durable data on disk and brings parts of it into memory when a query needs them. The main unit of transfer is usually a **page**, also called a block. A table row is a **record** stored inside a page.

## From a query to a row

| Level | What it holds | Why it matters |
| --- | --- | --- |
| CPU cache | Recently used machine data | Very fast, but small and managed mostly by hardware. |
| Main memory | Database buffer pages and query work | Much faster to use than reading storage again. |
| SSD or disk | Table files, indexes, and logs | Keeps data across server restarts. |

PostgreSQL normally uses 8 KiB pages, though a server can be built with another page size. Its shared buffer area caches table and index pages. The operating system can cache file data too. A query that needs a row may find its page in memory, or it may need a read from storage. Page reads, not just row counts, are a useful way to think about I/O cost.

An ordinary PostgreSQL table uses heap pages. A page has a header, an array of item pointers, free space, and the row data. A row location, called a `ctid`, contains a page number and an item position within that page. It is a physical location, not a stable business ID. An update can create a new row version, so use a primary key to identify a logical row.

Imagine a toy page that can hold four records. Ten records need at least three pages: two full pages and one page with two records. Real capacity is lower than `page size / visible column bytes` because headers, pointers, alignment, and sometimes large-value storage also take space. PostgreSQL may keep large values in a separate TOAST table.

## What a buffer does

A **buffer** is a memory slot holding one page. When a query needs a page, the buffer manager looks for it in memory. On a miss, it loads the page from storage. It tracks whether the page has been changed, often called **dirty**, and coordinates access so a page is not replaced while it is in use. A dirty page can be written back later. PostgreSQL also relies on write-ahead logging so committed changes can be recovered after a crash; writing a table page at commit time is not the basic durability rule.

The free space map helps PostgreSQL find pages with room for new rows. The visibility map records pages whose rows meet certain visibility conditions; it can help vacuum work and some index-only scans. These maps are metadata about table pages, not copies of table rows.

Try this in PostgreSQL to see the page size and some physical row locations. The `ctid` values depend on the server and on later changes, so inspect them instead of expecting fixed numbers.

```sql
SHOW block_size;

CREATE TEMP TABLE page_demo (
    id INTEGER PRIMARY KEY,
    label TEXT NOT NULL
);

INSERT INTO page_demo VALUES (1, 'one'), (2, 'two'), (3, 'three');

SELECT id, label, ctid
FROM page_demo
ORDER BY id;
```

The last query returns the three labels in ID order and a physical location for each row version. `ORDER BY id` controls the result order. The page location does not.

## Common mistakes

- A row is not the unit of disk I/O in this model. Several rows can share a page.
- A buffer hit avoids a storage read, but the query still does work to find and process the row.
- A primary key is a logical identifier. `ctid` can change and should not be saved as one.
- A dirty page waiting in memory does not mean a committed transaction lacks crash recovery. The log and data pages have different jobs.

## Try it yourself

1. If a toy page holds five records, what is the minimum number of pages for 12 records?
2. Why can a query that returns one row still read several pages?
3. Why is `ctid` unsuitable as a foreign key?

## References

- [PostgreSQL database page layout](https://www.postgresql.org/docs/current/storage-page-layout.html)
- [PostgreSQL shared buffer setting](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-SHARED-BUFFERS)
- [PostgreSQL database file layout](https://www.postgresql.org/docs/current/storage-file-layout.html)
- [PostgreSQL write-ahead logging](https://www.postgresql.org/docs/current/wal-intro.html)
