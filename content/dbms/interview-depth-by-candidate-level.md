# Interview Depth by Candidate Level

An interview question often begins with a definition and then asks what happens in a real case. You can prepare by building an answer in layers: state the rule, show a small example, name the edge case, and explain the choice you would make. The levels below are study targets, not rules used by every employer.

## What to practice at each level

| Level | A useful target | Example follow-up |
| --- | --- | --- |
| Student or first role | Read a schema and write correct SQL with keys, joins, grouping, and `NULL`. | Why did this left join lose customers with no orders? |
| Developer with project work | Explain constraints, indexes, transactions, and a query plan in an application you built. | What prevents two buyers from taking the last item? |
| Developer owning a service | Diagnose slow queries, failed transactions, migrations, and recovery plans. | What would you measure before adding an index? |
| Designer of a larger system | State consistency and failure promises across replicas or services. | What happens after a payment succeeds but the reply is lost? |

Do not memorize one answer for each job title. A small company may ask deep SQL questions in a first-role interview. A senior interview may still test basic `NULL` rules. Use the table to widen your practice, not to skip fundamentals.

## Follow one question to its real edge cases

**Question: What is an index?** A basic answer is that it is an extra structure that helps find rows without scanning every row. A stronger answer says which columns and query shape benefit. For `WHERE customer_id = 42 ORDER BY order_id`, a B-tree index on `(customer_id, order_id)` can both narrow the search and provide order. It also uses space and slows writes that change indexed values. On a tiny table or a query that reads most rows, a sequential scan can be better. Check `EXPLAIN (ANALYZE, BUFFERS)` on representative data before claiming a speedup.

**Question: Does a transaction stop overselling?** A transaction keeps its own writes together, but the isolation level and update rule matter. For a stock row, a conditional update such as `UPDATE stock SET units = units - 1 WHERE product_id = 10 AND units > 0` can make one buyer claim the last unit. Check whether one row was updated before promising the sale, and keep the order write in the same local transaction if both tables share a database. If stock and payment live in different systems, plan idempotent requests and recovery for uncertain outcomes.

**Question: Can a replica always serve reads?** A replica can answer reads only within the freshness rule the feature accepts. An asynchronous replica may lag after a confirmed primary write. A user may then save an order and briefly fail to see it on a replica. For read-your-writes, route that user's next read to a source that has reached the write's position, or use a primary read when appropriate. Say how failover affects acknowledged writes instead of saying only that there are two copies.

## Show your reasoning on a board or in a document

For a schema question, start with entities and keys, then draw the relationship and state who owns each foreign key. Give one row example and try a missing or duplicate value. For a SQL question, write the small input tables and expected output before typing the query. Check duplicates, `NULL`, ties, and whether a left join stays a left join after the `WHERE` clause.

For a performance question, ask for table size, data distribution, indexes, and the slow query plan. Distinguish estimated rows from actual rows. For a concurrency question, write two sessions in time order. Name what each session can see and when it commits. For a failure question, separate a confirmed result, a timeout with an unknown result, and a known rollback.

If you have not used a feature, say so plainly and work from the rule you do know. For example, explain what a B+ tree page search does, then say you would verify the database's exact leaf and fill rules before predicting its size. A clear assumption is better than a confident guess.

## Try it yourself

1. A query gets slower after a table grows. What measurements would you ask for before creating an index?
2. How would you explain a left join that returns fewer customers than expected?
3. A checkout request times out. What must the retry know before it sends another payment request?
4. Give a two-session example in which each transaction looks safe alone but their combined result breaks a rule.

## References

- [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
