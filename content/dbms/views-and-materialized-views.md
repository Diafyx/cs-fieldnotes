# Views and Materialized Views

A view gives a saved query a name. In PostgreSQL, a regular view does not store its result rows. Its query runs when the view is used, so changes to the base tables appear in later reads. A materialized view stores the result rows. It can make an expensive result faster to read, but its rows get old until you refresh it.

| Feature | Regular view | Materialized view |
| --- | --- | --- |
| Stored result rows | No | Yes |
| Sees later base-table changes | On the next query | After a refresh |
| Can have its own index | No | Yes |
| Main cost | Run the underlying query on reads | Store data and refresh it |

The following PostgreSQL example creates all objects inside a transaction and ends with `ROLLBACK`. Run it in a scratch database. Do not use the object names if they already exist in your schema.

```sql
BEGIN;

CREATE TABLE demo_sales (
    sale_id INTEGER PRIMARY KEY,
    amount INTEGER NOT NULL
);

INSERT INTO demo_sales VALUES (1, 10), (2, 20);

CREATE VIEW demo_sales_total AS
SELECT SUM(amount) AS total FROM demo_sales;

CREATE MATERIALIZED VIEW demo_sales_total_saved AS
SELECT SUM(amount) AS total FROM demo_sales;

INSERT INTO demo_sales VALUES (3, 5);

SELECT total FROM demo_sales_total;
SELECT total FROM demo_sales_total_saved;

REFRESH MATERIALIZED VIEW demo_sales_total_saved;
SELECT total FROM demo_sales_total_saved;

ROLLBACK;
```

The first `SELECT` gives `35`. The second gives the old total, `30`. After the refresh, the third gives `35`. `ROLLBACK` removes the tables and views created by this transaction.

## Choosing and maintaining a view

Use a regular view when you want a reusable query and current data. Use a materialized view when repeated reads justify stored results and you can choose when to refresh. A refresh in PostgreSQL replaces its stored contents by rerunning the defining query. Without `CONCURRENTLY`, a refresh can block readers. `REFRESH MATERIALIZED VIEW CONCURRENTLY` lets reads continue, but needs a populated materialized view and a qualifying unique index that covers all rows. Only one refresh of a given materialized view can run at a time.

Indexes can help reads of a materialized view, but they take space and add work to refreshes. A regular view uses the underlying tables and their indexes. Check the actual query plan before adding an index.

Some simple PostgreSQL views can be updated through `INSERT`, `UPDATE`, or `DELETE`. Views with grouping, aggregates, or joins are generally read-only by default. A view used to restrict access needs careful permissions. PostgreSQL normally checks access to base tables as the view owner; `security_invoker` changes that behavior. A view name by itself is not a complete security policy.

## Try it yourself

1. What would each view return after another sale is inserted but before the next refresh?
2. Why might a report accept a materialized view that is one hour old?
3. What must be true before using `REFRESH MATERIALIZED VIEW CONCURRENTLY`?

## References

- [PostgreSQL CREATE VIEW](https://www.postgresql.org/docs/current/sql-createview.html)
- [PostgreSQL CREATE MATERIALIZED VIEW](https://www.postgresql.org/docs/current/sql-creatematerializedview.html)
- [PostgreSQL REFRESH MATERIALIZED VIEW](https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html)
