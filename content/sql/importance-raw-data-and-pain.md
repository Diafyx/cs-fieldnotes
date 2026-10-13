# Importance, Raw Data and Pain

Raw data often repeats facts because it was made for a report, a spreadsheet, or an import file. Repeated facts are easy to read in one row, but they become a problem when the same fact can change in several places. Look for insert, update, and delete problems before making tables.

## A flat order sheet

```sql
CREATE TEMP TABLE raw_order_lines (
  order_id integer,
  customer_id integer,
  customer_name text,
  product_id integer,
  product_name text,
  quantity integer
);

INSERT INTO raw_order_lines VALUES
  (10, 1, 'Ada', 100, 'Lamp', 2),
  (10, 1, 'Ada', 101, 'Mug', 1),
  (11, 1, 'Ada', 101, 'Mug', 3);

SELECT order_id, customer_name, product_name, quantity
FROM raw_order_lines
ORDER BY order_id, product_id;
```

Ada's name appears three times. The product name `Mug` appears twice. If Ada changes her name, three rows need an update. Missing one row leaves two answers to the same question. If we cannot add a customer until that customer has an order, we have an insert problem. If we delete Ada's last order and lose her only customer record, we have a delete problem.

There is another risk: the sheet has no primary key or foreign keys. It can hold the same order line twice, a negative quantity, or a product ID with two names. The data can look reasonable in a small sample while the rules remain unprotected.

## Find the facts that repeat

The customer name depends on `customer_id`. The product name depends on `product_id`. Quantity belongs to one product in one order, so it depends on the order and product together in this simple model. This suggests separate `customers`, `products`, `orders`, and `order_items` tables. The item row keeps IDs and quantity. A join can rebuild a report when needed.

Do not split every repeated value without asking what it means. A price charged at purchase time is a fact about that order line. It should stay even if the current product price changes. The source and time of a fact decide where it belongs.

Before loading real data, check for conflicting copies. If product 101 is called `Mug` in one row and `Cup` in another, the schema change cannot choose the correct name for you. Clean and agree on the data rule first.

## Check your understanding

1. Which fact in the sample must be changed three times when Ada changes her name?
2. Why should an order line keep its charged price after a product's current price changes?
3. What conflict could stop you from safely building a `products` table from the sheet?

## Further reading

- [Codd's relational model paper](https://doi.org/10.1145/362384.362685)
- [PostgreSQL table constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
