# Salespersons Without RED Orders

Return salespeople who have never handled an order for the company named `RED`. Someone with no orders also qualifies.

## Sample data

```sql
CREATE TEMP TABLE salespeople (salesperson_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE companies (company_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE orders (order_id integer PRIMARY KEY, salesperson_id integer, company_id integer);
INSERT INTO salespeople VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cara');
INSERT INTO companies VALUES (100, 'RED'), (200, 'BLUE');
INSERT INTO orders VALUES (10, 1, 100), (11, 2, 200);
```

## Solution

```sql
SELECT s.salesperson_id, s.name
FROM salespeople AS s
WHERE NOT EXISTS (
  SELECT 1
  FROM orders AS o
  JOIN companies AS c ON c.company_id = o.company_id
  WHERE o.salesperson_id = s.salesperson_id
    AND c.name = 'RED'
)
ORDER BY s.salesperson_id;
```

The result is Ben and Cara. Ben sold to BLUE only. Cara has no orders. Ana has one RED order, so she is excluded even if she also sold to another company. The correlation to `s.salesperson_id` makes the test specific to each salesperson.

Avoid `NOT IN (SELECT salesperson_id ...)` if the inner IDs can be `NULL`. One null can make nonmatching rows disappear from a `WHERE` result. `NOT EXISTS` directly asks the intended question. Company names may have duplicates or change over time; a stable company ID is usually a better business key if one is available.

## Check your understanding

1. Why is Cara included?
2. Would another BLUE order change the result?
3. What would go wrong if the salesperson comparison were left out?

## Further reading

- [PostgreSQL EXISTS and NOT EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html)
