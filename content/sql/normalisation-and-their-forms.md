# Normalisation and their Forms

Normalisation asks whether each fact is stored in a place where its key determines it. It helps prevent conflicting copies and the insert, update, and delete problems that come from them. The normal forms are tests for different kinds of unwanted dependency. Start by writing the real business rules; the shape of a small sample is not enough to prove them.

## Find the dependencies

Imagine one table with this shape:

```text
order_lines(order_id, product_id, customer_id, customer_name,
            product_name, quantity)
key: (order_id, product_id)

order_id -> customer_id
customer_id -> customer_name
product_id -> product_name
(order_id, product_id) -> quantity
```

The arrow means that one value determines one fact. If product 100 always has the current name `Lamp`, then `product_id -> product_name`. In the large table, the name repeats on every order that contains that product. A rename must change many rows.

## First, second, and third normal form

**First normal form (1NF)** keeps one value of the chosen column domain in each field, with no repeated columns such as `phone_1`, `phone_2`, and `phone_3`. Put a variable number of phone numbers in a related table when each number needs its own row, search, or constraint. "Atomic" depends on what the application needs to do with a value; a date can be one useful value even though it has parts. A JSON value is not automatically a design error, but hiding independently managed facts inside it can cause the same problems.

**Second normal form (2NF)** requires 1NF and stops a non-key attribute from depending on only part of a candidate key. In `order_lines`, the key is `(order_id, product_id)`, but `product_name` depends only on `product_id`. `customer_id` depends only on `order_id`. Move facts about a product to `products` and facts about an order to `orders`. If a table's only candidate key has one column, a partial dependency on that key cannot occur.

**Third normal form (3NF)** removes the usual non-key to non-key chain. In an `orders(order_id, customer_id, customer_name)` table, `order_id` determines `customer_id`, which determines the current `customer_name`. Put current customer names in `customers`. More exactly, for each nontrivial functional dependency `X -> A`, 3NF requires `X` to be a superkey or `A` to be a prime attribute, meaning part of some candidate key. The simple "non-key depends on non-key" phrase is a useful warning, not the full definition.

## A practical split

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  customer_name text NOT NULL
);

CREATE TEMP TABLE products (
  product_id integer PRIMARY KEY,
  product_name text NOT NULL
);

CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customers(customer_id)
);

CREATE TEMP TABLE order_items (
  order_id integer NOT NULL REFERENCES orders(order_id),
  product_id integer NOT NULL REFERENCES products(product_id),
  quantity integer NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (order_id, product_id)
);

INSERT INTO customers VALUES (1, 'Ada');
INSERT INTO products VALUES (100, 'Lamp'), (101, 'Mug');
INSERT INTO orders VALUES (10, 1);
INSERT INTO order_items VALUES (10, 100, 2), (10, 101, 1);

SELECT o.order_id, c.customer_name, p.product_name, i.quantity
FROM order_items AS i
JOIN orders AS o ON o.order_id = i.order_id
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN products AS p ON p.product_id = i.product_id
ORDER BY i.product_id;
```

The report returns `(10, Ada, Lamp, 2)` and `(10, Ada, Mug, 1)`. Each current name has one stored owner. Joins rebuild the flat view when it is needed.

## BCNF and later forms

**Boyce-Codd normal form (BCNF)** is stricter than 3NF: every determinant of a nontrivial functional dependency must be a superkey. Consider `teaching(student, course, instructor)` with rules `(student, course) -> instructor` and `instructor -> course`. The candidate keys are `(student, course)` and `(student, instructor)`. `instructor -> course` is allowed by 3NF because `course` is part of a candidate key, but it fails BCNF because `instructor` alone does not identify a teaching row. Splitting into instructor courses and student instructors removes that repetition. It can make the rule "one instructor per student and course" harder to enforce, so check which dependencies a split preserves.

**Fourth normal form (4NF)** addresses independent multi-valued facts. If Ada has two skills and two spoken languages, storing every skill and language combination repeats both lists. Separate `person_skills` and `person_languages` when there is no business link between a particular skill and language. If a pairing itself has meaning, keep the pairing instead. Formally, a nontrivial multi-valued dependency needs a superkey determinant.

**Fifth normal form (5NF)** addresses a relation that can be rebuilt from several smaller projections without adding false combinations. A supplier, part, and project table can be split into pair tables only if the business rule says the pair facts fully determine every valid triple. Otherwise the join may invent a triple that was never allowed. This form is rare in day-to-day design, but the warning about false join results matters. Sixth normal form studies further irreducible joins and is mainly useful in some temporal designs.

Always check that a split is **lossless**: joining the new tables must recover exactly the allowed original rows. Also ask whether important rules can still be enforced directly. Sometimes a measured reporting need justifies a stored copy or summary. Name the source of truth, keep the copy in sync, and test the update path. Normalisation guides the logical design; it is not a promise that every query will be fast.

## Check your understanding

1. Which dependencies in `order_lines` use only part of its composite key?
2. Why is `customer_name` better kept in `customers` than in every order?
3. What new problem can appear if a split loses a business rule or invents rows when joined?
4. When should skill and language pairings stay together?

## Further reading

- [Codd's further normalisation paper](https://thaumatorium.com/articles/the-papers-of-ef-the-coddfather-codd/1971b-further-normalization-of-the-data-base-relational-model/)
- [Codd's relational model paper](https://doi.org/10.1145/362384.362685)
- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
