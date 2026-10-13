# Data Models and Database Families

A data model describes how facts and relationships are represented. A database family is a broad group of systems built around a common model or workload. The family name is a starting point, not a full description of a product. One DBMS can support more than one shape of data, and two systems in the same family can have different transaction and scaling rules.

## One example in a relational model

A customer can have many orders. In a relational model, separate tables can keep customer details in one place while orders refer to the customer key.

```sql
CREATE TEMP TABLE customers (
  customer_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customers(customer_id),
  total numeric(10, 2) NOT NULL
);

INSERT INTO customers VALUES (1, 'Ada');
INSERT INTO orders VALUES (10, 1, 25.00), (11, 1, 40.00);

SELECT c.name, o.order_id, o.total
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
ORDER BY o.order_id;
```

The result has Ada's orders 10 and 11. The foreign key rejects an order for a customer ID that does not exist. The join does not copy Ada's name into every order row.

## Other useful shapes

| Family or layout | Basic shape | A question it handles well | Design point to check |
| --- | --- | --- | --- |
| Relational | Tables, keys, and relationships | Which orders belong to a customer? | Joins, constraints, and transactions |
| Document | Documents with fields and nested values | Show one item with its bounded details | Whether nested data grows or changes separately |
| Key-value and data structures | A key finds a value or structure | Read a cached session by ID | Expiry, durability, and how other lookups work |
| Graph | Nodes connected by named relationships | Follow several connection steps | Which traversals are common and how data is updated |
| Wide-column | Rows grouped by a partition key and ordered within a partition | Fetch a known customer's time-ordered records | Partition size and which queries the key supports |
| Time-series | Measurements ordered by time | Read a sensor's last hour of values | Retention, time windows, and late data |
| Analytical column storage | Values stored by column for large scans | Sum one measure across many rows | Write pattern and reporting freshness |

A document could hold Ada and a small list of recent orders together. If the order list grows without limit or orders need independent changes, references may be easier. A graph could represent customers and orders as connected nodes, but a graph DBMS is not required just because data has relationships. A relational database can also store JSON and graph-like edges. Redis is often used for key-based access and offers more than plain string values. Wide-column systems such as Cassandra group rows by partition key; they are not the same as columnar analytics systems. Time-series features can also be built on a relational database. Column storage describes a physical layout for analytical queries; it is not the opposite of the relational model. Some columnar systems also use SQL and tables.

"NoSQL" covers several different families. It does not mean "no queries" or one shared consistency guarantee. Choose from the operations the application actually needs: lookups, joins, traversals, updates, reports, transaction boundaries, and recovery. Decide which store owns each fact before copying data to a cache or analytics system.

## Check your understanding

1. Why might one huge customer document be awkward when orders grow forever?
2. Can a relational database store graph edges or JSON values?
3. Why does knowing that a product is "NoSQL" tell you too little about its transactions?

## Further reading

- [PostgreSQL table constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [MongoDB document relationships](https://www.mongodb.com/docs/manual/applications/data-models-relationships/)
- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Neo4j graph concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)
- [Apache Cassandra data modeling](https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/data-modeling_logical.html)
- [Timescale hypertables](https://docs.timescale.com/use-timescale/latest/hypertables/)
- [ClickHouse columnar database overview](https://clickhouse.com/resources/engineering/what-is-columnar-database)
