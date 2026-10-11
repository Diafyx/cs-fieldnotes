"""Check transaction examples whose SQL is shared by SQLite and PostgreSQL.

PostgreSQL roles, timeouts, and concurrency behavior need PostgreSQL itself.
"""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"

EXAMPLES = {
    "permissions-and-transactions-part-2": [(1, 70), (2, 80)],
    "connection-connection-pool-and-commit": [(1, "done")],
    "rollback": [(1, 5)],
    "savepoint": [(1, 3), (2, 5)],
}


def main():
    for slug, expected in EXAMPLES.items():
        article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
        assert len(blocks) >= 3, f"Expected setup, transaction, and query in {slug}"
        with sqlite3.connect(":memory:") as db:
            db.executescript(blocks[0])
            db.executescript(blocks[1])
            actual = db.execute(blocks[2]).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"
    print(f"Checked {len(EXAMPLES)} transaction examples.")


if __name__ == "__main__":
    main()
