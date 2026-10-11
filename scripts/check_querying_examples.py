"""Run the practice page setup and answer queries with in-memory SQLite.

These exercises use SQL that both PostgreSQL and SQLite understand. This check
does not replace a PostgreSQL check for PostgreSQL-specific examples.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

EXPECTED = {
    "big-countries": [
        ("Alder", 3000000, 1200000),
        ("Birch", 900000, 25000000),
        ("Dune", 4000000, 40000000),
    ],
    "profitable-customers-in-2021": [(1,), (4,)],
    "odd-non-boring-movies": [
        (1, "North Road", "adventure", 8.5),
        (5, "Last Train", "drama", 8.5),
    ],
    "filter-records-excluding-a-specific-pattern": [
        (3, "TEMP-7"),
        (4, "READY_A"),
        (6, "PRETEMP_A"),
    ],
    "find-records-excluding-a-given-set-of-values": [
        (10, 1),
        (13, 5),
        (15, None),
    ],
    "find-salaries-outside-the-expected-range": [
        (1, 39999.99),
        (5, 120000.01),
    ],
    "non-referred-customers": [
        ("Anya",),
        ("Ben",),
        ("Dev",),
        ("Faye",),
    ],
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
    print(f"Checked setup and answer queries in {len(EXPECTED)} practice pages.")


if __name__ == "__main__":
    main()
