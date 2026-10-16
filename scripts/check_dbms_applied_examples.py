"""Check the DBMS capstone, rollback, and complete DBMS heading map."""

from pathlib import Path
import re
import sqlite3
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import read_inventory


def sql_block(slug, count=1, index=0):
    text = (ROOT / "content" / "dbms" / f"{slug}.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```sql\n(.*?)\n```", text, re.DOTALL)
    assert len(blocks) == count, f"Expected {count} SQL blocks in {slug}"
    return blocks[index]


def main():
    setup, query = sql_block("schema-design-capstone").rsplit("\nSELECT ", 1)
    with sqlite3.connect(":memory:") as db:
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript(setup)
        rows = db.execute("SELECT " + query).fetchall()
        assert rows == [(100, "Ana", 22)], rows
        assert db.execute("SELECT current_price FROM cap_products WHERE product_id = 20").fetchone() == (14,)
        assert db.execute("SELECT COUNT(*) FROM cap_orders WHERE customer_id = 2").fetchone() == (0,)

    setup, query = sql_block("concurrency-and-recovery-lab", count=2, index=1).rsplit("\nSELECT ", 1)
    with sqlite3.connect(":memory:") as db:
        db.executescript(setup)
        assert db.execute("SELECT " + query).fetchall() == [(100,)]

    topics = read_inventory()
    dbms = [t for t in topics if any(p["course"] == "DBMS" for p in t["placements"])]
    placements = [p for t in dbms for p in t["placements"] if p["course"] == "DBMS"]
    modules = {p["sections"][0] for p in placements}
    assert len(placements) == 217, f"Expected 217 DBMS headings, found {len(placements)}"
    assert len(modules) == 23, f"Expected 23 DBMS modules, found {len(modules)}"
    for topic in dbms:
        path = ROOT / "content" / topic["subject"] / f'{topic["slug"]}.md'
        assert path.exists(), f"Missing DBMS article: {topic['title']}"
        assert path.read_text(encoding="utf-8").splitlines()[0] == f'# {topic["title"]}'

    print(f"Checked capstone and rollback results; all {len(placements)} DBMS headings have articles.")


if __name__ == "__main__":
    main()
