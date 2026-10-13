"""Check window function examples with SQLite where SQL syntax is shared.

Three PostgreSQL date expressions are changed to equivalent SQLite expressions
for these local checks. The articles keep PostgreSQL syntax.
"""

from pathlib import Path
import math
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

CONCEPTS = {
    "everything-about-window-functions": [
        (1, 10, 20, 50, 2), (2, 10, 30, 50, 1), (3, 20, 15, 15, 1),
    ],
    "core-mental-model-over-partition-by-order-by": [
        (1, "A", 10, 2, 2), (2, "A", 20, 2, 1),
        (3, "B", 5, 2, 2), (4, "B", 7, 2, 1),
    ],
    "ranking-functions": [
        (1, 100, 1, 1, 1), (2, 90, 2, 2, 2),
        (3, 90, 3, 2, 2), (4, 80, 4, 4, 3),
    ],
    "offset-functions": [
        (1, "2026-01-01", 10, None, 20),
        (1, "2026-01-02", 20, 10, 40),
        (1, "2026-01-03", 40, 20, None),
        (2, "2026-01-01", 5, None, None),
    ],
    "window-frames": [
        (1, "2026-01-01", 10, 30, 10),
        (2, "2026-01-01", 20, 30, 30),
        (3, "2026-01-02", 5, 35, 35),
    ],
    "value-window-functions": [
        ("A", 1, 10, 10, 30, 20),
        ("A", 2, 20, 10, 30, 20),
        ("A", 3, 30, 10, 30, 20),
        ("B", 4, 7, 7, 7, None),
    ],
    "distribution-helpers": [
        (1, 100, 0, 0.25, 1),
        (2, 90, 1 / 3, 0.75, 1),
        (3, 90, 1 / 3, 0.75, 2),
        (4, 70, 1, 1, 2),
    ],
    "named-windows": [
        (1, "A", 10, 30, 2, 2), (2, "A", 20, 30, 2, 1),
        (3, "B", 5, 12, 2, 2), (4, "B", 7, 12, 2, 1),
    ],
    "real-life-use-cases": [
        (1, 1, 10, 3, None, 10),
        (1, 2, 20, 2, 10, 30),
        (1, 3, 15, 1, 20, 45),
        (2, 4, 5, 2, None, 5),
        (2, 5, 7, 1, 5, 12),
    ],
}

PROBLEMS = {
    "follow-up-game-activity": [(0.5,)],
    "track-continuous-periods-of-task-failures-and-successes": [
        (1, "failed", "2026-01-01", "2026-01-02"),
        (1, "succeeded", "2026-01-03", "2026-01-04"),
        (1, "succeeded", "2026-01-06", "2026-01-06"),
        (1, "failed", "2026-01-07", "2026-01-07"),
        (2, "succeeded", "2026-01-02", "2026-01-02"),
    ],
    "find-the-largest-window-between-user-visits": [
        (1, 8), (2, 1), (3, 31),
    ],
    "top-3-salaries-per-department": [
        (10, 1, 100), (10, 2, 90), (10, 3, 90), (10, 4, 80),
        (20, 6, 50), (20, 7, 40), (20, 8, 30),
    ],
    "top-ratings-in-feb-2020": [(1, "Alpha", 4.5)],
    "find-continuous-ranges-in-logs": [(1, 3), (5, 5), (7, 8)],
    "most-experienced-employees-in-each-project": [
        (10, 1, 5), (10, 2, 5), (20, 4, 8),
    ],
    "most-recent-three-orders-for-each-customer": [
        (1, 13, "2026-01-03 08:00:00", 1),
        (1, 12, "2026-01-02 10:00:00", 2),
        (1, 11, "2026-01-02 10:00:00", 3),
        (2, 21, "2026-01-04 11:00:00", 1),
        (2, 20, "2026-01-01 12:00:00", 2),
    ],
}


def blocks_for(slug):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    return re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)


def assert_rows(actual, expected, slug):
    assert len(actual) == len(expected), f"Wrong row count in {slug}: {actual}"
    for actual_row, expected_row in zip(actual, expected):
        assert len(actual_row) == len(expected_row), f"Wrong columns in {slug}: {actual_row}"
        for value, wanted in zip(actual_row, expected_row):
            if isinstance(wanted, float):
                assert math.isclose(value, wanted, abs_tol=1e-9), (
                    f"Wrong value in {slug}: {actual_row}"
                )
            else:
                assert value == wanted, f"Wrong value in {slug}: {actual_row}"


def main():
    for slug, expected in CONCEPTS.items():
        blocks = blocks_for(slug)
        assert len(blocks) == 1, f"Unexpected SQL blocks in {slug}"
        with sqlite3.connect(":memory:") as db:
            actual = db.execute(blocks[0]).fetchall()
        assert_rows(actual, expected, slug)

    substitutions = {
        "follow-up-game-activity": (
            "f.first_day + 1", "date(f.first_day, '+1 day')"
        ),
        "track-continuous-periods-of-task-failures-and-successes": (
            "previous_day + 1", "date(previous_day, '+1 day')"
        ),
        "find-the-largest-window-between-user-visits": (
            "COALESCE(next_day, '2021-01-01') - visit_date",
            "julianday(COALESCE(next_day, '2021-01-01')) - julianday(visit_date)",
        ),
    }
    for slug, expected in PROBLEMS.items():
        blocks = blocks_for(slug)
        assert len(blocks) == 2, f"Unexpected SQL blocks in {slug}"
        query = blocks[1]
        if slug in substitutions:
            before, after = substitutions[slug]
            assert before in query, f"Expected PostgreSQL date syntax in {slug}"
            query = query.replace(before, after)
        with sqlite3.connect(":memory:") as db:
            db.executescript(blocks[0])
            actual = db.execute(query).fetchall()
        assert_rows(actual, expected, slug)

    slug = "find-team-size-for-each-employee"
    blocks = blocks_for(slug)
    assert len(blocks) == 3, f"Unexpected SQL blocks in {slug}"
    with sqlite3.connect(":memory:") as db:
        db.executescript(blocks[0])
        actual = db.execute(blocks[2]).fetchall()
    assert_rows(actual, [
        (1, 10, 2), (2, 10, 2), (3, 20, 3), (4, 20, 3), (5, 20, 3),
    ], slug)
    print(f"Checked {len(CONCEPTS)} concepts, {len(PROBLEMS)} problems, and 1 shared window example.")


if __name__ == "__main__":
    main()
