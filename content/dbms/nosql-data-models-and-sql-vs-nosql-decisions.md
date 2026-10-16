# NoSQL Data Models and SQL-vs-NoSQL Decisions

NoSQL is a loose name for databases whose main data model is not a traditional relational table. It does not mean “no structure,” “no SQL-like query language,” or “no transactions.” Products differ in their keys, queries, indexes, consistency, and transaction rules. Pick from the data and requests your application has, not from the label.

## Four useful models

| Model | Main shape | Good starting question | Example product |
| --- | --- | --- | --- |
| Key-value | A key finds a value or data structure. | Can the request name the key directly? | Redis |
| Document | One record holds nested fields and arrays. | Are related fields read and changed together? | MongoDB |
| Wide-column | Rows are grouped by a partition key, with clustering inside a partition. | Can each important query name a bounded set of partition keys? | Cassandra |
| Graph | Nodes connect through typed relationships. | Are multi-step relationship paths central to the work? | Neo4j |

Redis supports more than plain strings, including hashes, sets, sorted sets, and streams. MongoDB can index fields inside documents and supports transactions across documents when needed. Cassandra's partition key controls placement; a poor key can create a hot or oversized partition. Neo4j stores connections as relationships, but a relational database can also model many graphs with join tables. Test the real queries and size before assuming a special model is necessary.

## Embed or reference?

Imagine this order document. The numbers use cents so the example avoids rounding with binary floating point:

```json
{
  "order_id": 7,
  "customer_id": 42,
  "items": [
    {"sku": "PEN", "quantity": 2, "unit_price_cents": 1000},
    {"sku": "MUG", "quantity": 1, "unit_price_cents": 1200}
  ],
  "total_cents": 3200
}
```

The total is `2 * 1000 + 1 * 1200 = 3200` cents. Embedding these two items lets one document read return the order and its items. In MongoDB, a write to one document is atomic, so changing an item and its stored total can be one document update. The database does not calculate the total correctly for you unless you implement and test that rule. A separate product catalog can still be referenced by `sku` because product details may change independently.

Embedding an unbounded history in one customer document is different. The document grows, every new order touches that large record, and the product has document size limits. Separate order documents may be better. Referencing shared data reduces copies, but a read may need another lookup or a join-like operation, and a change across documents may need a transaction. The choice follows access and update patterns.

## When relational SQL is a good fit

Use a relational database when keys, foreign keys, joins, constraints, and transactions across several rows are central. PostgreSQL can also store flexible JSONB fields, so needing one nested attribute does not require a second database. A document database may fit a record that is naturally read and changed as one unit. A key-value system may fit a cache or a direct-key lookup. A wide-column design may fit predictable large-scale queries by partition key. A graph system may fit frequent traversals through many relationships.

These are starting points, not guarantees of speed. Ask what each query filters on, how many records it touches, how it sorts, and which updates must be atomic. Check whether the product can enforce the required integrity rule and whether its indexes support the query. Also count the work of operating another database: backups, migrations, monitoring, security, and moving data between systems.

## Common mistakes

- A flexible document shape still needs validation and a plan for old document versions.
- Copying a product name into every order can preserve a sale-time snapshot, but a correction may require many updates if those copies were meant to stay current.
- A Cassandra partition key is not the same as a warehouse columnar storage layout. “Wide-column” and “columnar analytics” name different ideas.
- A cache is not automatically a durable source of truth. Check its persistence and eviction settings.
- A relational join is not always slower than a graph traversal. Measure the specific path query.

## Try it yourself

1. If the PEN quantity becomes 3, what total should the document store?
2. Why might all orders for one customer be a poor unbounded array inside one document?
3. Which model would you consider first for a lookup that always has an exact session key?
4. What must you test before moving a PostgreSQL workload to a graph or document database?

## References

- [MongoDB embedded data](https://www.mongodb.com/docs/manual/data-modeling/embedding/)
- [MongoDB embedding and references](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/)
- [Apache Cassandra data modeling](https://cassandra.apache.org/doc/stable/cassandra/developing/data-modeling/intro.html)
- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Neo4j graph concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)
- [PostgreSQL JSON types](https://www.postgresql.org/docs/current/datatype-json.html)
