# SELECT AND FROM

`FROM` says where rows come from. `SELECT` says what each output row should contain. Start with one table and named columns. Once that feels clear, a source can also be a join, a subquery, or a common table expression.

## Pick columns from a table

```sql
SELECT order_id, customer_id, amount
FROM orders;
```

This returns three columns for every row in `orders`. It does not sort the rows. It does not remove duplicates. To limit rows by a condition, add `WHERE`. To guarantee an order, add `ORDER BY`.

You can compute a value in the output:

```sql
SELECT order_id, amount, amount * 0.10 AS tax_estimate
FROM orders;
```

`AS tax_estimate` gives the computed column a readable name. It does not add a new stored column to `orders`. If the tax rule varies by location or product, this simple formula would be wrong. The point here is how an output expression works.

## Give a source a short name

```sql
SELECT o.order_id, o.amount
FROM orders AS o;
```

The alias `o` helps when a query has several tables with columns such as `id` or `name`. Once you alias a table in PostgreSQL, use the alias for that source in the rest of the query. A short, clear alias is useful. A one-letter alias in a long query can also make the query harder to read.

## When SELECT has no table

PostgreSQL allows a `SELECT` with no `FROM` for expressions:

```sql
SELECT 2 + 3 AS answer;
```

This returns one row with the value 5. It is handy for testing an expression or a function. Do not assume every SQL database supports every form of this syntax in exactly the same way.

## Why SELECT * needs care

`SELECT *` asks for every column. It is convenient while exploring, but a program that relies on the exact order or number of returned columns can break after a schema change. Pulling large text or JSON columns you do not need also costs work. Name the columns in application queries and keep `*` for cases where you truly need all of them.

## Check your understanding

1. Does `AS tax_estimate` store a value in the table?
2. What does the query return if `orders` has no rows?
3. Why might a join need table aliases or qualified column names?

## Further reading

- [PostgreSQL SELECT reference](https://www.postgresql.org/docs/current/sql-select.html)
- [PostgreSQL SELECT lists](https://www.postgresql.org/docs/current/queries-select-lists.html)
- [PostgreSQL FROM clause](https://www.postgresql.org/docs/current/queries-table-expressions.html)
