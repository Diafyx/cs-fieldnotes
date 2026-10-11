# Table Join Operation

A join must use the columns that identify the same thing in both tables. When order numbers restart in every store, `order_id` alone is not enough. Use the store ID and order ID together.

## The question

Return each order that has a matching payment, with the customer and payment status. Sort by store ID and order ID.

```sql
CREATE TEMP TABLE store_orders (
  store_id integer NOT NULL,
  order_id integer NOT NULL,
  customer_name text NOT NULL,
  PRIMARY KEY (store_id, order_id)
);
CREATE TEMP TABLE payments (
  store_id integer NOT NULL,
  order_id integer NOT NULL,
  status text NOT NULL,
  PRIMARY KEY (store_id, order_id)
);

INSERT INTO store_orders VALUES
  (1, 1, 'Ana'), (2, 1, 'Ben'), (1, 2, 'Cara');
INSERT INTO payments VALUES
  (1, 1, 'paid'), (2, 1, 'pending');
```

## A solution

```sql
SELECT o.store_id, o.order_id, o.customer_name, p.status
FROM store_orders AS o
JOIN payments AS p
  ON p.store_id = o.store_id AND p.order_id = o.order_id
ORDER BY o.store_id, o.order_id;
```

The result is Ana's order `(1, 1)` with `paid`, then Ben's order `(2, 1)` with `pending`. Cara's order has no payment and is absent from this inner join. If the query joined only on `order_id`, both order 1 rows would match both payment 1 rows and produce four incorrect pairs.

The composite primary keys make each full `(store_id, order_id)` pair unique on each side. If a payment can have several attempts, this one-row payment table would need a different design and a rule for which attempt to show.

## Check your understanding

1. Why is joining only on `order_id` wrong here?
2. Why is Cara absent?
3. What would change if a single order could have several payment attempts?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL multicolumn primary keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS)
