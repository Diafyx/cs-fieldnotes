# Index Strategy at Scale

An index strategy starts with a workload: the filters, joins, sort orders, and row counts that matter most. Each index should serve a clear query or enforce a clear rule. More indexes can make reads faster, but they also consume space and add work to inserts, updates, and deletes.

## Index one important queue query

```sql
CREATE TEMP TABLE work_orders (
  order_id bigint PRIMARY KEY,
  tenant_id bigint NOT NULL,
  placed_at timestamp NOT NULL,
  status text NOT NULL CHECK (status IN ('pending', 'paid')),
  amount numeric(10, 2) NOT NULL
);

INSERT INTO work_orders VALUES
  (101, 1, '2026-01-01 09:00:00', 'pending', 10),
  (102, 1, '2026-01-03 09:00:00', 'pending', 20),
  (103, 1, '2026-01-02 09:00:00', 'pending', 30),
  (104, 1, '2026-01-04 09:00:00', 'paid', 40),
  (201, 2, '2026-01-05 09:00:00', 'pending', 50);

CREATE INDEX work_orders_pending_recent_idx
ON work_orders (tenant_id, placed_at DESC, order_id DESC)
INCLUDE (amount)
WHERE status = 'pending';

SELECT order_id, placed_at, amount
FROM work_orders
WHERE tenant_id = 1 AND status = 'pending'
ORDER BY placed_at DESC, order_id DESC
LIMIT 3;
```

The query returns orders `102`, `103`, and `101` in that order. Order 104 is paid, and order 201 belongs to another tenant. The index stores only pending rows. Its leading key finds one tenant, and the next keys match the requested order. `amount` is included as payload for a possible index-only scan; it is not used to guide the search. PostgreSQL may still scan the tiny sample table because that can be cheaper.

## Choose the shape from the query

A B-tree fits equality, ranges, and ordered reads on sortable values. In a multicolumn B-tree, leading equality conditions followed by a range or order are usually the strongest fit. PostgreSQL can sometimes use later columns through skip scan, so the leftmost rule is a guide, not an absolute ban. An expression index can match a frequent computed filter such as `lower(email)`. A partial index can stay smaller when queries focus on a stable subset, such as pending orders. The query condition must imply the partial index condition; a generic prepared plan may not prove that a status parameter always means `pending`.

GIN can help containment searches in JSONB or arrays. BRIN summarizes page ranges and can be useful for very large tables whose timestamp values follow physical row order. These index types answer different questions. Choose from actual predicates, not from table size alone.

`INCLUDE` columns can help an index-only scan when all needed values are in the index, but PostgreSQL still needs visibility information from heap pages. Recently changed rows often require heap visits. Extra payload also makes the index larger. A primary or unique constraint already creates an index, so do not add an identical one. Foreign keys on child tables do not automatically get their own indexes in PostgreSQL; frequent joins or parent deletes may justify one.

For an existing large production table, `CREATE INDEX CONCURRENTLY` lets normal writes continue during the build, but takes more work and cannot run inside a transaction block. A failed concurrent build can leave an invalid index that needs attention. Test the query before and after with `EXPLAIN (ANALYZE, BUFFERS)`, check common and rare parameter values, and keep an eye on write cost and total index size. Remove an index only after checking which queries and constraints use it.

## Check your understanding

1. Why is `status = 'pending'` in the index condition instead of a key column here?
2. Does `INCLUDE (amount)` guarantee that the heap is never read?
3. Why might an index that helps this queue query make writes slower?

## Further reading

- [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html)
- [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html)
- [PostgreSQL CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)
