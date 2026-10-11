# UNION ALL

`UNION ALL` puts one query's rows together with another query's rows and keeps every occurrence. If the same value appears three times across the inputs, it appears three times in the result.

```sql
WITH store_a(item) AS (
  VALUES ('pen'), ('pen')
), store_b(item) AS (
  VALUES ('pen'), ('book')
)
SELECT item FROM store_a
UNION ALL
SELECT item FROM store_b
ORDER BY item;
```

The result has one `book` and three `pen` rows. This matters when each row represents a separate sale or event. Replacing `UNION ALL` with `UNION` would leave only one `pen` and lose the fact that three records were present.

## Keep source identity when needed

Two sources may both have a row numbered 5. If those are different records, add a source label:

```sql
SELECT 'store_a' AS source, sale_id, amount FROM store_a_sales
UNION ALL
SELECT 'store_b' AS source, sale_id, amount FROM store_b_sales;
```

The label makes the combined key `(source, sale_id)` clear. The column names and types still need to line up by position. Use a final `ORDER BY` if order matters; `UNION ALL` does not promise that rows from the first query appear first.

`UNION ALL` skips duplicate removal, so it often does less work than `UNION`. Choose it because repeated rows have meaning, not only for speed. If a duplicate came from an import error, keeping it would double-count an amount. Decide what a row represents before aggregating the combined data.

## Check your understanding

1. How many `pen` rows does the first query return?
2. Why can sale ID 5 from two stores represent two different sales?
3. What can go wrong if an accidental duplicate is counted as another sale?

## Further reading

- [PostgreSQL combining queries](https://www.postgresql.org/docs/current/queries-union.html)
- [PostgreSQL UNION clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-UNION)
