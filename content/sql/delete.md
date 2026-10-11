# DELETE

`DELETE` removes rows that meet a `WHERE` condition. The table and its columns stay in place. Without `WHERE`, every row in that table is a candidate for deletion.

## Remove selected rows

```sql
DELETE FROM orders
WHERE order_id = 42
RETURNING order_id, customer_id;
```

If order 42 exists, PostgreSQL removes it and returns its ID and customer ID. If it does not exist, zero rows are returned. A primary key on `order_id` makes the condition match at most one row.

To remove completed orders before a date, write the full condition and review matching rows first:

```sql
SELECT order_id, status, completed_at
FROM orders
WHERE status = 'completed'
  AND completed_at < DATE '2025-01-01';
```

After checking that list, use the same condition in `DELETE`. A preview is useful, but concurrent writes can change what matches before the delete runs. Use a transaction and inspect `RETURNING` when the exact affected rows matter.

## Related rows and transactions

A foreign key may stop a delete while other rows still refer to it. If the foreign key uses `ON DELETE CASCADE`, deleting a parent can remove child rows too. Read the relationship rule before deleting a parent. `RETURNING` on the parent delete shows parent rows, so it is not a complete list of child rows removed by cascading.

```sql
BEGIN;

DELETE FROM orders
WHERE order_id = 42
RETURNING order_id;

ROLLBACK;
```

This is a trial delete in PostgreSQL. `ROLLBACK` restores the row if the transaction has not been committed. For a real delete, use `COMMIT` after checking the result. PostgreSQL has no direct `DELETE ... LIMIT` clause; select a batch of keys first if you need a limited batch. Do not rely on an unspecified row order.

`DELETE` can use another table through a subquery or PostgreSQL's `USING` clause. It removes rows from the named target table, not every table named in the condition.

## Check your understanding

1. What remains after every row in a table is deleted?
2. Why might deleting one customer affect rows in another table?
3. What does a zero-row `RETURNING` result tell you?

## Further reading

- [PostgreSQL DELETE](https://www.postgresql.org/docs/current/sql-delete.html)
- [PostgreSQL foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
