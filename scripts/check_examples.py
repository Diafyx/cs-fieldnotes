"""Run a few portable SQL examples against an in-memory database."""

import sqlite3


def main():
    with sqlite3.connect(":memory:") as db:
        db.executescript("""
            CREATE TABLE books (
                book_id integer PRIMARY KEY,
                title text NOT NULL,
                price numeric(8, 2) NOT NULL
            );
            INSERT INTO books (book_id, title, price) VALUES
                (1, 'The River', 12.50),
                (2, 'Small Maps', 18.00),
                (3, 'Northbound', 9.75);
        """)
        titles = db.execute("""
            SELECT title FROM books WHERE price < 15 ORDER BY title
        """).fetchall()
        assert titles == [("Northbound",), ("The River",)]

        db.executescript("""
            CREATE TABLE employees (employee_id integer PRIMARY KEY, bonus integer);
            INSERT INTO employees VALUES (1, 0), (2, 50), (3, NULL), (4, NULL), (5, 100);
        """)
        counts = db.execute("SELECT COUNT(*), COUNT(bonus) FROM employees").fetchone()
        assert counts == (5, 3)
        missing = db.execute("SELECT employee_id FROM employees WHERE bonus IS NULL ORDER BY employee_id").fetchall()
        assert missing == [(3,), (4,)]

        db.executescript("""
            CREATE TABLE orders (customer_id integer, status text, amount integer);
            INSERT INTO orders VALUES
                (1, 'paid', 80), (1, 'paid', 40), (1, 'pending', 500),
                (2, 'paid', 70), (3, 'paid', 100);
        """)
        totals = db.execute("""
            SELECT customer_id, SUM(amount) AS total
            FROM orders
            WHERE status = 'paid'
            GROUP BY customer_id
            HAVING SUM(amount) >= 100
            ORDER BY total DESC, customer_id
        """).fetchall()
        assert totals == [(1, 120), (3, 100)]
    print("Checked the book query, NULL counts, and grouped order query.")


if __name__ == "__main__":
    main()
