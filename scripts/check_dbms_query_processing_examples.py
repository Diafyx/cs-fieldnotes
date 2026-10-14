"""Check the portable query results in DBMS query processing articles.

SQLite checks the first SQL block in each page. PostgreSQL EXPLAIN plans are
data and version dependent, so this script does not assert their shape.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "dbms"
EXPECTED = {
    "from-sql-to-an-executable-plan": [("Mina", 10), ("Dev", 12)],
    "algorithms-for-selection-projection-sorting-and-aggregation": [
        ("West", 2, 40),
        ("East", 2, 30),
    ],
    "join-processing-algorithms": [
        ("Mina", 10),
        ("Dev", 12),
        ("Lee", None),
    ],
    "cost-based-query-optimization": [
        (1, "open"),
        (3, "click"),
        (4, "close"),
    ],
}


def main():
    for slug, expected in EXPECTED.items():
        article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
        assert len(blocks) == 2, f"Expected a query and EXPLAIN block in {slug}"
        setup, query = blocks[0].rsplit("\nSELECT ", 1)
        with sqlite3.connect(":memory:") as db:
            db.execute("PRAGMA foreign_keys = ON")
            db.executescript(setup)
            actual = db.execute("SELECT " + query).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"

    print("Checked SQL results in 4 DBMS query processing articles.")


if __name__ == "__main__":
    main()
