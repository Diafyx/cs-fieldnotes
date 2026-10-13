# JSON Output Builders

SQL can build JSON for an API or report. Build each object from typed columns, then gather related rows into an array. State the array order in the aggregate if clients depend on it.

## One customer with an array of orders

```sql
WITH customers(customer_id, name) AS (
  VALUES (1, 'Ada'), (2, 'Ben')
), orders(order_id, customer_id, total) AS (
  VALUES (10, 1, 25), (11, 1, 12)
)
SELECT jsonb_build_object(
         'customer_id', c.customer_id,
         'name', c.name,
         'orders', COALESCE(
           jsonb_agg(
             jsonb_build_object('order_id', o.order_id, 'total', o.total)
             ORDER BY o.order_id
           ) FILTER (WHERE o.order_id IS NOT NULL),
           '[]'::jsonb
         )
       ) AS customer_json
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;
```

Ada's object has orders 10 and 11 in that order. Ben's object has an empty `orders` array. The left join keeps Ben. Without the `FILTER`, its unmatched row would produce an order object with null fields. `COALESCE` turns the missing aggregate result into `[]`.

`jsonb_build_object` takes alternating key and value arguments. SQL numbers become JSON numbers, and SQL text becomes JSON strings. `jsonb_agg` gathers rows; its order is not dependable unless you put `ORDER BY` inside the aggregate. The final `ORDER BY` sorts customer rows, not items inside each order array.

`row_to_json` converts a row to a JSON object, and `to_jsonb` converts an SQL value to JSONB. These can be useful when column names already match the desired output. A shaped `jsonb_build_object` call is clearer when the API needs selected names or a nested layout. Be careful with an outer join before aggregation: it can multiply rows if you join several one-to-many tables at once. Aggregate each child table separately before combining them.

`jsonb` does not promise an object key order. Clients should read keys by name. If a client needs an empty array rather than JSON `null`, use the `COALESCE` pattern shown above.

## Check your understanding

1. Why does Ben get `[]` instead of an order with null fields?
2. Which `ORDER BY` controls the order of Ada's orders?
3. What can happen if a query joins both orders and addresses before grouping?

## Further reading

- [PostgreSQL JSON creation functions](https://www.postgresql.org/docs/current/functions-json.html)
- [PostgreSQL JSON aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
