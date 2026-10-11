# Inactive Sellers

Find sellers who made no sales during calendar year 2020. A seller may have sold in another year and still qualify. A seller with no orders at all also qualifies.

## Sample data

```sql
CREATE TEMP TABLE sellers (seller_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE orders (
  order_id integer PRIMARY KEY,
  seller_id integer NOT NULL,
  sold_at timestamp NOT NULL
);
INSERT INTO sellers VALUES
  (1, 'Ana'), (2, 'Ben'), (3, 'Cara'), (4, 'Dev');
INSERT INTO orders VALUES
  (10, 1, '2020-01-01 00:00:00'),
  (11, 2, '2019-12-31 23:59:00'),
  (12, 2, '2021-01-01 00:00:00'),
  (13, 4, '2020-12-31 23:59:59');
```

## Solution

```sql
SELECT s.seller_id, s.name
FROM sellers AS s
WHERE NOT EXISTS (
  SELECT 1
  FROM orders AS o
  WHERE o.seller_id = s.seller_id
    AND o.sold_at >= '2020-01-01 00:00:00'
    AND o.sold_at < '2021-01-01 00:00:00'
)
ORDER BY s.seller_id;
```

The answer is Ben and Cara. Ben sold outside 2020 only. Cara has no order rows. Ana and Dev each have a 2020 sale. The year filter belongs inside the `NOT EXISTS` query: it asks whether this seller has a sale *in that year*. Filtering an outer joined order table in `WHERE` can remove the null row that represents a seller with no orders.

The sample uses timestamps without time zones. For stored instants, decide which business time zone defines 2020 and convert its start and end into timestamp boundaries. A sale at the start of 2021 is excluded from the 2020 test, even if it is close to midnight.

## Check your understanding

1. Why does Ben qualify although he has two orders?
2. Why is Cara included?
3. Where must the 2020 range test sit to make `NOT EXISTS` mean “no sale in 2020”?

## Further reading

- [PostgreSQL EXISTS and NOT EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html)
- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
