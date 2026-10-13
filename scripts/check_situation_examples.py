"""Check the easy situation examples with in-memory SQLite.

These examples use SQL understood by both SQLite and PostgreSQL. This check
does not replace running the pages on PostgreSQL.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"
EXPECTED = {
    "introduction-to-situation-based-questions": [[(2,)]],
    "situation-1": [[(2,)], [(2,)]],
    "situation-2": [[(2,), (3,)]],
    "situation-3": [[(3, 2, 3.0)]],
    "situation-4": [[(90,)]],
    "situation-5": [[
        (1, 12, "2026-01-12 10:00:00"),
        (2, 20, "2026-01-11 08:00:00"),
    ]],
}


def main():
    for slug, results in EXPECTED.items():
        article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
        setup, queries = ("", blocks) if slug.startswith("introduction-") else (blocks[0], blocks[1:])
        assert len(queries) == len(results), f"Unexpected query count in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.executescript(setup)
            for query, expected in zip(queries, results):
                actual = db.execute(query).fetchall()
                assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked the examples in {len(EXPECTED)} easy situation pages.")


if __name__ == "__main__":
    main()
