# Constraints in SQL

A constraint is a rule that the database checks when data changes. It protects a fact that should remain true no matter which Python script, Java service, or SQL tool writes the row. Put stable data rules in the database. The application can still show a friendly error before the database rejects an invalid change.

## The main constraint types

```sql
CREATE TABLE order_items (
    order_id bigint NOT NULL REFERENCES orders(order_id),
    line_no integer NOT NULL,
    sku text NOT NULL,
    quantity integer NOT NULL CHECK (quantity > 0),
    unit_price numeric(10, 2) NOT NULL CHECK (unit_price >= 0),
    PRIMARY KEY (order_id, line_no),
    UNIQUE (order_id, sku)
);
```

`NOT NULL` requires a value. `CHECK` tests a condition on the row. `PRIMARY KEY` gives each item a unique identity within an order. `UNIQUE` says the same SKU may appear at most once in an order. The foreign key requires the order to exist.

The two uniqueness rules answer different questions. `PRIMARY KEY (order_id, line_no)` identifies a line. `UNIQUE (order_id, sku)` prevents two lines for the same product in one order. If the business allows the same SKU on separate lines, remove the second rule.

## A CHECK rule and NULL

A `CHECK` constraint passes when its condition is true or unknown. If `quantity` were nullable, `CHECK (quantity > 0)` alone would still allow `NULL`. That is why the example also uses `NOT NULL`. A rule such as "quantity must be a positive number" needs both parts.

Constraints are checked on changes, but they do not explain every business rule. For example, `unit_price >= 0` cannot tell you whether a discount was approved. Some rules require other tables, time, or a workflow. Keep those checks in an appropriate service or use database mechanisms designed for them.

## Defaults are not constraints

A `DEFAULT` supplies a value when an insert leaves a column out. It does not forbid a client from giving another value. For example, `active boolean DEFAULT true` still allows `false` and, without `NOT NULL`, may allow `NULL`. Add a constraint when the rule is about which values are valid.

## Add rules to existing data

Adding a constraint to a populated table may fail because old rows break the new rule. Find and fix those rows first. In a busy production database, plan the change with the product's locking and validation behavior in mind. A valid rule on a new empty table is not automatically a safe change on a large live table.

## Check your understanding

1. Why does the example use `NOT NULL` as well as `CHECK (quantity > 0)`?
2. What does the primary key allow that the unique SKU rule does not?
3. Why is `DEFAULT true` not the same as `NOT NULL`?

## Further reading

- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL default values](https://www.postgresql.org/docs/current/ddl-default.html)
- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/ddl-alter.html)
