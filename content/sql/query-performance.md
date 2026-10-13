# Query Performance

Query performance is the time and work needed to return the right result. The amount of data read, the order of rows, the number of joins, and the rows sent to the application all matter. An index helps only when it fits a real query and the planner judges it useful.

## Match an index to a filter and order

```sql
CREATE TEMP TABLE perf_sales (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  placed_on date NOT NULL,
  amount numeric(10, 2) NOT NULL
);

INSERT INTO perf_sales (order_id, customer_id, placed_on, amount)
SELECT g, (g % 100) + 1, DATE '2026-01-01' + (g % 30), 10.00
FROM generate_series(1, 10000) AS series(g);

CREATE INDEX perf_sales_customer_day_id_idx
ON perf_sales (customer_id, placed_on DESC, order_id DESC);

ANALYZE perf_sales;

SELECT order_id, placed_on
FROM perf_sales
WHERE customer_id = 7
  AND placed_on >= DATE '2026-01-10'
  AND placed_on < DATE '2026-01-20'
ORDER BY placed_on DESC, order_id DESC
LIMIT 3;
```

The result is orders `9706`, `9406`, and `9106`, all dated January 17. The index starts with the equality key `customer_id`, then follows the date and ID order used by the query. The ID settles ties on the same day. On a real table, inspect the plan to see whether the index is chosen; even a matching index can lose to a scan when many rows qualify.

## Keep filters usable

The two date comparisons form a half-open range. They can use the ordered date values directly and avoid guessing the last moment of a day. A filter that wraps an indexed column in a function, such as `date_trunc('day', placed_at) = ...` on a timestamp column, may need an expression index instead of a plain index on `placed_at`. A direct range is often simpler. For a timestamp, also decide which time zone defines the day.

Select only the columns the caller needs. A `LIMIT` cuts the number of returned rows, but it may not save much work if PostgreSQL first has to inspect or sort many rows. A large `OFFSET` still makes it skip earlier rows. For long ordered lists, a cursor based on the last seen `(placed_on, order_id)` can avoid repeatedly walking earlier pages; the sort keys must make the order stable.

Do not add an index for every column. Indexes take disk space and add work to writes. Joins may need indexes on their keys, and filters on correlated columns may need better statistics. Run `ANALYZE` after a large load, compare estimated and actual rows in `EXPLAIN`, and test with common and rare parameter values. A plan that is good for one customer can be poor for another if their data sizes differ.

Measure the whole request too. Many small queries from an application can be slower than one clear query even if each plan looks cheap. Returning thousands of unused rows also costs network and application time, which `EXPLAIN ANALYZE` does not fully measure.

## Check your understanding

1. Why does the index begin with `customer_id`?
2. Why is `order_id` part of the final sort order?
3. Why can a large `OFFSET` be slow even when the page contains ten rows?

## Further reading

- [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html)
- [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
