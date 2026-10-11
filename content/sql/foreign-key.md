# Foreign Key

A foreign key is a rule about a relationship between tables. It requires a value in one table to match a key or another suitable unique value in another table. This prevents an order from pointing to a customer that does not exist. The database checks the rule even if several different applications write to the same tables.

The table with the foreign key is often called the child or referencing table. The table it points to is the parent or referenced table.

## A customer and an order

```sql
CREATE TABLE customers (
    customer_id bigint PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE orders (
    order_id bigint PRIMARY KEY,
    customer_id bigint NOT NULL REFERENCES customers(customer_id),
    placed_at timestamptz NOT NULL
);
```

An `orders.customer_id` value must match a row in `customers`. `NOT NULL` makes the relationship required. Without `NOT NULL`, a missing customer ID can be stored as `NULL`, and the foreign key check does not require a matching parent for that row.

The rule protects changes in both directions. Inserting an order for a missing customer fails. Deleting a customer who still has orders also fails by default, unless the constraint defines another action or the operation resolves the references within the transaction.

## Decide what deletion means

An `ON DELETE` action is a business choice:

- `NO ACTION` is the default. It stops a delete that would leave a broken reference when the rule is checked.
- `CASCADE` deletes dependent rows with the parent. It can make sense for items that have no life outside their parent.
- `SET NULL` clears the reference. It needs a nullable column and fits an optional relationship.

Do not add `CASCADE` just to make an error go away. Deleting a customer should not silently erase financial orders unless that is truly the intended rule.

## Indexes and performance

The referenced key is indexed when it is a primary key or unique key in PostgreSQL. The referencing column does not receive an index automatically from the foreign key declaration. An index on `orders(customer_id)` often helps joins and checks that run when a customer is changed or deleted. Whether it is worth adding depends on the table and workload.

```sql
CREATE INDEX orders_customer_id_idx ON orders (customer_id);
```

## Check your understanding

1. Why does the example include both `NOT NULL` and `REFERENCES`?
2. When would `ON DELETE SET NULL` make sense? When would it be invalid?
3. Which side of this relationship does PostgreSQL not index automatically for a foreign key?

## Further reading

- [PostgreSQL foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
- [PostgreSQL index overview](https://www.postgresql.org/docs/current/indexes.html)
