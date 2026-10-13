"""Check portable conceptual modeling examples with in-memory SQLite.

These examples use SQL understood by both SQLite and PostgreSQL. The check
does not replace running them on PostgreSQL.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "dbms"
EXPECTED = {
    "entities-entity-sets-and-attributes": [(1, "Ada", 2), (2, "Lin", 0)],
    "relationships-and-structural-constraints": [(1, "Ada", 2), (2, "Lin", 0)],
    "weak-entities-and-enhanced-er-modeling": [
        (100, 1, "Pen", 2),
        (100, 2, "Notebook", 1),
        (101, 1, "Pen", 3),
    ],
    "er-eer-to-relational-mapping": [
        ("Ada", 100, 1, "Pen", 2),
        ("Ada", 100, 2, "Notebook", 1),
    ],
}


def main():
    for slug, expected in EXPECTED.items():
        article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
        assert len(blocks) == 1, f"Expected one SQL example in {slug}"
        setup, query = blocks[0].rsplit("\nSELECT ", 1)
        with sqlite3.connect(":memory:") as db:
            db.execute("PRAGMA foreign_keys = ON")
            db.executescript(setup)
            actual = db.execute("SELECT " + query).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked the SQL results in {len(EXPECTED)} DBMS modeling articles.")


if __name__ == "__main__":
    main()
