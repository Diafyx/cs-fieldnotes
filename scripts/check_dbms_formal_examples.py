"""Check the portable SQL examples in the relational model articles.

SQLite checks the data and expected results here. PostgreSQL-specific view and
trigger examples still need PostgreSQL for a full runtime check.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "dbms"


def sql_blocks(slug):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    return re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)


def run_last_query(db, block):
    setup, query = block.rsplit("\nSELECT ", 1)
    db.executescript(setup)
    return db.execute("SELECT " + query).fetchall()


def main():
    cases = {
        "formal-relational-model-and-integrity-constraints": [
            (7, "Mina", "Research"),
            (8, "Dev", "Support"),
        ],
        "fundamental-relational-algebra": [(10,), (30,)],
        "tuple-and-domain-relational-calculus": [("Dev",), ("Mina",)],
    }

    for slug, expected in cases.items():
        blocks = sql_blocks(slug)
        assert len(blocks) == 1, f"Expected one SQL example in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.execute("PRAGMA foreign_keys = ON")
            actual = run_last_query(db, blocks[0])
        assert actual == expected, f"Wrong result in {slug}: {actual}"

    blocks = sql_blocks("joins-and-extended-relational-algebra")
    assert len(blocks) == 2, "Expected two SQL examples in joins article"
    with sqlite3.connect(":memory:") as db:
        db.execute("PRAGMA foreign_keys = ON")
        left_join = run_last_query(db, blocks[0])
        antijoin = db.execute(blocks[1]).fetchall()
    assert left_join == [
        ("Mina", 100),
        ("Mina", 101),
        ("Dev", 102),
        ("Lee", None),
    ], left_join
    assert antijoin == [("Lee",)], antijoin

    print("Checked SQL results in 4 relational model articles.")


if __name__ == "__main__":
    main()
