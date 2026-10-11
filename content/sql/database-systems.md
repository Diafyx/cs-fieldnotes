# Database Systems

A database is the organized data. A database management system, or DBMS, is the software that stores it, checks rules, serves queries, and coordinates changes. PostgreSQL is a DBMS. A PostgreSQL database is one database managed by that software. A Python script using PostgreSQL is a client, not the DBMS.

These names are often mixed in casual speech. Keeping them separate helps when you set up a connection or debug a query. A query can fail because the SQL is wrong, the database is missing, the server is stopped, or the client cannot authenticate. Those are different problems.

## The pieces in one request

Imagine a Java application showing a customer's latest orders:

1. The application opens a connection to the database server using a driver.
2. It sends a parameterized SQL query and the customer ID.
3. The server checks the query and the user's permissions.
4. The server chooses a plan, reads the matching rows, and sends the result.
5. The application turns the returned rows into the screen the user sees.

The driver handles the connection protocol. The database server handles stored data and query execution. The application decides what the user is allowed to ask for and how to present the answer. Database permissions are another layer of protection, not a reason to skip application checks.

## Relational databases

A relational database presents data as tables with rows and columns. Keys and constraints describe important rules. SQL lets you combine tables, filter rows, and summarize results. PostgreSQL, MySQL, and SQLite all support relational data, but they differ in features and deployment.

SQLite is an embedded database that runs inside an application and stores data in a file. PostgreSQL normally runs as a server that many clients can connect to. This difference changes setup and operations, even when basic SQL looks similar.

## Other database shapes

Some systems store documents, key-value pairs, graphs, or large analytical tables. Those shapes can help with particular access patterns. The label "NoSQL" covers many different products, so it does not tell you one set of guarantees. Ask what data you have, which questions you need to answer, and what consistency and operations you need before choosing a system.

An application can use more than one store. For example, it might keep orders in a relational database and photos in object storage. The important part is knowing which store owns the authoritative copy of each fact.

## Operational questions

Before relying on a database, know who creates backups, how restore is tested, who can connect, and how schema changes reach production. A local learning database can be simple. A production database needs clear answers to those questions. Fast queries are useful, but correct data and recoverable data come first.

## Check your understanding

1. Which part of the system runs a SQL query: a Java driver or the database server?
2. Why can two databases support similar SQL but need very different deployment steps?
3. If an application stores images outside PostgreSQL, what information might it still keep in a table?

## Further reading

- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [Python sqlite3 module](https://docs.python.org/3/library/sqlite3.html)
- [PostgreSQL client interfaces](https://www.postgresql.org/docs/current/external-interfaces.html)
