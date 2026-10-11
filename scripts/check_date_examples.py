"""Check date examples using SQLite for SQL shared with PostgreSQL.

One PostgreSQL date-add expression is translated to SQLite syntax before its
result is checked. PostgreSQL-only EXTRACT and clock functions are not run here.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

EXAMPLES = {
    "dates-functions-and-filtering": [
        (2, "2026-03-01 00:00:00"), (3, "2026-03-31 23:59:59"),
    ],
    "filtering-with-date-ranges": [(1,), (2,)],
    "finding-first-and-latest-events": [(1, 10, 12), (2, 20, 20)],
    "latest-2020-login": [
        (1, "2020-12-31 23:00:00"), (3, "2020-02-29 08:00:00"),
    ],
    "kid-friendly-movies-in-last-month": [(10, "Sky"), (11, "River")],
    "warmer-days": [(2, "2026-01-02"), (5, "2026-01-06")],
    "restaurant-payment-trends": [
        ("2026-01-07", 280, 40.0), ("2026-01-08", 350, 50.0),
    ],
    "inactive-sellers": [(2, "Ben"), (3, "Cara")],
}


def blocks_for(slug):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    return re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)


def main():
    for slug, expected in EXAMPLES.items():
        blocks = blocks_for(slug)
        expected_count = 3 if slug == "kid-friendly-movies-in-last-month" else 2
        assert len(blocks) == expected_count, f"Unexpected SQL blocks in {slug}"
        query = blocks[1]
        if slug == "warmer-days":
            before = "yesterday.record_date + 1"
            assert before in query, f"Expected PostgreSQL date arithmetic in {slug}"
            query = query.replace(before, "date(yesterday.record_date, '+1 day')")
        with sqlite3.connect(":memory:") as db:
            db.executescript(blocks[0])
            actual = db.execute(query).fetchall()
            if slug == "kid-friendly-movies-in-last-month":
                count = db.execute(blocks[2]).fetchall()
                assert count == [(2,)], f"Wrong unique movie count: {count}"
        assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked {len(EXAMPLES)} date problem examples.")


if __name__ == "__main__":
    main()
