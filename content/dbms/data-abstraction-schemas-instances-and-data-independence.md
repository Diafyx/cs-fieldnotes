# Data Abstraction, Schemas, Instances, and Data Independence

Data abstraction means showing each part of a system the details it needs while hiding other details. A person reading a customer list needs names, not the layout of disk pages. A database designer needs table relationships, but usually does not need to choose the physical location of each row.

## Three levels

| Level | Main question | Example |
| --- | --- | --- |
| External | What does this user or application see? | A view with customer IDs and names |
| Conceptual | What data and rules exist? | A customer table with a primary key |
| Internal | How does the DBMS store and find it? | Pages, indexes, and access paths |

These are levels of description, not three copies of the data. A SQL view can represent an external view, though an application screen can also be an external view. In PostgreSQL, an index is one part of the internal design. The DBMS may change its query plan while the table and the answer stay the same.

## Schema and instance

A schema describes the structure and rules. An instance is the data present at a particular moment. If you insert one customer, the instance changes. The table definition does not. People also use "schema" for a PostgreSQL namespace such as `public`; that is a different use of the same word. A namespace groups objects inside one database.

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  full_name text NOT NULL,
  email text NOT NULL
);
INSERT INTO customers VALUES
  (1, 'Ada', 'ada@example.test'),
  (2, 'Lin', 'lin@example.test');

CREATE TEMP VIEW customer_names AS
SELECT customer_id, full_name FROM customers;

CREATE INDEX customers_full_name_idx ON customers(full_name);

SELECT customer_id, full_name
FROM customer_names
ORDER BY customer_id;
```

The view returns `(1, Ada)` and `(2, Lin)`. It leaves out emails. Adding the index does not change those rows. It may change how PostgreSQL finds them on a larger table, but the planner may still choose a table scan for this tiny one. Inserting another customer would change the instance and the view's result without changing either definition.

## What independence means

Physical data independence means internal changes can leave the logical structure and application queries alone. Adding or rebuilding an index is a common example. Logical data independence means a logical design can change while an external contract stays usable. For example, an application could keep querying `customer_names` while the data behind that view is reorganized, if the view is updated to preserve its columns and meaning.

Neither kind is automatic. Renaming `full_name` without updating the view can break it. Changing a column's meaning can break clients even if its name stays the same. Treat views and APIs as contracts and test changes against their users.

## Check your understanding

1. Which abstraction level does adding the index mainly affect, and why do the returned rows stay the same?
2. Why does inserting a customer change the view's result without changing the view definition?
3. What must stay true for an application to keep using a view after the underlying tables change?

## Further reading

- [PostgreSQL schemas as namespaces](https://www.postgresql.org/docs/current/ddl-schemas.html)
- [PostgreSQL CREATE VIEW](https://www.postgresql.org/docs/current/sql-createview.html)
- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
