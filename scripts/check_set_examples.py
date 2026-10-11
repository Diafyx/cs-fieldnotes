"""Check set operation examples with in-memory SQLite.

The checked examples use SQL shared by PostgreSQL and SQLite. PostgreSQL's
type conversion and INTERSECT ALL behavior are covered by its documentation.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

CONCEPTS = {
    "union": [("Delhi",), ("Jaipur",), ("Pune",)],
    "union-all": [("book",), ("pen",), ("pen",), ("pen",)],
    "difference-between-union-and-union-all": [(1,), (2,), (3,)],
    "intersection": [(2,)],
}

PRACTICE = {
    "combine-active-and-archived-users": [(1,), (2,), (3,)],
    "merge-recent-orders-from-multiple-sources": [
        ("shop", 2, "2026-01-02", 30),
        ("online", 1, "2026-01-06", 100),
        ("shop", 1, "2026-01-07", 20),
        ("online", 3, "2026-01-08", 40),
    ],
    "combine-sales-records-without-deduplication": [
        ("Book", 2, 60),
        ("Pen", 3, 30),
    ],
    "reshape-products-data": [
        (1, "Notebook", "regular", 12),
        (1, "Notebook", "sale", 9),
        (2, "Pen", "regular", 2),
        (3, "Bag", "regular", 20),
        (3, "Bag", "sale", 20),
    ],
}


def blocks_for(slug):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    return re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)


def main():
    for slug, expected in CONCEPTS.items():
        blocks = blocks_for(slug)
        assert blocks, f"Missing example in {slug}"
        with sqlite3.connect(":memory:") as db:
            actual = db.execute(blocks[0]).fetchall()
            assert actual == expected, f"Wrong result in {slug}: {actual}"

    difference_query = blocks_for("difference-between-union-and-union-all")[0]
    all_query = difference_query.replace("\nUNION\n", "\nUNION ALL\n")
    assert all_query != difference_query
    with sqlite3.connect(":memory:") as db:
        actual = db.execute(all_query).fetchall()
    assert actual == [(1,), (1,), (2,), (2,), (3,)]

    for slug, expected in PRACTICE.items():
        blocks = blocks_for(slug)
        assert len(blocks) >= 2, f"Missing setup or answer in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.executescript(blocks[0])
            actual = db.execute(blocks[1]).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked {len(CONCEPTS)} concept examples and {len(PRACTICE)} practice pages.")


if __name__ == "__main__":
    main()
