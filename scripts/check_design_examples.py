"""Run portable database design examples with SQLite.

These examples use SQL shared with PostgreSQL. PostgreSQL-specific behavior is
checked against its documentation, not by this script.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"
EXAMPLES = {
    "database-design-fundamentals": [[(10, "Ada"), (11, "Ada")]],
    "importance-raw-data-and-pain": [[
        (10, "Ada", "Lamp", 2), (10, "Ada", "Mug", 1),
        (11, "Ada", "Mug", 3),
    ]],
    "core-concepts-overview": [[(1, "Support"), (2, None)]],
    "mental-model-first-principle": [[(10, "Ada", 50)]],
    "schema-design": [[(10, 50)]],
    "entity-and-attributes": [[
        (1, "Ada", "+1-555-0101"),
        (1, "Ada", "+1-555-0102"),
        (2, "Ben", None),
    ]],
    "relationships-cardinality-and-optionality": [
        [("Ada", "SQL"), ("Ada", "Networks"), ("Ben", None)],
        [("Ada", "Asia/Kolkata"), ("Ben", None)],
    ],
    "everything-about-keys": [[
        (10, "Ada", 1, "Lamp"), (10, "Ada", 2, "Mug"),
    ]],
    "normalisation-and-their-forms": [[
        (10, "Ada", "Lamp", 2), (10, "Ada", "Mug", 1),
    ]],
}


def main():
    query_count = 0
    for slug, expected_queries in EXAMPLES.items():
        article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
        assert len(blocks) == len(expected_queries), f"Unexpected SQL blocks in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.execute("PRAGMA foreign_keys = ON")
            for block, expected in zip(blocks, expected_queries):
                split = block.rfind("\nSELECT ")
                assert split >= 0, f"No final SELECT in {slug}"
                db.executescript(block[:split])
                actual = db.execute(block[split + 1:]).fetchall()
                assert actual == expected, f"Wrong result in {slug}: {actual}"
                query_count += 1

            if slug == "schema-design":
                for statement in (
                    "INSERT INTO order_items VALUES (10, 100, 1, 25)",
                    "INSERT INTO order_items VALUES (10, 999, 1, 25)",
                    "INSERT INTO order_items VALUES (10, 101, -1, 25)",
                ):
                    try:
                        db.execute(statement)
                    except sqlite3.IntegrityError:
                        pass
                    else:
                        raise AssertionError(f"Invalid order item accepted: {statement}")

    print(f"Checked {query_count} queries in {len(EXAMPLES)} database design articles.")


if __name__ == "__main__":
    main()
