# ER/EER-to-Relational Mapping

An ER or EER model states what things, relationships, and rules exist. Relational mapping turns that model into tables, keys, foreign keys, and checks. The aim is to keep the meaning of the model. Drawing a relationship line does not automatically create the right SQL constraint.

## A short mapping guide

| Concept in the model | Common table design |
| --- | --- |
| Strong entity | One table with a primary key and its simple attributes |
| Composite attribute | Separate useful parts into columns, such as city and postal code |
| Multivalued attribute | Separate table with owner key and one value per row |
| Derived attribute | Compute from stored facts when possible |
| One-to-many relationship | Foreign key on the many side; use `NOT NULL` if required |
| One-to-one relationship | Foreign key with `UNIQUE`; decide which side may be absent |
| Many-to-many relationship | Linking table with both foreign keys and any relationship attributes |
| Weak entity | Owner key plus partial key form its primary key |
| Subtype | Choose a mapping that preserves shared identity and subtype rules |

This is a guide, not a rule to make one table for every box and diamond. The key of a linking table depends on the business rule. If a product may appear only once per order, `(order_id, product_id)` can identify the link. If the same product may appear on several separate lines, use `(order_id, line_no)` instead.

## Map a small shop

The model has customers, products, and orders. A customer can have several phone numbers and orders. Each order has lines. A line belongs to one order and names one product. Its quantity is a fact about that line.

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  display_name text NOT NULL
);
CREATE TEMP TABLE customer_phones (
  customer_id integer NOT NULL REFERENCES customers(customer_id),
  phone text NOT NULL,
  PRIMARY KEY (customer_id, phone)
);
CREATE TEMP TABLE products (
  product_id integer PRIMARY KEY,
  product_name text NOT NULL
);
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customers(customer_id)
);
CREATE TEMP TABLE order_lines (
  order_id integer NOT NULL REFERENCES orders(order_id),
  line_no integer NOT NULL CHECK (line_no > 0),
  product_id integer NOT NULL REFERENCES products(product_id),
  quantity integer NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (order_id, line_no)
);

INSERT INTO customers VALUES (1, 'Ada');
INSERT INTO customer_phones VALUES (1, '+12025550101');
INSERT INTO products VALUES (10, 'Pen'), (11, 'Notebook');
INSERT INTO orders VALUES (100, 1);
INSERT INTO order_lines VALUES (100, 1, 10, 2), (100, 2, 11, 1);

SELECT c.display_name, o.order_id, l.line_no,
       p.product_name, l.quantity
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
JOIN order_lines AS l ON l.order_id = o.order_id
JOIN products AS p ON p.product_id = l.product_id
ORDER BY o.order_id, l.line_no;
```

The result is `(Ada, 100, 1, Pen, 2)` and `(Ada, 100, 2, Notebook, 1)`. The phone table is not joined because a customer with two phones would repeat each order line. Join only the facts the question needs. The foreign keys check that every stored line points to an existing order and product. They do not require every order to have at least one line; enforce that as part of creating or completing an order if the business requires it.

## Map subtype rules carefully

For EER, one choice is a base `customers` table plus `personal_customers` and `business_customers` tables. Each subtype table uses `customer_id` as both its primary key and a foreign key to `customers`. This keeps one shared identity and puts subtype-only facts in the right place. It does not by itself guarantee that every customer has a subtype or that a customer appears in only one subtype. Another choice is one customer table with a type column and checks on subtype fields. Choose the form that can express the actual disjointness and participation rules without leaving invalid states.

A relationship among three entity sets needs one table with all three foreign keys when the complete triple is the fact. Three independent pair tables may allow combinations that never happened. Choose a primary key based on which combinations can repeat.

Before calling a mapping complete, test missing parents, duplicate weak keys, optional relationships, deletion behavior, and subtype membership. Some conceptual minimum participation rules need a transaction or more database logic because a single foreign key only checks the row that carries it.

## Check your understanding

1. Why is `order_id` part of the primary key in `order_lines`?
2. Why does the sample query avoid joining `customer_phones`?
3. Which EER subtype rules are not enforced by a subtype table's foreign key alone?

## Further reading

- [MIT database lecture on ER to relational mapping](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/a9c47ed7d80c1bfc51d0baf7ac545398_MIT6_830F10_lec03.pdf)
- [PostgreSQL table constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
