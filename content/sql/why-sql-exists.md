# Why SQL Exists

Suppose a shop stores orders in a file. To answer "How much did each customer spend last month?" a program must read records, match customers to orders, filter dates, add totals, and sort the result. It must also handle a file being changed at the same time. Each new question needs more code.

SQL gives us a common way to ask those questions. The database handles storage, access paths, and safe changes. You still have to describe the result correctly. SQL does not fix a vague question or a poor table design.

## Say what you want

Here is a query for completed orders. It groups rows by customer and adds each customer's order amounts:

```sql
SELECT customer_id, SUM(amount) AS total_spent
FROM orders
WHERE status = 'completed'
GROUP BY customer_id
ORDER BY total_spent DESC;
```

You did not write a loop over the file or choose an index. The query describes the result. The database checks the statement, plans a way to run it, and returns rows. Different plans can produce the same answer.

This is called a declarative style. It saves code, but it also means that understanding the data and the query rules matters more than memorizing a particular execution order.

## Why tables help

A relational database keeps related facts in tables. One table can hold customers. Another can hold orders with a `customer_id` that points to a customer. This avoids repeating a customer's name and address on every order. It also lets the database check that an order belongs to an existing customer, if a foreign key is defined.

Tables make it possible to ask new questions without writing a new storage format. You can join customers to orders, count orders by day, or find customers with no orders. The same stored facts support different queries.

## Why a database does more than store files

The database can enforce rules such as unique IDs and required values. Transactions let several changes succeed together or be rolled back together. Indexes can help specific searches, though indexes also take space and add work when rows change. Permissions can limit who may read or change data.

These features are useful because data is shared. When two people place orders at the same time, the system must prevent one operation from leaving the data in a broken state. A plain file can be made safe too, but then your application has to build and maintain much more of that machinery.

## When SQL is a good fit

SQL fits data with clear relationships and questions that combine, filter, or summarize records. It is common in business applications, reporting, and data analysis. It is less useful as a replacement for every file. A photo or video can be stored outside the database while the database stores its owner, name, and location.

## Check your understanding

1. Which parts of the shop question describe the result, and which parts describe how to compute it?
2. Why might an `orders` table store `customer_id` instead of a full customer address?
3. Does adding an index make every query faster? What extra work does an index create?

## Further reading

- [PostgreSQL SQL tutorial](https://www.postgresql.org/docs/current/tutorial-sql.html)
- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
