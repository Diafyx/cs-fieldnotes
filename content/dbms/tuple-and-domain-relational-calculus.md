# Tuple and Domain Relational Calculus

Relational calculus describes which values a query should return using logical conditions. Relational algebra describes operations that produce those values. Both are ways to express queries over relations. Calculus is declarative: it says what must be true of a result.

Tuple relational calculus uses variables that stand for whole tuples. Domain relational calculus uses variables that stand for individual attribute values. Their notation differs, but both can describe the same safe queries.

## One question in two forms

Suppose `Customers(customer_id, name)` and `Orders(order_id, customer_id)` are relations. We want customer names for customers with at least one order. Here is readable tuple calculus notation:

```text
{ c.name |
  Customers(c) and
  exists o (Orders(o) and o.customer_id = c.customer_id) }
```

`c` and `o` each stand for a tuple. `exists o` says that at least one matching order must exist. The output is the set of names that pass the condition.

Here is the same question with domain variables:

```text
{ name |
  exists customer_id, order_id (
    Customers(customer_id, name) and
    Orders(order_id, customer_id)
  ) }
```

Each variable here stands for one value. A variable introduced by `exists` is bound inside its condition. The output variable `name` is free, so its values can appear in the result. This notation assumes the attributes are in the order shown in the relation schemas.

SQL expresses the same test with `EXISTS`:

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

SELECT DISTINCT c.name
FROM customers AS c
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id
)
ORDER BY c.name;
```

The result is `Dev` and `Mina`. `DISTINCT` matches the set result of the calculus expression. If two different customers share a name, the expression above returns that name once. To identify customers separately, return both ID and name.

## `NOT`, `FOR ALL`, and safe queries

The logic also has `not`, `and`, `or`, and `for all`. For example, "customers with no orders" means there does not exist an order that matches the customer. In SQL, that is usually `NOT EXISTS`.

A "for all" condition can be written as "there does not exist a counterexample." For example, a customer has bought every required product if no required product lacks a matching purchase. In logic, `for all p (Required(p) implies Bought(customer, p))` says the same thing as `not exists p (Required(p) and not Bought(customer, p))`. This also explains the empty-set case: if there are no required products, every candidate customer meets the condition.

A calculus expression must be **safe**, also called range restricted, to be a practical database query. Its results must come from a finite range tied to the database. An expression asking for every value that is *not* a customer name could otherwise include infinitely many possible strings. Add a finite relation that supplies candidate values before filtering them.

Classical calculus uses two-valued logic and sets. SQL uses `NULL`, three-valued logic, and usually keeps duplicates. In particular, `NOT IN` can give a surprising result if its subquery contains `NULL`; `NOT EXISTS` is usually clearer for an anti-match. These SQL details do not change the logical idea, but they do change the query you write.

## Try it yourself

1. Rewrite the example in tuple calculus to return customer IDs instead of names.
2. State "customers with no orders" using `not exists` in tuple calculus.
3. Why is `{ x | not Customers(x) }` unsafe if `x` can be any possible tuple?

## References

- [MIT Database Systems lecture on query languages](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/8d7652b95f032eab2dcd6320d8a9f1c7_MIT6_830F10_lec02.pdf)
- [PostgreSQL subquery expressions](https://www.postgresql.org/docs/current/functions-subquery.html)
