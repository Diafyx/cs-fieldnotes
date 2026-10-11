"""Check the data modification practice examples with in-memory SQLite.

These two examples use SQL understood by PostgreSQL and SQLite. This check
does not cover PostgreSQL-specific ALTER TABLE or TRUNCATE behavior.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

EXPECTED = {
    "system-settings": [
        ("email_alerts", "on"),
        ("page_size", "20"),
        ("theme", "dark"),
    ],
    "employee-salary": [
        (1, 55000, 1),
        (2, 66000, 1),
        (3, 70000, 0),
    ],
}


def main():
    for slug, expected in EXPECTED.items():
        article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
        assert len(blocks) >= 3, f"Missing setup, write, or check query in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.executescript(blocks[0])
            db.executescript(blocks[1])
            actual = db.execute(blocks[2]).fetchall()
            assert actual == expected, f"Wrong result in {slug}: {actual}"
            db.executescript(blocks[1])
            repeated = db.execute(blocks[2]).fetchall()
            assert repeated == expected, f"Repeated write changed result in {slug}: {repeated}"
    print(f"Checked writes and repeated writes in {len(EXPECTED)} practice pages.")


if __name__ == "__main__":
    main()
