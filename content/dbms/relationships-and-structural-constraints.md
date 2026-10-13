# Relationships and Structural Constraints

A relationship says how entities are connected. A customer places an order. A product appears on an order line. A structural constraint says how many connections are allowed or required. Write those rules in words before drawing symbols, because ER diagram styles use different marks for the same idea.

## Count from both sides

In this shop, a customer may place zero or many orders. Every order must belong to exactly one customer. In minimum and maximum form, that is `Customer: 0..many` and `Order: 1..1` for the placing relationship. The zero means customer participation is optional. The one on the order side means order participation is required, or total.

This PostgreSQL example stores the customer key on the many side:

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  display_name text NOT NULL
);
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customers(customer_id)
);

INSERT INTO customers VALUES (1, 'Ada'), (2, 'Lin');
INSERT INTO orders VALUES (100, 1), (101, 1);

SELECT c.customer_id, c.display_name,
       COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.display_name
ORDER BY c.customer_id;
```

The result is `(1, Ada, 2)` and `(2, Lin, 0)`. The foreign key rejects an order with no existing customer, and `NOT NULL` rejects an order without a customer ID. These rules do not require every customer to have an order. That is why Lin can appear with zero. Deleting a customer who still has orders is rejected by the default foreign key action; a different delete policy needs an explicit business decision.

## Common relationship shapes

| Shape | Example | Usual relational form |
| --- | --- | --- |
| One to one | Customer and an optional profile | A foreign key with `UNIQUE`; add `NOT NULL` only if that side is required |
| One to many | Customer and orders | Foreign key in `orders` |
| Many to many | Orders and products | A linking table with both foreign keys |

The linking table can hold facts about the connection. An order line's quantity belongs to the order and product together, not to every order or every product. If the same product may appear in several separate lines of one order, a line number can identify each line. The business rule decides whether `(order_id, product_id)` must be unique.

Relationships can also be recursive, such as an employee reporting to another employee. A ternary relationship connects three entity sets at once, such as a supplier delivering a product to a warehouse. Replacing every ternary relationship with three unrelated pairs can lose which supplier delivered which product to which warehouse. Model the full fact when all three parts matter.

## Limits of simple constraints

A foreign key and `NOT NULL` can enforce that every order has a customer. They cannot by themselves enforce that every customer has at least one order, since a new customer may exist before the first order. Some minimum participation rules need application workflow, a transaction, or additional database logic. State the rule even when one table definition cannot enforce it alone.

## Check your understanding

1. Which constraint stops an order from referring to customer 99 when no such customer exists?
2. Why does `COUNT(o.order_id)` return zero for Lin while `COUNT(*)` would not?
3. When would an order-product link need a line number as well as two foreign keys?

## Further reading

- [CMU ER model lecture notes](https://www.cs.cmu.edu/~natassa/courses/15-415/S03/notes/2ER6up.pdf)
- [PostgreSQL foreign key constraints](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
