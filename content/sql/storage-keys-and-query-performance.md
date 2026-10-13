# Storage, Keys and Query Performance

PostgreSQL stores table rows in a heap and keeps indexes in separate structures. A primary key protects identity and creates a unique B-tree index. A search can use that index to find a row location, then read the heap row. This path is often fast for a few matching rows, but it is not free.

## Follow one lookup

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  email text NOT NULL UNIQUE,
  name text NOT NULL
);

INSERT INTO customers VALUES
  (1, 'ada@example.test', 'Ada'),
  (2, 'ben@example.test', 'Ben'),
  (3, 'cara@example.test', 'Cara');

SELECT customer_id, name
FROM customers
WHERE customer_id = 2;
```

The answer is `(2, Ben)`. The primary key makes a second customer with ID 2 invalid. It also creates an index that can support this lookup. PostgreSQL may still scan this three-row table because reading it all can cost less than using the index. The SQL result must stay the same either way.

## What the lookup may touch

A B-tree stores ordered key entries and pointers to table row versions. An ordinary index scan first searches index pages, then visits heap pages to read requested columns and check which row version is visible to the transaction. Those heap visits can be scattered when matching rows live on many pages. If a large fraction of the table matches, scanning heap pages in order can be cheaper than many separate lookups.

An index-only scan can sometimes answer from an index when all needed columns are available there. PostgreSQL must still check visibility. It can skip a heap visit when the heap page is marked all-visible; recently changed pages often need a heap check. An index is therefore not a promise of zero heap reads.

Key choices affect more than one query. A wide primary key takes more index space and can make foreign keys and joins wider. A changing natural key can force updates through related tables. A stable, narrow key may be easier to use, while a separate `UNIQUE` rule still protects a real business identifier such as an email or SKU when that rule is valid.

In PostgreSQL, a primary key does not keep heap rows physically ordered by that key. `ORDER BY` is still needed for ordered results. Read a real `EXPLAIN (ANALYZE, BUFFERS)` plan before blaming a key or index for a slow query; the cost depends on row counts, selectivity, page reads, and the work after the lookup.

## Check your understanding

1. Why might PostgreSQL scan all three customers even though a primary key index exists?
2. Why can an index scan still read heap pages?
3. Does a primary key make `SELECT * FROM customers` return rows in key order?

## Further reading

- [PostgreSQL primary keys](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL index-only scans and heap storage](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
- [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
