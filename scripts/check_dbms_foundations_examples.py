"""Check portable DBMS foundations examples with in-memory SQLite.

The role query uses PostgreSQL system functions, so it is not checked here.
This script does not replace running the examples on PostgreSQL.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "dbms"
EXPECTED = {
    "file-systems-vs-database-management-systems": [
        (1, "ada@example.test"),
        (2, "lin@example.test"),
    ],
    "data-abstraction-schemas-instances-and-data-independence": [
        (1, "Ada"),
        (2, "Lin"),
    ],
    "dbms-components-and-end-to-end-query-flow": [
        (1, 20),
        (3, 10),
    ],
    "data-models-and-database-families": [
        ("Ada", 10, 25),
        ("Ada", 11, 40),
    ],
}


def main():
    for slug, expected in EXPECTED.items():
        article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
        assert len(blocks) == 1, f"Expected one SQL example in {slug}"
        setup, query = blocks[0].rsplit("\nSELECT ", 1)
        with sqlite3.connect(":memory:") as db:
            db.executescript(setup)
            actual = db.execute("SELECT " + query).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked the SQL results in {len(EXPECTED)} DBMS foundations articles.")


if __name__ == "__main__":
    main()
