"""Run SQL examples shared by PostgreSQL and SQLite on their sample data."""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

CONCEPTS = {
    "everything-about-subqueries": [(1, 40)],
    "introduction-to-subqueries-in": [(1, "Ana"), (3, "Cara")],
    "exists-and-not-exists": [(2, "Ben")],
    "correlated-subqueries": [(2, 10, 80), (4, 20, 50)],
}

PRACTICE = {
    "contest-participation-rate": [(20, 75), (10, 50), (30, 0)],
    "high-report-managers": [(1, "Asha"), (2, "Ben")],
    "all-product-buyers": [(1, "Ana")],
    "highest-non-repeating-number": [(8,)],
    "find-the-first-device-logged-in-by-each-player": [(1, "phone"), (2, "browser")],
    "salespersons-without-red-orders": [(2, "Ben"), (3, "Cara")],
    "employees-with-the-highest-salary-in-each-department": [
        (10, 2, "Ben", 70), (10, 3, "Cara", 70), (20, 5, "Ema", 60),
    ],
    "find-the-most-recent-order-for-each-product": [
        (1, "Pen", 12), (2, "Book", 13), (3, "Bag", None),
    ],
    "find-transactions-with-maximum-amount-per-day": [
        (10, "2026-01-01", 50), (11, "2026-01-01", 50), (13, "2026-01-02", 70),
    ],
    "incomplete-employee-records": [(2,), (3,)],
    "find-quiet-students-in-all-exams": [(1, "Ana")],
    "top-grade-per-student": [(1, 10, 90), (2, 20, 75)],
    "swap-consecutive-seats": [
        (1, "Ben"), (2, "Ana"), (3, "Dev"), (4, "Cara"), (5, "Ema"),
    ],
    "safe-investment-countries": [(2, "South")],
    "tennis-grand-slam-winners": [
        (1, "Ana", 4), (2, "Ben", 3), (3, "Cara", 1),
    ],
    "football-team-scores": [
        (3, "Owls", 4, 4), (1, "Lions", 3, 4),
        (2, "Bears", 1, 1), (4, "Foxes", 0, 0),
    ],
    "order-count-per-customer": [
        (1, "Ana", 2), (2, "Ben", 1), (3, "Cara", 0),
    ],
    "boolean-expression-evaluator": [
        (1, "false"), (2, "true"), (3, "true"), (4, "true"),
    ],
    "immediate-first-orders-percentage": [(66.67,)],
    "find-all-employees-reporting-to-the-head-of-the-company": [
        (2, "Ben"), (3, "Cara"), (4, "Dev"), (5, "Ema"),
    ],
    "orphan-employees": [(3, "Cara", 99)],
}


def blocks_for(slug):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    return re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)


def main():
    for slug, expected in CONCEPTS.items():
        blocks = blocks_for(slug)
        assert len(blocks) == 1, f"Expected one query in {slug}"
        with sqlite3.connect(":memory:") as db:
            actual = db.execute(blocks[0]).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"

    for slug, expected in PRACTICE.items():
        blocks = blocks_for(slug)
        assert len(blocks) == 2, f"Expected setup and answer in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.executescript(blocks[0])
            actual = db.execute(blocks[1]).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked {len(CONCEPTS)} concepts and {len(PRACTICE)} subquery problems.")


if __name__ == "__main__":
    main()
