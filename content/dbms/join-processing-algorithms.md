# Join Processing Algorithms

A join matches rows from two inputs. The SQL join condition says which pairs belong in the result. The database still needs an algorithm to find those pairs. PostgreSQL commonly plans nested loop, hash, or merge joins. The best choice depends on input sizes, available indexes, ordering, and the number of matches.

| Algorithm | How it works | Often useful when |
| --- | --- | --- |
| Nested loop | For each row on one side, search the other side for matches. | The outer side is small, or an index makes each inner lookup cheap. |
| Hash join | Build a hash table from one input, then probe it with rows from the other. | The join uses equality and the build side is a manageable size. |
| Merge join | Read both inputs in join-key order and move through them together. | Inputs are already ordered, or sorting them is worth the cost. |

A nested loop can test many kinds of conditions, including inequalities. Without an efficient inner lookup, it may repeat a lot of work. A hash join needs a hashable equality condition; its hash table can use more memory than expected or spill into batches. A merge join needs sortable join keys and may pay for sorting first. A stored hash **index** is different from a hash join's temporary hash table.

## Match rows and keep unmatched rows

```sql
CREATE TEMP TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TEMP TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    total INTEGER NOT NULL
);

INSERT INTO customers VALUES
    (1, 'Mina'),
    (2, 'Dev'),
    (3, 'Lee');

INSERT INTO orders VALUES
    (10, 1, 80),
    (11, 1, 20),
    (12, 2, 60);

SELECT c.name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id AND o.total >= 50
ORDER BY c.customer_id, o.order_id;
```

The result is `(Mina, 10)`, `(Dev, 12)`, and `(Lee, NULL)`. Order `11` fails the `ON` condition. Lee remains because a left join keeps every customer, even without a matching order. Moving `o.total >= 50` to `WHERE` would remove Lee, since the comparison with the missing right row is unknown.

On this small input, PostgreSQL may pick any join method it estimates to be cheap. After creating the tables, inspect its choice with:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id AND o.total >= 50
ORDER BY c.customer_id, o.order_id;
```

Read the input scans under the join node. A nested loop's inner scan may run once per outer row. In `EXPLAIN ANALYZE`, `loops` shows repeated executions and the displayed actual rows are per loop. A hash node shows hash memory and batch information. A merge join may have sort nodes below it, unless its inputs already arrive in key order. The exact plan and times are not fixed by the example data.

## Join order and row counts

With three or more tables, the planner also chooses which pair to join first. A selective filter can make one input small before it reaches a join. A wrong row-count estimate can lead to a poor choice, such as many repeated index probes or a much larger hash table than expected.

One matching row is not guaranteed. In the example, Mina has two orders before the `total` filter. Joining without that filter returns Mina twice. Adding `DISTINCT` afterward may hide a mistaken join but also adds work. First decide whether the question asks for orders, customers with any order, or customers with a count of orders.

Joins must preserve SQL meaning. Outer joins, `NULL`, and filters can limit safe reorderings. A semi-join such as `EXISTS` only asks whether a match exists; it does not need to return every matching right row. An anti-join such as `NOT EXISTS` asks whether no match exists. These forms can avoid multiplying left rows when only existence matters.

## Try it yourself

1. What rows would the main query return if the total filter were removed?
2. Why might a nested loop be good with ten outer rows and an indexed inner table?
3. Why can a hash join use extra disk space even when the final answer is small?

## References

- [PostgreSQL planner join strategies](https://www.postgresql.org/docs/current/planner-optimizer.html)
- [PostgreSQL EXPLAIN join examples](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
