# Algorithms for Selection, Projection, Sorting, and Aggregation

A query plan is built from small jobs. **Selection** keeps rows that meet a condition. **Projection** keeps or computes the needed columns. Sorting puts rows in an order. Aggregation combines rows into counts, sums, or groups. The database can use different algorithms for each job.

## Selection and projection

For a filter such as `amount >= 10`, a sequential scan reads table pages and checks each row. An index scan can find candidate rows through an index, then read table rows when needed. A bitmap scan can collect matches from an index and visit heap pages in a more useful order. Which is cheapest depends on how many rows match, where they are stored, and whether the needed pages are cached.

Projection may be as simple as returning two columns instead of five. It may also compute an expression, such as `amount * 2`. Returning fewer columns can reduce work and network traffic. But classic relational projection removes duplicate tuples, while ordinary SQL `SELECT` keeps duplicates. SQL needs `DISTINCT` to request duplicate removal. The planner may use a sort or a hash table to find distinct values.

## Sorting and grouping

`ORDER BY` may use rows already available in the wanted order from a suitable index. Otherwise, a sort node orders them. A large sort may write temporary data to storage when it cannot stay in memory. With `ORDER BY ... LIMIT`, PostgreSQL may use a method that keeps only the best few rows, but it still has to inspect enough input to know which rows are best.

`GROUP BY` can use a hash table with one entry per group, or process rows in group-key order after a sort or ordered scan. A plain `COUNT(*)` without grouping can use a single running count. Memory needs depend on the number of groups and the size of their state. `HAVING` tests completed groups, while `WHERE` can remove input rows before grouping. `COUNT(*)` counts rows; `COUNT(column)` ignores `NULL` in that column.

## A query with all four jobs

```sql
CREATE TEMP TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    region TEXT NOT NULL,
    amount INTEGER NOT NULL
);

INSERT INTO sales VALUES
    (1, 'East', 10),
    (2, 'East', 20),
    (3, 'East', 5),
    (4, 'West', 15),
    (5, 'West', 25),
    (6, 'North', 9);

SELECT region, COUNT(*) AS sale_count, SUM(amount) AS total
FROM sales
WHERE amount >= 10
GROUP BY region
HAVING COUNT(*) >= 2
ORDER BY total DESC, region;
```

The filter removes sales `3` and `6`. The groups left are West with two sales totaling `40`, and East with two totaling `30`. The result is `(West, 2, 40)` followed by `(East, 2, 30)`. `ORDER BY` guarantees that order. The SQL says nothing about whether PostgreSQL uses a hash aggregate or a sort-based aggregate; both can give the same answer.

To see the chosen methods after creating the table, use:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT region, COUNT(*) AS sale_count, SUM(amount) AS total
FROM sales
WHERE amount >= 10
GROUP BY region
HAVING COUNT(*) >= 2
ORDER BY total DESC, region;
```

Look for `Seq Scan` or another scan, `HashAggregate` or `GroupAggregate`, and perhaps `Sort`. This example is tiny, so its plan is for learning node names, not measuring a useful speedup. The `BUFFERS` lines show page hits and reads; they do not directly count rows.

## Common mistakes

- `LIMIT` does not always avoid reading or sorting most of the input.
- `GROUP BY` does not promise output order. Add `ORDER BY` when order matters.
- `DISTINCT` is not a free decoration. It can require extra work and may hide an unwanted join that made duplicate rows.
- A memory setting such as PostgreSQL `work_mem` applies to plan operations, not as one simple limit for the whole query. Several sorts or hashes can run in one query.

## Try it yourself

1. What changes if the example moves `amount >= 10` from `WHERE` into a condition on `SUM(amount)` in `HAVING`?
2. Why might a table scan beat an index scan when most sales qualify?
3. Why can `SELECT DISTINCT region` cost more than `SELECT region`?

## References

- [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL planner overview](https://www.postgresql.org/docs/current/planner-optimizer.html)
- [PostgreSQL memory settings](https://www.postgresql.org/docs/current/runtime-config-resource.html#RUNTIME-CONFIG-RESOURCE-MEMORY)
