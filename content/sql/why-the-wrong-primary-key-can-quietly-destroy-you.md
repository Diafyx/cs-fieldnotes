# Why the Wrong Primary Key Can Quietly Destroy You

A primary key is the chosen identity for a table row. Other tables may store it in foreign keys, and application code may use it for years. A key that changes, is too wide, or does not truly identify one row can make later changes hard. Choose it from the meaning of the data, not from what happens to be unique in a small sample.

## Keep identity when a detail changes

```sql
CREATE TEMP TABLE customers (
  customer_id bigint PRIMARY KEY,
  email text NOT NULL UNIQUE,
  name text NOT NULL
);

CREATE TEMP TABLE orders (
  order_id bigint PRIMARY KEY,
  customer_id bigint NOT NULL REFERENCES customers(customer_id)
);

INSERT INTO customers VALUES (1, 'ada@old.example', 'Ada');
INSERT INTO orders VALUES (10, 1);

UPDATE customers
SET email = 'ada@new.example'
WHERE customer_id = 1;

SELECT o.order_id, c.customer_id, c.email
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id;
```

The result is order `10`, customer `1`, and `ada@new.example`. The order link stays the same because it uses a stable customer ID. The `UNIQUE` email rule still prevents two customers from using the same exact email. If email were the primary key and orders referred to it, a change would need a coordinated update of the key and its references. PostgreSQL could reject it or cascade it, depending on the foreign key rule.

## Check what the key really means

`(order_id, product_id)` works as an order-line key only if one product can occur once per order. If the same product can appear on two separate lines, that pair is not unique. Use a line number with the order ID, or a separate line ID, and keep any needed business uniqueness rule separately. A key that accidentally rejects valid rows is a data model bug.

A natural key such as an externally assigned SKU can be a good primary key if it is short, stable, and genuinely unique for the table's lifetime. A made-up numeric or UUID key can avoid tying row identity to changing business text. But adding a surrogate key does not make duplicate business records safe; use a separate `UNIQUE` constraint where the business rule requires it.

Key width and insertion pattern affect a B-tree's size and maintenance work. Wide keys also widen matching foreign keys and join values. In PostgreSQL, a primary key creates a separate unique B-tree index; it does **not** physically sort the heap. Other indexes do not automatically store the primary key as part of every entry. Do not copy assumptions from a different database engine when judging key performance. Compare real index sizes and write plans on representative data.

## Check your understanding

1. Why did the order keep its customer link after Ada's email changed?
2. When would `(order_id, product_id)` fail to identify an order line?
3. Why can a surrogate primary key still need a separate unique business rule?

## Further reading

- [PostgreSQL primary and foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL B-tree indexes](https://www.postgresql.org/docs/current/btree.html)
- [PostgreSQL heap and index separation](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
