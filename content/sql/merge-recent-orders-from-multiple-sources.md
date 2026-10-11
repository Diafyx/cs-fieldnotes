# Merge Recent Orders from Multiple Sources

Orders from a website and a shop need one report. An order ID is unique within its source, but the same number can be used by both sources. Keep the source name so those orders stay separate.

## The question

Return every order on or after January 1, 2026 from both tables. Include `source`, `order_id`, `ordered_on`, and `total`. Sort by date, source, and ID. Dates are stored as ISO dates.

```sql
CREATE TEMP TABLE online_orders (
  order_id integer PRIMARY KEY,
  ordered_on date NOT NULL,
  total numeric(10, 2) NOT NULL
);

CREATE TEMP TABLE shop_orders (
  order_id integer PRIMARY KEY,
  ordered_on date NOT NULL,
  total numeric(10, 2) NOT NULL
);

INSERT INTO online_orders (order_id, ordered_on, total) VALUES
  (1, '2026-01-06', 100.00),
  (2, '2025-12-30', 50.00),
  (3, '2026-01-08', 40.00);

INSERT INTO shop_orders (order_id, ordered_on, total) VALUES
  (1, '2026-01-07', 20.00),
  (2, '2026-01-02', 30.00),
  (3, '2025-12-01', 15.00);
```

## A solution

```sql
SELECT 'online' AS source, order_id, ordered_on, total
FROM online_orders
WHERE ordered_on >= '2026-01-01'
UNION ALL
SELECT 'shop' AS source, order_id, ordered_on, total
FROM shop_orders
WHERE ordered_on >= '2026-01-01'
ORDER BY ordered_on, source, order_id;
```

The rows are shop order 2 on January 2, online order 1 on January 6, shop order 1 on January 7, and online order 3 on January 8. Older rows are filtered out before combining the results. `UNION ALL` keeps every order. The two orders numbered 1 are different orders because their sources differ.

The `ORDER BY` belongs to the combined result. Do not assume online orders appear first because their query was written first. If the tables stored timestamps rather than dates, a cutoff would need a time zone rule. If they used different currencies, totals would need conversion before adding them in a report.

## Check your understanding

1. Why are there two rows with order ID 1?
2. Why is the date filter written in both queries?
3. What would have to change before totals in different currencies could be added?

## Further reading

- [PostgreSQL combining queries](https://www.postgresql.org/docs/current/queries-union.html)
- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
