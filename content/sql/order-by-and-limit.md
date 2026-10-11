# ORDER BY and LIMIT

`ORDER BY` asks the database to sort query results. `LIMIT` asks it to return only a certain number of rows. Use them together when you want the "first" or "latest" records. A limit without a clear order has no stable meaning.

## Sort by one or more values

```sql
SELECT order_id, placed_at, amount
FROM orders
ORDER BY placed_at DESC, order_id DESC;
```

`DESC` puts later timestamps first. If two orders share a timestamp, `order_id` breaks the tie. `ASC` puts smaller values first and is the default when no direction is written. You can give each sort expression its own direction.

PostgreSQL lets you specify where `NULL` values go with `NULLS FIRST` or `NULLS LAST`:

```sql
SELECT order_id, shipped_at
FROM orders
ORDER BY shipped_at DESC NULLS LAST, order_id;
```

That is clearer than relying on a database's default placement of missing values, which can differ across products.

## Ask for a small result

```sql
SELECT order_id, placed_at
FROM orders
ORDER BY placed_at DESC, order_id DESC
LIMIT 10;
```

This returns at most ten rows. It does not mean "ten random rows" because the order is specified. If fewer than ten orders exist, it returns fewer than ten.

## Ties and paging

If you sort only by `amount DESC` and several orders have the same amount, their order is not fixed. Adding a unique key gives a stable order. That matters when you show pages of results. `OFFSET` can skip rows, but large offsets may force the database to work through many earlier rows. Changes between page requests can also make offset pages repeat or miss records.

For a growing feed, a cursor based on the last seen sort values is often a better fit:

```sql
SELECT order_id, placed_at
FROM orders
WHERE (placed_at, order_id) < ('2026-01-20 12:00:00+00', 500)
ORDER BY placed_at DESC, order_id DESC
LIMIT 10;
```

This PostgreSQL example assumes the cursor values came from the last row of the previous page. It also assumes `placed_at` and `order_id` are not `NULL`. Pass the cursor values as parameters in application code.

## Check your understanding

1. What happens if `LIMIT 10` is used without `ORDER BY`?
2. Why is `order_id` included after `placed_at` in the sort?
3. What can happen to offset pages when new rows are inserted between requests?

## Further reading

- [PostgreSQL sorting rows](https://www.postgresql.org/docs/current/queries-order.html)
- [PostgreSQL LIMIT and OFFSET](https://www.postgresql.org/docs/current/queries-limit.html)
- [PostgreSQL SELECT reference](https://www.postgresql.org/docs/current/sql-select.html)
