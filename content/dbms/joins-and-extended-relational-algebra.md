# Joins and Extended Relational Algebra

A join combines rows from two relations using a match condition. In basic relational algebra, an inner join can be built from a Cartesian product followed by a selection. Join notation saves us from writing that longer expression.

An inner join returns matching pairs. A theta join uses any comparison condition, such as `<` or `=`. An equijoin uses equality. A natural join matches all columns that have the same name on both sides and returns one copy of each matched column. Natural joins are fragile: adding a same-named column can silently change what matches. For application queries, spell out the condition with `JOIN ... ON`.

## Missing matches

An outer join keeps unmatched rows and fills the missing side with `NULL`. A left join keeps every left row; a right join keeps every right row; a full join keeps both sides. A semijoin keeps a left row when any match exists, without adding right-side columns. An antijoin keeps a left row when no match exists. SQL commonly expresses those last two with `EXISTS` and `NOT EXISTS`.

```sql
CREATE TEMP TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TEMP TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id)
);

INSERT INTO customers VALUES (1, 'Mina'), (2, 'Dev'), (3, 'Lee');
INSERT INTO orders VALUES (100, 1), (101, 1), (102, 2);

SELECT c.name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
ORDER BY c.customer_id, o.order_id;
```

The result is `(Mina, 100)`, `(Mina, 101)`, `(Dev, 102)`, and `(Lee, NULL)`. Mina appears twice because she has two orders. A left join preserves rows, not one row per customer.

To get customers with no orders, use an antijoin:

```sql
SELECT c.name
FROM customers AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id
)
ORDER BY c.name;
```

This returns `Lee`. The matching `EXISTS` query would return Mina and Dev once each. `EXISTS` tests whether at least one matching row exists; it does not multiply customer rows.

Do not put a right-table filter in `WHERE` without checking its effect on a left join. For example, `WHERE o.order_id > 100` removes Lee because `NULL > 100` is unknown. Put a filter in `ON` when the unmatched left row must remain.

## Other extended operations

Intersection keeps tuples present in both inputs; SQL has `INTERSECT`. Division answers an "all of these" question. If `Completed(student_id, course_id)` lists completed courses and `Required(course_id)` lists required courses, division returns students who completed every required course. In SQL, a common way to express that test is a `NOT EXISTS` query that looks for a required course the student has not completed. If `Required` is empty, every candidate student passes, so choose the candidate relation carefully.

Grouping and aggregation calculate values such as a count per customer. These are extensions beyond the small set of basic operations. SQL also supports sorting with `ORDER BY`, but a mathematical relation has no order. When a join feeds a count, decide whether you mean matching rows, distinct customers, or all customers including those with zero matches.

## Try it yourself

1. How many rows would an inner join produce for the example data?
2. Write a query that returns each customer who has at least one order, once.
3. What happens to Lee if the last query is rewritten with `NOT IN` and the subquery can return `NULL`?
4. If there are no required courses, which students should the division query return?

## References

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL subquery expressions](https://www.postgresql.org/docs/current/functions-subquery.html)
