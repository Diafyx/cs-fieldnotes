# Entities, Entity Sets, and Attributes

An entity is one thing the system needs to remember, such as customer 1 or order 100. An entity set is the collection of things of that kind, such as all customers. An attribute is a fact about an entity, such as a customer's name. An ER model starts with these meanings before choosing tables and columns.

## Decide what needs its own identity

A customer can place many orders, and each order has its own date and state. `Customer` and `Order` are useful entity sets. Putting all order numbers in one customer text field would make it hard to find, change, and protect one order. A customer's display name is an attribute because it describes the customer; it does not usually need an independent identity.

Each entity needs a way to distinguish it from others. `customer_id` can be a stable key. An email address may look unique, but people can change addresses and a business may share one address. Do not declare it a key until the business rule supports that choice. A key is a rule about identity, not just a column that happens to be unique in today's data.

## Kinds of attributes

| Kind | Example | Modeling question |
| --- | --- | --- |
| Simple | `birth_date` | Is one value enough? |
| Composite | An address with street, city, and postal code | Which parts must be searched or changed separately? |
| Multivalued | A customer with two phone numbers | Should each value be a separate row? |
| Derived | Age calculated from birth date and a chosen date | Can it be calculated instead of stored? |
| Optional | A birth date that a customer did not provide | What does a missing value mean? |

The type and allowed values of an attribute are its domain. A phone number is usually text, because leading zeros and `+` matter and arithmetic does not. A quantity may be an integer with a rule that it must be positive. The model should say these rules before code is written.

## A small relational form

This PostgreSQL example gives a customer one row and each phone number its own row:

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  display_name text NOT NULL,
  birth_date date
);
CREATE TEMP TABLE customer_phones (
  customer_id integer NOT NULL REFERENCES customers(customer_id),
  phone text NOT NULL,
  PRIMARY KEY (customer_id, phone)
);

INSERT INTO customers VALUES
  (1, 'Ada', NULL),
  (2, 'Lin', '1998-04-12');
INSERT INTO customer_phones VALUES
  (1, '+12025550101'),
  (1, '+12025550102');

SELECT c.customer_id, c.display_name,
       COUNT(p.phone) AS phone_count
FROM customers AS c
LEFT JOIN customer_phones AS p ON p.customer_id = c.customer_id
GROUP BY c.customer_id, c.display_name
ORDER BY c.customer_id;
```

The result is `(1, Ada, 2)` and `(2, Lin, 0)`. `COUNT(p.phone)` gives Lin zero because the left join has no matching phone; `COUNT(*)` would count the placeholder row and give one. Ada's missing birth date is `NULL`, not a claim that Ada has no birth date. Age is not stored because it changes as time passes.

An attribute can become an entity when it gains its own facts or relationships. If a phone number needs verification history and a separate owner record, a `Phone` entity may be useful. Choose based on the rules the application must keep, not on the length of the value.

## Check your understanding

1. Why is `customer_id` a safer key than `display_name`?
2. Why does the example use a second table for phone numbers?
3. What information would make an address more than one simple text attribute?

## Further reading

- [CMU ER model lecture notes](https://www.cs.cmu.edu/~natassa/courses/15-415/S03/notes/2ER6up.pdf)
- [PostgreSQL primary and foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html)
