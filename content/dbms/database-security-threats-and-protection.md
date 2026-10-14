# Database Security Threats and Protection

A database can be harmed through an unsafe query, a stolen login, a public network port, or a backup that anyone can read. Protecting the database means controlling each path to it. One safe SQL query cannot make an overpowered account safe, and a strong password cannot fix SQL injection.

## Know the main paths

| Threat | What can happen | Protection |
| --- | --- | --- |
| SQL injection | User input becomes part of the SQL command. | Bind values as parameters. Allowlist any dynamic SQL identifiers. |
| Stolen credentials | Someone connects with a real account. | Protect secrets, rotate exposed credentials, and grant only needed access. |
| Excess privileges | One bug can read or change more data than needed. | Use separate application, migration, and administration roles. |
| Open network access | Unwanted clients can reach the database service. | Limit reachable hosts and require suitable authentication. |
| Intercepted connection | Data or credentials can be exposed in transit. | Use TLS with server identity checks where the connection crosses an untrusted network. |
| Unsafe elevated function | A caller gets the function owner's privileges through a flaw. | Review `SECURITY DEFINER`, restrict `EXECUTE`, and set a safe `search_path`. |
| Lost or altered data | A bad write, disk failure, or ransomware removes the only copy. | Keep protected, independent backups and test restores. |

## Keep input as a value

Suppose a search page accepts an email address. Use this PostgreSQL setup in the same connection as either example below:

```sql
CREATE TEMP TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_email TEXT NOT NULL
);
INSERT INTO orders VALUES
    (1, 'sam@example.test'),
    (2, 'lee@example.test');
```

Do not build SQL by joining the email address to the query string. In Python with Psycopg 3, use a `%s` placeholder and pass the value separately:

```python
# conn is an existing Psycopg connection. email comes from a request.
with conn.cursor() as cur:
    cur.execute(
        "SELECT order_id FROM orders WHERE customer_email = %s",
        (email,),
    )
    order_ids = [row[0] for row in cur.fetchall()]
```

In Java with JDBC, the same rule uses a `PreparedStatement` and a `?` placeholder:

```java
// connection is an existing JDBC connection. email comes from a request.
String query = "SELECT order_id FROM orders WHERE customer_email = ?";
try (PreparedStatement statement = connection.prepareStatement(query)) {
    statement.setString(1, email);
    try (ResultSet results = statement.executeQuery()) {
        while (results.next()) {
            System.out.println(results.getInt("order_id"));
        }
    }
}
```

Both queries search for the email value as data. With `email = "sam@example.test"`, each finds order ID `1`. An unmatched email gives an empty result. An input containing a quote or SQL words remains one value. The table and column names are fixed in these examples. Parameters cannot stand for a table name or SQL keyword. If users may choose a sort field, map a short list of allowed choices to fixed SQL fragments. For a truly dynamic PostgreSQL identifier in Python, use Psycopg's `sql.Identifier` rather than inserting raw text.

Input validation still matters for length, format, and business rules. It does not replace parameters. A string that looks harmless to a validator can still break a query built by concatenation.

## Reduce what one mistake can do

Use a dedicated login role for the application. Give it only the schemas, tables, and commands it needs. Keep schema migration and backup privileges under separate roles. Check grants inherited through other roles and through `PUBLIC`. If the app uses a shared database role for all customers, the app still has to authorize each customer's request; database login alone does not identify the customer.

PostgreSQL's `pg_hba.conf` controls which clients may authenticate and how. Avoid `trust` for connections where an untrusted person can reach the server. Use a suitable password method such as SCRAM-SHA-256, or another approved authentication method for the environment. Limit network reach as well. For remote PostgreSQL clients using libpq, `sslmode=verify-full` checks both encryption and the server's certificate name when the trust setup is correct. Merely turning on TLS without verifying the server leaves room for connecting to an impostor.

Store credentials outside source code and logs. Protect backup files and WAL archives as carefully as the live data. Review extensions and elevated functions before granting access. PostgreSQL `SECURITY DEFINER` functions run with their owner's rights; an unsafe `search_path` can let an attacker place an object where the function will find it. Keep the path to trusted schemas and limit who can execute the function.

Watch connection counts, slow queries, errors, and failed logins. Timeouts and connection limits can reduce damage from stuck or abusive requests, but set them for the workload. Log enough to investigate incidents without logging secrets. Keep the server and client libraries updated, and test recovery from a separate backup copy.

## Try it yourself

1. Why does a parameter protect an email value but not a dynamic table name?
2. What can still go wrong if a safe parameterized query runs under a superuser account?
3. Why should a remote client verify the PostgreSQL server's identity as well as use encryption?
4. Which separate roles would you use for normal app queries and schema changes?

## References

- [Psycopg 3 query parameters](https://www.psycopg.org/psycopg3/docs/basic/params.html)
- [Java JDBC prepared statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)
- [PostgreSQL connection authentication](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)
- [PostgreSQL TLS settings for clients](https://www.postgresql.org/docs/current/libpq-ssl.html)
- [PostgreSQL function security](https://www.postgresql.org/docs/current/sql-createfunction.html)
