# From SQL to an Executable Plan

SQL says what result you want. The database must decide how to get it. An **execution plan** is a tree of steps such as reading a table, applying a filter, joining rows, grouping, and sorting. Two plans can return the same rows while doing very different amounts of work.

In PostgreSQL, a query passes through these stages:

| Stage | Job |
| --- | --- |
| Parse and analyze | Check syntax, find tables and columns, and turn SQL into an internal query tree. |
| Rewrite | Apply rules, including expanding a regular view to its base-table query. |
| Plan | Compare possible ways to read and combine the data, then choose a plan using estimated costs. |
| Execute | Run the chosen plan and return rows. |

The planner can choose a table scan or an index scan, different join orders, and different ways to sort or group. It also decides where a filter can be applied. A condition on one table can often run during that table's scan, before a join creates more rows. This is a choice about execution, not a change to the query's answer.

## Follow one query

```sql
CREATE TEMP TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TEMP TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    amount INTEGER NOT NULL
);

INSERT INTO customers VALUES (1, 'Mina'), (2, 'Dev');
INSERT INTO orders VALUES (10, 1, 80), (11, 1, 20), (12, 2, 60);

CREATE TEMP VIEW large_orders AS
SELECT order_id, customer_id, amount
FROM orders
WHERE amount >= 50;

SELECT c.name, o.order_id
FROM large_orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
ORDER BY o.order_id;
```

The result is `(Mina, 10)` and `(Dev, 12)`. The view names a query; it does not hold a separate stored copy of these rows. PostgreSQL can expand the view, filter out order `11`, join the remaining orders to customers, and sort the two results. It may choose different scan or join methods as table sizes change.

To inspect the plan in PostgreSQL, run the setup above and then:

```sql
EXPLAIN
SELECT c.name, o.order_id
FROM large_orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
ORDER BY o.order_id;
```

Read the displayed tree from the lower scans upward. The top node produces the final result. An index on a join key gives the planner an option, not an order to use it. On this tiny data set, a scan may be cheaper.

## Plans and query meaning

The logical result still follows SQL rules. `WHERE` keeps rows for which its condition is true; `NULL` can make a condition unknown. An inner join can usually be rearranged in several ways. An outer join needs more care because a filter in `ON` can keep an unmatched row while a filter in `WHERE` can remove it. The planner must preserve those meanings.

The executor often asks a child node for rows as needed. A `LIMIT` can sometimes stop this work early. A sort or hash build may need many input rows before it can return its first row. This explains why two plans with similar total work can feel different when a page only needs its first few results.

Plain `EXPLAIN` estimates a plan without running a `SELECT`. `EXPLAIN (ANALYZE, BUFFERS)` runs the statement and reports actual rows, time, and buffer activity. Run the latter on a safe test query, especially for statements that change data. Plan shapes and numbers depend on data and PostgreSQL settings; the SQL result above does not.

## Try it yourself

1. Which order is removed before the join, and why?
2. Why can an index exist without appearing in the plan?
3. How could moving a right-table condition from `ON` to `WHERE` change a left join's answer?

## References

- [PostgreSQL path of a query](https://www.postgresql.org/docs/current/query-path.html)
- [PostgreSQL planner overview](https://www.postgresql.org/docs/current/planner-optimizer.html)
- [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
