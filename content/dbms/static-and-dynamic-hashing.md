# Static and Dynamic Hashing

Hashing turns a search key into a bucket number. A bucket holds entries whose keys map there. For an equality search, the database can go to the likely bucket instead of checking every key in order. Hashing does not keep keys sorted, so it is a poor fit for a range such as `price BETWEEN 10 AND 20`.

## Static hashing

In a simple static hash file, choose a fixed number of buckets, such as four, and send key `k` to `k % 4`. Then keys `7`, `11`, and `15` all go to bucket `3`, while `20` goes to bucket `0`. Different keys sharing a bucket are a **collision**, not a data error. The bucket must hold all of them or use an overflow area. If the file grows while the bucket count stays fixed, overflow chains can make lookups and inserts slower.

```python
keys = [7, 11, 15, 20]
buckets = {number: [] for number in range(4)}

for key in keys:
    buckets[key % 4].append(key)

for number in sorted(buckets):
    print(number, buckets[number])
```

This prints `0 [20]`, `1 []`, `2 []`, and `3 [7, 11, 15]` on separate lines. A real hash function handles many data types and tries to spread keys well; `k % 4` is only a small model.

## Dynamic hashing

Dynamic hashing grows the bucket structure as data grows. Two common textbook designs are:

| Design | How it grows | Main tradeoff |
| --- | --- | --- |
| Extendible hashing | A directory uses bits of the hash to point to buckets. A full bucket splits; the directory doubles when more bits are needed. | Fast direct lookup, but the directory takes space. |
| Linear hashing | Buckets split in a planned sequence as the file grows. It does not need a full directory. | Growth is gradual, but lookups must account for the current split position. |

In extendible hashing, **global depth** is the number of bits used by the directory, and **local depth** is the number of bits that identify one bucket. Several directory entries may point to the same bucket. A split may update only those entries; doubling is needed when a bucket's local depth must grow past the global depth. Linear hashing instead tracks a split pointer and a hash level. A bucket may temporarily have overflow pages until its turn to split.

These are ways to manage a hash file. They do not mean a SQL query performs a hash join. A hash join builds an in-memory hash table as part of one query; a hash index is a stored structure used across queries.

## PostgreSQL hash indexes

PostgreSQL has a persistent, crash-recoverable hash index. It supports one indexed column and equality comparisons only. It does not enforce uniqueness. It stores hash codes rather than full key values, so a matching hash still needs a check against the table row. Bucket pages can gain overflow pages; PostgreSQL can add buckets and split existing ones as the index grows. These implementation details are not identical to every textbook hash scheme.

```sql
CREATE TEMP TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL
);

INSERT INTO accounts VALUES
    (1, 'mina@example.test'),
    (2, 'dev@example.test'),
    (3, 'lee@example.test');

CREATE INDEX accounts_email_hash_idx
ON accounts USING HASH (email);

SELECT account_id
FROM accounts
WHERE email = 'dev@example.test';
```

The query returns `2`. It may use the hash index on a large table, but this three-row table may be cheaper to scan. If email must be unique, add a separate `UNIQUE` constraint or use a unique B-tree index. A B-tree also supports equality and can serve ranges and ordering, so compare measured plans before choosing a hash index.

## Try it yourself

1. In the four-bucket model, which bucket gets key `23`?
2. Why can a fixed bucket count become a problem as the table grows?
3. Why does a hash index not help with `email > 'm'`?
4. What is the difference between a stored hash index and a hash join?

## References

- [CMU lecture on static, extendible, and linear hashing](https://www.cs.cmu.edu/~christos/courses/dbms.S13/slides/12Hashing.pdf)
- [PostgreSQL hash indexes](https://www.postgresql.org/docs/current/hash-index.html)
- [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html)
