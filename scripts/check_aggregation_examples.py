"""Run aggregation practice setup and answer queries with in-memory SQLite.

The checked queries use SQL understood by both PostgreSQL and SQLite. This
does not test PostgreSQL-only behavior mentioned elsewhere in the articles.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

EXPECTED = {
    "first-login-analysis": [
        (1, "2026-01-03"),
        (2, "2026-03-05"),
        (3, "2026-02-01"),
    ],
    "employee-work-time-summary": [
        ("2026-01-01", 1, 35),
        ("2026-01-01", 2, 10),
        ("2026-01-02", 1, 30),
    ],
    "unique-subjects-per-teacher": [(1, 2), (2, 2), (3, 1)],
    "user-follower-count": [(10, 2), (11, 1), (13, 3)],
    "crm-automotive-sales-analysis": [
        ("hatch", 1, 15000, 1),
        ("sedan", 2, 41000, 2),
        ("suv", 2, 61000, 1),
    ],
    "highest-order-placing-customer": [(1, 2), (3, 2)],
    "frequent-actor-director-duos": [(10, 20), (11, 20)],
    "large-classes": [("math", 5)],
    "email-duplicates": [("a@example.com", 2), ("c@example.com", 3)],
}


def main():
    for slug, expected in EXPECTED.items():
        article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
        sql_blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
        assert len(sql_blocks) >= 2, f"Missing setup or answer in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.executescript(sql_blocks[0])
            actual = db.execute(sql_blocks[1]).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked setup and answer queries in {len(EXPECTED)} aggregation pages.")


if __name__ == "__main__":
    main()
