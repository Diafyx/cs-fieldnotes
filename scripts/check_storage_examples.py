"""Check portable results in the storage and index section with SQLite.

PostgreSQL CTID and INCLUDE index behavior require a PostgreSQL server. This
script checks the shared SQL results and constraints without claiming to test
physical page layout or planner choices.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"
EXAMPLES = {
    "storage-keys-and-query-performance": [(2, "Ben")],
    "how-a-b-tree-is-built-with-data": [(20, "B"), (30, "C")],
    "why-the-wrong-primary-key-can-quietly-destroy-you": [
        (10, 1, "ada@new.example"),
    ],
    "index-strategy-at-scale": [
        (102, "2026-01-03 09:00:00", 20),
        (103, "2026-01-02 09:00:00", 30),
        (101, "2026-01-01 09:00:00", 10),
    ],
}


def block_for(slug):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
    assert len(blocks) == 1, f"Unexpected SQL blocks in {slug}"
    return blocks[0]


def main():
    for slug, expected in EXAMPLES.items():
        block = block_for(slug)
        position = block.rfind("\nSELECT ")
        assert position >= 0, f"Missing SELECT in {slug}"
        setup, query = block[:position], block[position + 1:]
        if slug == "index-strategy-at-scale":
            index_start = setup.index("CREATE INDEX work_orders_pending_recent_idx")
            index_end = setup.index("WHERE status = 'pending';", index_start) + len(
                "WHERE status = 'pending';"
            )
            setup = setup[:index_start] + setup[index_end:]
        with sqlite3.connect(":memory:") as db:
            db.execute("PRAGMA foreign_keys = ON")
            db.executescript(setup)
            actual = db.execute(query).fetchall()
            assert actual == expected, f"Wrong result in {slug}: {actual}"
            if slug == "why-the-wrong-primary-key-can-quietly-destroy-you":
                try:
                    db.execute("INSERT INTO customers VALUES (2, 'ada@new.example', 'Other')")
                except sqlite3.IntegrityError:
                    pass
                else:
                    raise AssertionError("Duplicate email was accepted")
            if slug == "index-strategy-at-scale":
                try:
                    db.execute("INSERT INTO work_orders VALUES "
                               "(301, 3, '2026-01-06 09:00:00', 'invalid', 10)")
                except sqlite3.IntegrityError:
                    pass
                else:
                    raise AssertionError("Invalid order status was accepted")

    block = block_for("where-rows-actually-live")
    assert "ctid AS old_ctid" in block and "n.ctid AS current_ctid" in block
    setup = block[:block.index("CREATE TEMP TABLE before_update AS")]
    update = re.search(r"UPDATE notes SET body = 'revised text' WHERE note_id = 1;", block)
    assert update, "Missing update in row location example"
    with sqlite3.connect(":memory:") as db:
        db.executescript(setup)
        db.execute(update.group())
        assert db.execute("SELECT note_id, body FROM notes ORDER BY note_id").fetchall() == [
            (1, "revised text"), (2, "other text"),
        ]

    print("Checked logical results in 5 storage and index articles.")


if __name__ == "__main__":
    main()
