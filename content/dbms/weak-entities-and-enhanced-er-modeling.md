# Weak Entities and Enhanced ER Modeling

A weak entity cannot be identified by its own attributes alone. It needs the key of an owner entity. An order line is a useful example: line 1 can exist in order 100 and also in order 101. Its line number is only a partial key. The full identity is `(order_id, line_no)`.

The line also has total participation in its identifying relationship: every line belongs to one order. The owner may have many lines. "Weak" describes identity, not importance or whether the data is optional.

## See the owner key in the child key

```sql
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY
);
CREATE TEMP TABLE order_lines (
  order_id integer NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
  line_no integer NOT NULL CHECK (line_no > 0),
  description text NOT NULL,
  quantity integer NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (order_id, line_no)
);

INSERT INTO orders VALUES (100), (101);
INSERT INTO order_lines VALUES
  (100, 1, 'Pen', 2),
  (100, 2, 'Notebook', 1),
  (101, 1, 'Pen', 3);

SELECT order_id, line_no, description, quantity
FROM order_lines
ORDER BY order_id, line_no;
```

The result has three lines. Both orders have a line numbered 1, and that is valid because their full keys differ. Two lines numbered 1 in order 100 would be rejected. A line for an order that does not exist would also be rejected. `ON DELETE CASCADE` means deleting an order deletes its lines; use it only if that matches the business rule. Some systems keep orders for audit and forbid deletion instead.

A required foreign key alone does not prove an entity is weak. If a line had its own globally unique `line_id`, its identity would not need the order key, even though the business might still require it to belong to an order.

## Enhanced ER adds subtypes

Enhanced ER, or EER, adds ideas such as superclasses and subclasses. A `Customer` superclass could hold a shared ID and contact address. `PersonalCustomer` could add a birth date. `BusinessCustomer` could add a registration number. Each subtype member is also a customer and keeps the same customer ID. Designing the subtypes from a broad `Customer` is specialization; finding their common fields to form `Customer` is generalization.

Ask two separate questions about the subtype rule:

- **Disjoint or overlapping?** Can one customer be both personal and business?
- **Total or partial?** Must every customer be in at least one subtype?

For a simple shop, the rule might be disjoint and total: every customer is exactly one type. A different system may allow a person to buy for a business, so overlap could be valid. Decide from the real domain. A shared primary key and foreign key can show subtype membership in SQL, but they do not alone enforce disjointness or total coverage. Extra constraints or transaction logic may be needed.

PostgreSQL's `INHERITS` feature is a table mechanism with its own rules. It is not a direct replacement for an EER subtype: primary keys, unique constraints, and foreign keys do not automatically apply across a traditional inheritance hierarchy. A clear table design with shared keys is often easier to reason about.

## Check your understanding

1. Why can two different orders each have `line_no = 1`?
2. Does a non-null foreign key always make the child a weak entity?
3. What two questions must you answer before enforcing customer subtypes?

## Further reading

- [CMU ER model lecture notes](https://www.cs.cmu.edu/~natassa/courses/15-415/S03/notes/2ER6up.pdf)
- [PostgreSQL foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
- [PostgreSQL table inheritance caveats](https://www.postgresql.org/docs/current/ddl-inherit.html)
