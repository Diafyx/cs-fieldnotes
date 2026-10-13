# Debugging Correctness

When a query returns the wrong answer, find the first step where rows change in an unexpected way. Check the meaning of one source row, the join keys, the filters, and the grouping level. A fast wrong query is still a bug.

## A join that changes the count

```sql
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL
);

CREATE TEMP TABLE order_items (
  order_id integer NOT NULL REFERENCES orders(order_id),
  line_number integer NOT NULL,
  amount numeric(10, 2) NOT NULL,
  PRIMARY KEY (order_id, line_number)
);

INSERT INTO orders VALUES (10, 1), (11, 1), (20, 2);
INSERT INTO order_items VALUES
  (10, 1, 25), (10, 2, 12), (10, 3, 8), (11, 1, 5);

SELECT o.customer_id, COUNT(*) AS supposed_order_count
FROM orders AS o
JOIN order_items AS i ON i.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY o.customer_id;
```

This returns `(1, 4)` and no row for customer 2. It counts item rows, not orders. Order 10 appears three times after the join, and order 20 has no items so the inner join removes it. Check the rows before grouping when a count looks too large or a group is missing.

## Count at the right level

Run this after the setup above:

```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
ORDER BY customer_id;
```

The result is `(1, 2)` and `(2, 1)`. No item join is needed to count orders. If you also need item totals, first group items by `order_id`, then left join those totals to orders. That keeps one row per order before the customer-level count. `COUNT(DISTINCT o.order_id)` can repair this one count, but it does not fix every total that a many-to-many join may multiply.

## Inspect the join before grouping

```sql
SELECT o.order_id, COUNT(i.line_number) AS item_count
FROM orders AS o
LEFT JOIN order_items AS i ON i.order_id = o.order_id
GROUP BY o.order_id
ORDER BY o.order_id;
```

The result is `(10, 3)`, `(11, 1)`, and `(20, 0)`. `COUNT(i.line_number)` ignores the null made by the unmatched left join. `COUNT(*)` would give order 20 a count of 1 because the left join still produces one output row for it. A filter on `i` in `WHERE` can also remove unmatched orders and undo the purpose of the left join.

For other wrong answers, check null handling, duplicate source rows, date boundaries, and ties in `ORDER BY`. Compare against a tiny hand-checked dataset that includes empty groups and edge dates. When changing a query for speed, run the same correctness cases before accepting the new plan.

## Check your understanding

1. Why does the first query return four instead of two for customer 1?
2. Why is customer 2 absent from the inner join result?
3. Why does `COUNT(i.line_number)` return zero for order 20 after a left join?

## Further reading

- [PostgreSQL joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
