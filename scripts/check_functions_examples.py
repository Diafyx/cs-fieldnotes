"""Run the function section's practice queries against their sample data.

The answers use SQL shared by PostgreSQL and SQLite. The small registered
functions give SQLite the PostgreSQL names used in two examples.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

EXPECTED = {
    "call-count-between-pairs": [
        (1, 2, 2, 12),
        (1, 3, 2, 12),
        (2, 3, 1, 4),
    ],
    "valid-triangle-check": [
        (1, 3, 4, 5, "Yes"),
        (2, 1, 2, 3, "No"),
        (3, 0, 3, 3, "No"),
        (4, 5, 5, 5, "Yes"),
    ],
    "instant-food-delivery": [(66.67,)],
    "special-bonus-calculation": [
        (1, 1000),
        (2, 0),
        (3, 0),
        (5, 0),
        (7, 1500),
    ],
    "node-classification": [
        (1, "Root"),
        (2, "Inner"),
        (3, "Leaf"),
        (4, "Leaf"),
    ],
    "apples-vs-oranges": [
        ("2026-01-01", 6),
        ("2026-01-02", -3),
        ("2026-01-03", -3),
    ],
    "query-quality-analysis": [
        ("alpha", 2.0, 33.33),
        ("beta", 0.75, 50.0),
    ],
    "exceeding-tweet-length": [(2,)],
}


def main():
    for slug, expected in EXPECTED.items():
        article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
        sql_blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
        assert len(sql_blocks) >= 2, f"Missing setup or answer in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.create_function("LEAST", 2, min)
            db.create_function("GREATEST", 2, max)
            db.create_function("CHAR_LENGTH", 1, lambda s: len(s) if s is not None else None)
            db.executescript(sql_blocks[0])
            actual = db.execute(sql_blocks[1]).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked setup and answer queries in {len(EXPECTED)} function pages.")


if __name__ == "__main__":
    main()
