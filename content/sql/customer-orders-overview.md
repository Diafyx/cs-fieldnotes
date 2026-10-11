# Customer Orders Overview

A customer report should often include people who have placed no orders. Start from customers, left join orders, and count a non-null order key.

## The question

Return every customer with an order count and total order amount. A customer with no orders should have count 0 and total 0. Sort by customer ID.

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  amount numeric(10, 2) NOT NULL
);

INSERT INTO customers VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara');
INSERT INTO orders VALUES (10, 1, 40.00), (11, 1, 60.00), (12, 2, 20.00);
```

## A solution

```sql
SELECT c.customer_id, c.name,
       COUNT(o.order_id) AS order_count,
       COALESCE(SUM(o.amount), 0) AS total_amount
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;
```

The results are Ana with 2 orders and total 100, Ben with 1 and 20, and Cara with 0 and 0. Ana has two joined rows before grouping. Cara has one joined row with `NULL` order columns. `COUNT(o.order_id)` ignores that `NULL`; `COUNT(*)` would incorrectly report one order for Cara. `SUM` of no real amounts is `NULL`, so `COALESCE` shows zero under this report's rule.

If orders can have several line items in another table, joining those lines before counting may multiply each order. Count distinct order IDs or aggregate line items per order first, depending on the question. Decide whether cancelled orders count before adding a status filter.

## Check your understanding

1. Why does Cara need `COUNT(o.order_id)` instead of `COUNT(*)`?
2. Why does Ana have two joined rows before `GROUP BY`?
3. What might happen to the count if each order were joined to several line items?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
