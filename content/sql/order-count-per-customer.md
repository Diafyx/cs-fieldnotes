# Order Count per Customer

Count each customer's orders, including customers with no orders. Return one row per customer.

## Sample data

```sql
CREATE TEMP TABLE customers (customer_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE orders (order_id integer PRIMARY KEY, customer_id integer NOT NULL);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara');
INSERT INTO orders VALUES (10, 1), (11, 1), (12, 2);
```

## Solution

```sql
SELECT c.customer_id, c.name,
       (SELECT COUNT(*)
        FROM orders AS o
        WHERE o.customer_id = c.customer_id) AS order_count
FROM customers AS c
ORDER BY c.customer_id;
```

The result is Ana with 2, Ben with 1, and Cara with 0. The scalar subquery is correlated to the current customer. `COUNT(*)` returns zero when it finds no order rows, so Cara stays in the output. The primary key on `order_id` makes each order count once.

A left join with `GROUP BY` can answer the same question. With that form, count `o.order_id`, not `COUNT(*)`, because the unmatched customer still has one null-extended join row. If only paid orders count, place that filter inside the subquery so customers with no paid orders remain visible.

## Check your understanding

1. Why does Cara have a count of zero?
2. What goes wrong with `COUNT(*)` on a left join grouped by customer?
3. Where should a paid-order filter go to keep every customer?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL scalar subqueries](https://www.postgresql.org/docs/current/sql-expressions.html#SQL-SYNTAX-SCALAR-SUBQUERIES)
