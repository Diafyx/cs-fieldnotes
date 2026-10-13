"""Check query results used in the performance section with SQLite.

PostgreSQL EXPLAIN output and the PL/pgSQL procedure need a PostgreSQL server.
For generated data, this script inserts the same rows in SQLite and runs the
SELECT statements copied from the articles.
"""

from datetime import date, timedelta
from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"
START = date(2026, 1, 1)


def blocks_for(slug):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    return re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)


def sqlite_dates(sql):
    return re.sub(r"DATE '([0-9-]+)'", r"'\1'", sql)


def final_select(block):
    position = block.rfind("\nSELECT ")
    assert position >= 0, "SQL block has no final SELECT"
    return block[:position], sqlite_dates(block[position + 1:])


def main():
    blocks = blocks_for("performance-debugging")
    assert len(blocks) == 2
    setup, query = final_select(blocks[0])
    with sqlite3.connect(":memory:") as db:
        db.executescript(setup)
        assert db.execute(query).fetchall() == [(10, 30), (20, 5)]

    blocks = blocks_for("debugging-correctness")
    assert len(blocks) == 3
    setup, wrong_query = final_select(blocks[0])
    with sqlite3.connect(":memory:") as db:
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript(setup)
        assert db.execute(wrong_query).fetchall() == [(1, 4)]
        assert db.execute(blocks[1]).fetchall() == [(1, 2), (2, 1)]
        assert db.execute(blocks[2]).fetchall() == [(10, 3), (11, 1), (20, 0)]

    blocks = blocks_for("raw-data-setup-and-stored-procedures")
    assert len(blocks) == 2
    assert "GET DIAGNOSTICS changed = ROW_COUNT" in blocks[1]
    _, count_query = final_select(blocks[0])
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE orders (order_id integer PRIMARY KEY, customer_id integer, "
                   "placed_on text, status text, amount numeric)")
        db.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", (
            (g, (g % 100) + 1, (START + timedelta(days=g % 90)).isoformat(),
             "paid" if g % 3 == 0 else "pending", 10)
            for g in range(1, 10001)
        ))
        assert db.execute(count_query.replace("perf_lab.orders", "orders")).fetchall() == [
            (10000, 6667)
        ]
        db.execute("UPDATE orders SET status = 'paid' "
                   "WHERE order_id = 2 AND status = 'pending'")
        assert db.execute("SELECT order_id, status FROM orders WHERE order_id = 2").fetchall() == [
            (2, "paid")
        ]

    blocks = blocks_for("debugging-queries-with-explain")
    assert len(blocks) == 1
    _, query = final_select(blocks[0])
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE events (event_id integer PRIMARY KEY, user_id integer, event_day text)")
        db.executemany("INSERT INTO events VALUES (?, ?, ?)", (
            (g, (g % 100) + 1, (START + timedelta(days=g % 30)).isoformat())
            for g in range(1, 10001)
        ))
        actual = db.execute(query.replace("demo_events", "events")).fetchall()
        assert actual == [(6,), (306,), (606,), (906,), (1206,)], actual

    blocks = blocks_for("query-performance")
    assert len(blocks) == 1
    _, query = final_select(blocks[0])
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE sales (order_id integer PRIMARY KEY, customer_id integer, "
                   "placed_on text, amount numeric)")
        db.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", (
            (g, (g % 100) + 1, (START + timedelta(days=g % 30)).isoformat(), 10)
            for g in range(1, 10001)
        ))
        actual = db.execute(query.replace("perf_sales", "sales")).fetchall()
        assert actual == [
            (9706, "2026-01-17"),
            (9406, "2026-01-17"),
            (9106, "2026-01-17"),
        ], actual

    print("Checked query results in 5 performance articles.")


if __name__ == "__main__":
    main()
