"""Check CTE examples that use SQL shared by PostgreSQL and SQLite."""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

QUERY_ONLY = {
    "with-and-as-ctes": [(1, 60), (3, 35)],
    "non-recursive-ctes": [(1, 60)],
}

WITH_SETUP = {
    "ctes-and-temporary-tables": [(10, 50)],
    "recursive-ctes-for-hierarchies": [
        (1, "Asha", 0), (2, "Ben", 1), (4, "Dev", 1), (3, "Cara", 2),
    ],
    "most-frequently-ordered-product-s-for-each-customer": [
        (1, 10, "Pen", 2), (1, 20, "Book", 2), (2, 20, "Book", 3),
    ],
    "find-missing-subtasks-for-each-task": [(1, 2), (2, 1)],
}


def blocks_for(slug):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    return re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)


def main():
    for slug, expected in QUERY_ONLY.items():
        blocks = blocks_for(slug)
        assert len(blocks) == 1, f"Expected one query in {slug}"
        with sqlite3.connect(":memory:") as db:
            actual = db.execute(blocks[0]).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"

    for slug, expected in WITH_SETUP.items():
        blocks = blocks_for(slug)
        assert len(blocks) >= 2, f"Expected setup and query in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.executescript(blocks[0])
            actual = db.execute(blocks[1]).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked {len(QUERY_ONLY) + len(WITH_SETUP)} CTE examples.")


if __name__ == "__main__":
    main()
