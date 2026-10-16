"""Run the small distributed database and analytics article examples."""

import json
from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "dbms"


def block(slug, language):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    blocks = re.findall(rf"```{language}\n(.*?)\n```", article, re.DOTALL)
    assert len(blocks) == 1, f"Expected one {language} example in {slug}"
    return blocks[0]


def sql_result(slug):
    setup, query = block(slug, "sql").rsplit("\nSELECT ", 1)
    with sqlite3.connect(":memory:") as db:
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript(setup)
        return db.execute("SELECT " + query).fetchall()


def main():
    namespace = {}
    exec(block("partitioning-sharding-and-distributed-ids", "python"), namespace)
    assert namespace["orders"] == [(42, 101), (43, 101)]

    order = json.loads(block("nosql-data-models-and-sql-vs-nosql-decisions", "json"))
    total = sum(item["quantity"] * item["unit_price_cents"] for item in order["items"])
    assert total == order["total_cents"] == 3200

    outbox_rows = sql_result("distributed-transactions-and-coordination")
    assert outbox_rows == [(7, "created", "OrderCreated")], outbox_rows

    sales_rows = sql_result("oltp-olap-warehousing-and-columnar-storage")
    assert sales_rows == [("Home", 12, 1), ("Stationery", 9, 2)], sales_rows

    print("Checked distributed IDs, document total, outbox, and OLAP examples.")


if __name__ == "__main__":
    main()
