# Working with Databases in SQL

Your program should send a query to the database, pass values as parameters, read the returned rows, and close its resources. The SQL does the data work. Python or Java decides when to run it and what to do with the result. Keep that boundary clear so the query can be tested on its own.

The examples below read orders from PostgreSQL. They assume an `orders` table with `order_id`, `customer_id`, and `amount` columns. They also assume the needed driver is installed and the connection values are supplied through environment variables.

## Python with Psycopg

Psycopg is a PostgreSQL driver for Python. In Psycopg 3, `%s` is the placeholder for a value, regardless of whether the value is text or a number. Pass a tuple as the second argument to `execute`.

```python
import os
import psycopg

customer_id = 10

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    rows = conn.execute(
        """
        SELECT order_id, amount
        FROM orders
        WHERE customer_id = %s
        ORDER BY order_id
        """,
        (customer_id,),
    ).fetchall()

for order_id, amount in rows:
    print(order_id, amount)
```

The one-element tuple needs its trailing comma. `DATABASE_URL` should be a PostgreSQL connection string, such as one provided by your local setup or hosting service. Do not place a real password in source code or commit it to a repository. The connection block closes the connection when it leaves the block and handles transaction completion according to Psycopg's context manager rules.

## Java with JDBC

JDBC is Java's database API. PostgreSQL needs the pgJDBC driver available at runtime. A `PreparedStatement` uses `?` placeholders, and JDBC parameter positions start at 1.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class ReadOrders {
    public static void main(String[] args) throws SQLException {
        long customerId = 10;
        String url = System.getenv("JDBC_DATABASE_URL");
        String user = System.getenv("DB_USER");
        String password = System.getenv("DB_PASSWORD");

        try (Connection conn = DriverManager.getConnection(url, user, password);
             PreparedStatement stmt = conn.prepareStatement(
                 "SELECT order_id, amount FROM orders " +
                 "WHERE customer_id = ? ORDER BY order_id")) {
            stmt.setLong(1, customerId);

            try (ResultSet rows = stmt.executeQuery()) {
                while (rows.next()) {
                    System.out.println(
                        rows.getLong("order_id") + " " + rows.getBigDecimal("amount")
                    );
                }
            }
        }
    }
}
```

`JDBC_DATABASE_URL` should look like `jdbc:postgresql://localhost:5432/fieldnotes`. The `try` blocks close the result, statement, and connection even if a database call fails. In a larger application, a connection pool normally manages connections, but the query and parameter rules stay the same.

## Values are not identifiers

Parameters stand for data values. They cannot stand for a table name or a column name. If a user can choose a sort column, use a short allowlist in your application and insert only a name from that list. Do not pass arbitrary text as an identifier or build SQL from unchecked input.

## Check your understanding

1. Why does the Python parameter tuple contain a comma after `customer_id`?
2. Which method gives the first `?` in the Java query its value?
3. Why should the database URL and password be kept out of source code?

## Further reading

- [Psycopg basic usage](https://www.psycopg.org/psycopg3/docs/basic/usage.html)
- [Psycopg query parameters](https://www.psycopg.org/psycopg3/docs/basic/params.html)
- [pgJDBC connecting to PostgreSQL](https://jdbc.postgresql.org/documentation/use/)
- [Oracle JDBC prepared statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)
