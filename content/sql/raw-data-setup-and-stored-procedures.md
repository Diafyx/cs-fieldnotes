# Raw Data Setup and Stored Procedures

A performance test needs repeatable data. A few hand-written rows are good for checking an answer, but they may be too small to show a useful plan. PostgreSQL's `generate_series` can make a larger test table. A stored procedure can then perform a named operation on that data. Putting SQL in a procedure does not make it fast by itself.

## Make repeatable test data

Run this in a scratch PostgreSQL database:

```sql
CREATE SCHEMA perf_lab;

CREATE TABLE perf_lab.orders (
  order_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  placed_on date NOT NULL,
  status text NOT NULL CHECK (status IN ('pending', 'paid')),
  amount numeric(10, 2) NOT NULL CHECK (amount >= 0)
);

INSERT INTO perf_lab.orders (order_id, customer_id, placed_on, status, amount)
SELECT g, (g % 100) + 1, DATE '2026-01-01' + (g % 90),
       CASE WHEN g % 3 = 0 THEN 'paid' ELSE 'pending' END,
       10.00
FROM generate_series(1, 10000) AS series(g);

ANALYZE perf_lab.orders;

SELECT COUNT(*) AS orders, COUNT(*) FILTER (WHERE status = 'pending') AS pending
FROM perf_lab.orders;
```

The final query returns `10000` orders and `6667` pending orders. Every customer ID from 1 to 100 appears 100 times. The dates cover 90 days. This pattern is easy to recreate, but real data can have uneven customer sizes and hot dates. When a production plan is the question, test with a safe copy that has similar sizes and distributions. `ANALYZE` collects statistics used by the planner.

## Put one write rule in a procedure

Run this after the setup above:

```sql
CREATE PROCEDURE perf_lab.mark_paid(p_order_id integer)
LANGUAGE plpgsql
AS $$
DECLARE
  changed bigint;
BEGIN
  UPDATE perf_lab.orders
  SET status = 'paid'
  WHERE order_id = p_order_id AND status = 'pending';

  GET DIAGNOSTICS changed = ROW_COUNT;
  IF changed <> 1 THEN
    RAISE EXCEPTION 'No pending order with id %', p_order_id;
  END IF;
END;
$$;

CALL perf_lab.mark_paid(2);

SELECT order_id, status
FROM perf_lab.orders
WHERE order_id = 2;
```

The final query returns `(2, paid)`. `CALL` runs the procedure. `ROW_COUNT` reports how many rows the update changed. Calling it again for order 2 raises an error because that order is no longer pending. The procedure relies on the table's primary key and status rule; it does not replace them.

Use a procedure when a named database-side operation is helpful. A normal parameterized `UPDATE` may be simpler for a one-statement change. Stored procedures can also group several steps, but they still need clear transaction, error, and permission rules. To study a slow call, measure the SQL inside it and the number of times it runs. Do not infer performance from the fact that the work is inside the database.

## Check your understanding

1. Why is this generated data better for a plan test than four rows?
2. What happens when `mark_paid(2)` runs a second time?
3. Why must the table still have a primary key and a status check?

## Further reading

- [PostgreSQL generate_series](https://www.postgresql.org/docs/current/functions-srf.html)
- [PostgreSQL CREATE PROCEDURE](https://www.postgresql.org/docs/current/sql-createprocedure.html)
- [PostgreSQL PL/pgSQL result status](https://www.postgresql.org/docs/current/plpgsql-statements.html)
- [PostgreSQL ANALYZE](https://www.postgresql.org/docs/current/sql-analyze.html)
