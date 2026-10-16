# OLTP, OLAP, Warehousing, and Columnar Storage

OLTP systems record day-to-day actions such as placing an order or changing a balance. OLAP systems answer questions across many records, such as sales by month and category. Both may use SQL, but their usual query shapes differ. A data warehouse keeps cleaned, joined, and often historical data for analysis without making every report scan the live transaction database.

## Compare the work

| Question | OLTP pattern | OLAP pattern |
| --- | --- | --- |
| How many rows? | A small number per request. | Many rows per report. |
| What kind of write? | Frequent inserts and updates. | Loads or refreshes from source data. |
| What kind of read? | Find one order or account by key. | Group, join, filter, and aggregate history. |
| What matters most? | Correct transactions and quick user requests. | Correct definitions, broad scans, and useful refresh speed. |

The same database can do some of both, especially at modest scale. A separate warehouse becomes useful when heavy reports compete with live requests, many sources must be combined, or history needs different rules from current operational tables. Moving data adds delay and a second copy to secure and reconcile.

## Start a warehouse with its grain

The **grain** says what one fact row represents. For sales, choose one row per order line, not an unclear mix of orders and lines. A fact row then holds keys to dimensions and numeric measures. A product dimension can hold category and product name. A date or customer dimension can give useful grouping fields. Together they form a simple star schema.

This PostgreSQL example uses one fact row per order line:

```sql
CREATE TEMP TABLE product_dim (
    product_key INTEGER PRIMARY KEY,
    category TEXT NOT NULL
);

CREATE TEMP TABLE sales_fact (
    order_id INTEGER NOT NULL,
    line_no INTEGER NOT NULL,
    product_key INTEGER NOT NULL REFERENCES product_dim(product_key),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    PRIMARY KEY (order_id, line_no)
);

INSERT INTO product_dim VALUES (1, 'Stationery'), (2, 'Home');
INSERT INTO sales_fact VALUES
    (100, 1, 1, 2, 3.00),
    (100, 2, 2, 1, 12.00),
    (101, 1, 1, 1, 3.00);

SELECT p.category,
       SUM(f.quantity * f.unit_price) AS revenue,
       COUNT(DISTINCT f.order_id) AS orders
FROM sales_fact AS f
JOIN product_dim AS p ON p.product_key = f.product_key
GROUP BY p.category
ORDER BY p.category;
```

The result is `(Home, 12.00, 1)` and `(Stationery, 9.00, 2)`. Order 100 has lines in both categories. The per-category order counts add to three, but the warehouse has only two distinct orders. State the grain and measure definition before trusting a dashboard total.

## Load and preserve history

An extract, transform, load process, or **ETL**, reads source data, checks it, and writes warehouse tables. **ELT** loads first and transforms inside the analytical system. A change-data-capture stream can move new changes after an initial load. None of these means the warehouse is instantly current. Track the last loaded source position, failed records, duplicate events, and late arrivals. Make reprocessing the same batch safe.

Decide whether a report should use a product's **current** category or the category **at the time of sale**. If category changes later, a single mutable product row rewrites history in old reports. A versioned dimension, often called a slowly changing dimension, can keep the older category with effective dates and a new key for later sales. Some facts also need a snapshot of price at sale time, as the example stores in `sales_fact`.

## Why columnar storage helps scans

A row-oriented table keeps the fields for one row close together. This suits fetching or updating one complete record. A columnar layout keeps values from the same column together. An analytical query that reads only `category` and `revenue` across millions of rows can avoid reading many unrelated columns. Similar values can also compress well. BigQuery is one example of a system with columnar table storage.

Columnar layout does not make every query faster. Reconstructing many full rows and frequent small updates can have different costs. Indexes, partitioning, caching, and data size also affect a row store. Apache Cassandra's **wide-column** model is not the same as a columnar OLAP file layout. Test the expected queries, load pattern, and freshness target before choosing an engine.

## Try it yourself

1. Why do the example's category order counts add to three when there are only two orders?
2. What does one row in `sales_fact` mean?
3. How would you keep the category that was true on the day of each sale?
4. Why might a report of all past sales belong on a separate analytical copy?

## References

- [Microsoft guidance on star schemas and grain](https://learn.microsoft.com/power-bi/guidance/star-schema)
- [BigQuery columnar storage overview](https://docs.cloud.google.com/bigquery/docs/storage_overview)
- [PostgreSQL numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html)
