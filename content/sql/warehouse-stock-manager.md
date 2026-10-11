# Warehouse Stock Manager

A stock report may need to show every warehouse-product pair, even when no stock row has been recorded. Make the full grid with a cross join, then attach stock with a left join.

## The question

Return each warehouse and product with its quantity. In this exercise, a missing stock row means zero units. Sort by warehouse ID and product ID.

```sql
CREATE TEMP TABLE warehouses (
  warehouse_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE products (
  product_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE stock (
  warehouse_id integer NOT NULL,
  product_id integer NOT NULL,
  quantity integer NOT NULL CHECK (quantity >= 0),
  PRIMARY KEY (warehouse_id, product_id)
);

INSERT INTO warehouses VALUES (1, 'North'), (2, 'South');
INSERT INTO products VALUES (10, 'Pen'), (20, 'Book');
INSERT INTO stock VALUES (1, 10, 5), (1, 20, 2), (2, 10, 3);
```

## A solution

```sql
SELECT w.warehouse_id, p.product_id,
       COALESCE(s.quantity, 0) AS quantity
FROM warehouses AS w
CROSS JOIN products AS p
LEFT JOIN stock AS s
  ON s.warehouse_id = w.warehouse_id
 AND s.product_id = p.product_id
ORDER BY w.warehouse_id, p.product_id;
```

The result is North-Pen 5, North-Book 2, South-Pen 3, and South-Book 0. The cross join creates four expected pairs. The stock row matches by *both* keys. `COALESCE` turns South-Book's missing row into zero under this exercise's stated rule.

In a real inventory system, a missing row might mean unknown stock rather than zero. Decide that before applying `COALESCE`. The grid can become large: a thousand warehouses and ten thousand products create ten million pairs before stock is joined.

## Check your understanding

1. Why is South-Book present in the result?
2. What wrong matches could appear if `product_id` were omitted from the `ON` condition?
3. When would showing zero for a missing stock row be misleading?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
