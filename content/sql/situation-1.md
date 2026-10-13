# Situation-1

## The question

A shop asks: "How many customers have placed at least one order?" One customer may place several orders. Return one number. These are the sample tables:

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customers(customer_id)
);

INSERT INTO customers VALUES (1, 'Ana'), (2, 'Bo'), (3, 'Cal');
INSERT INTO orders VALUES (10, 1), (11, 1), (12, 2);
```

Ana has two orders, Bo has one, and Cal has none. The answer must be two customers.

## Work through it

One output value counts customers, not orders. A join from `customers` to `orders` produces three rows because Ana appears twice. `COUNT(*)` on that join would answer a different question. Count distinct customer IDs from the orders table:

```sql
SELECT COUNT(DISTINCT customer_id) AS customers_with_orders
FROM orders;
```

The query returns `2`. The foreign key makes each order's customer ID refer to a real customer in this data. If that rule did not exist, and the question required current customers only, join to `customers` or check existence there. `COUNT(DISTINCT customer_id)` ignores `NULL` values; here the column is `NOT NULL`.

An alternative is to start with `customers` and use `EXISTS`. It makes the one-row-per-customer rule clear:

```sql
SELECT COUNT(*) AS customers_with_orders
FROM customers AS c
WHERE EXISTS (
  SELECT 1 FROM orders AS o WHERE o.customer_id = c.customer_id
);
```

It also returns `2`. Use either form after checking what the data rules allow. For a list of customer names, the `EXISTS` form can return each customer once without `DISTINCT`.

## Check your understanding

1. What would `COUNT(*)` return after an inner join of these two tables?
2. Would the answer change if Ana placed another order?
3. How would you list the customers who have no orders?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL subquery expressions](https://www.postgresql.org/docs/current/functions-subquery.html)
