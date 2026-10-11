"""Run join examples and practice answers with in-memory SQLite.

These examples use SQL understood by PostgreSQL and the installed SQLite.
This check does not replace testing PostgreSQL-specific behavior in PostgreSQL.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

CONCEPTS = {
    "joins-deep-dive": [(10, "Ana"), (11, "Ana")],
    "right-join": [(1, "Sales"), (2, None)],
    "on-vs-where": [(1, 10), (2, None)],
    "left-join": [(1, "Ana", 10), (1, "Ana", 11), (2, "Ben", 12), (3, "Cara", None)],
    "inner-join": [(10, "Ana"), (11, "Ana")],
    "full-outer-join": [(1, "Pen", None), (2, "Book", "arrived"), (3, None, "unexpected")],
    "cross-join": [
        ("blue", "L"), ("blue", "M"), ("blue", "S"),
        ("red", "L"), ("red", "M"), ("red", "S"),
    ],
    "implicit-join": [(10, "Ana"), (11, "Ana")],
    "self-join": [("Asha", None), ("Ben", "Asha"), ("Cara", "Asha")],
    "natural-join": [],
}

FOLLOW_UP_EXAMPLES = {
    "right-join": [(1, "Sales"), (2, None)],
    "on-vs-where": [(1, 10)],
    "left-join": [(1, 2), (2, 1), (3, 0)],
    "natural-join": [(1, "Sales")],
}

PRACTICE = {
    "employees-and-their-departments": [
        (1, "Asha", "Engineering"), (2, "Ben", "Sales"), (3, "Cara", None),
    ],
    "customer-orders-overview": [
        (1, "Ana", 2, 100), (2, "Ben", 1, 20), (3, "Cara", 0, 0),
    ],
    "employees-with-confirmed-salary-records": [
        (1, "Asha", 50000), (2, "Ben", 60000),
    ],
    "generate-all-possible-user-category-pairs": [
        (1, "Books"), (1, "Games"), (1, "Music"),
        (2, "Books"), (2, "Games"), (2, "Music"),
    ],
    "employees-with-or-without-salary-records": [
        (1, "Asha", 50000), (2, "Ben", 60000), (3, "Cara", None),
    ],
    "match-employees-with-their-salaries": [
        (1, "Asha", 50000), (3, "Cara", 70000),
    ],
    "employees-earning-more-than-their-manager": [
        ("Ben", "Asha"), ("Dev", "Ben"),
    ],
    "students-enrolled-in-courses": [
        (1, "Ana", 10, "SQL"), (1, "Ana", 20, "Networks"), (2, "Ben", 10, "SQL"),
    ],
    "sales-analysis": [
        (1, "Pen", 5, 11), (2, "Book", 1, 10), (3, "Bag", 0, 0),
    ],
    "minimum-distance-between-points": [(1, 3, 1.414)],
    "suspended-accounts": [(1, "Asha"), (4, "Dev")],
    "find-team-size-for-each-employee": [
        (1, 10, 2), (2, 10, 2),
        (3, 20, 3), (4, 20, 3), (5, 20, 3),
    ],
    "average-experience-by-project": [
        (10, "Apollo", 3.0), (20, "Boreal", 5.5), (30, "Cedar", None),
    ],
    "warehouse-stock-manager": [
        (1, 10, 5), (1, 20, 2), (2, 10, 3), (2, 20, 0),
    ],
    "table-join-operation": [
        (1, 1, "Ana", "paid"), (2, 1, "Ben", "pending"),
    ],
    "inactive-customers": [(1, "Ana"), (3, "Cara")],
    "students-enrolled-in-non-existent-departments": [
        (2, "Ben", 99), (4, "Dev", 98),
    ],
    "low-bonus-employees": [
        (1, "Asha", 500), (3, "Cara", 0), (4, "Dev", 0),
    ],
    "available-seat-streaks": [(1, 1), (2, 3)],
    "visitors-without-transactions": [(10, 1), (20, 1)],
    "a-b-buyers-without-c": [(1,), (5,)],
    "product-selling-price-report": [(1, 2.33), (2, 10), (3, 0)],
    "updated-bank-balances": [(1, 85), (2, 40), (3, 0)],
    "most-frequent-travellers": [(1, "Asha", 2), (2, "Ben", 2)],
    "suggested-pages": [(20, 2), (30, 1)],
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

    for slug, expected in FOLLOW_UP_EXAMPLES.items():
        blocks = blocks_for(slug)
        assert len(blocks) >= 2, f"Missing second example in {slug}"
        with sqlite3.connect(":memory:") as db:
            actual = db.execute(blocks[1]).fetchall()
        assert actual == expected, f"Wrong second result in {slug}: {actual}"

    for slug, expected in PRACTICE.items():
        blocks = blocks_for(slug)
        assert len(blocks) >= 2, f"Missing setup or answer in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.executescript(blocks[0])
            actual = db.execute(blocks[1]).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked {len(CONCEPTS) + len(FOLLOW_UP_EXAMPLES)} join examples and {len(PRACTICE)} practice pages.")


if __name__ == "__main__":
    main()
