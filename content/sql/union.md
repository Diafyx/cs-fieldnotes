# UNION

`UNION` combines the rows from two queries and removes duplicate result rows. It is useful when you want one list of values found in either source.

```sql
WITH current_cities(city) AS (
  VALUES ('Delhi'), ('Pune'), ('Pune')
), past_cities(city) AS (
  VALUES ('Pune'), ('Jaipur')
)
SELECT city FROM current_cities
UNION
SELECT city FROM past_cities
ORDER BY city;
```

The result is `Delhi`, `Jaipur`, and `Pune`, each once. `Pune` occurs twice in the first input and once in the second, but the union result has one `Pune`. `ORDER BY city` makes the shown order reliable.

## What counts as a duplicate?

SQL compares the complete selected row. If one side returns `(7, 'Ana')` and the other returns `(7, 'Anya')`, both stay because the names differ. If you only need unique IDs, select only the ID in both queries. Missing values in the same positions are treated as equal for duplicate removal, so two rows containing only `NULL` become one result row.

The queries need the same number of columns in the same intended order, and corresponding types must be compatible. For example, joining an integer ID column to a text email column by position is not a meaningful union and may fail. Give the columns clear aliases in the first query because those names label the combined result.

## Other set operations

`UNION ALL` keeps repeats. `INTERSECT` keeps rows present in both results. `EXCEPT` keeps rows from the left result that are absent from the right. A `UNION` cannot choose which complete user record is newest when two rows have the same ID but different details. That needs a separate rule for selecting one record per ID.

## Check your understanding

1. How many `Pune` rows does the example return?
2. Would `UNION` remove two rows with the same ID but different names?
3. Where should `ORDER BY` go to sort the full union result?

## Further reading

- [PostgreSQL combining queries](https://www.postgresql.org/docs/current/queries-union.html)
- [PostgreSQL UNION clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-UNION)
