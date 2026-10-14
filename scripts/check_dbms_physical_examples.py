"""Check the deterministic examples in DBMS physical storage articles.

SQLite checks query results. Date literals and the hash-index declaration are
translated only for this check; PostgreSQL syntax still needs PostgreSQL.
"""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "dbms"
EXPECTED = {
    "file-organization": [(10, "A"), (20, "B"), (30, "C")],
    "index-classification-and-design": [(4, 50), (2, 30)],
    "b-trees-and-b-trees": [(20, "B"), (30, "C")],
    "static-and-dynamic-hashing": [(2,)],
}


def block(slug, language):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    found = re.findall(rf"```{language}\n(.*?)\n```", article, flags=re.DOTALL)
    assert len(found) == 1, f"Expected one {language} block in {slug}"
    return found[0]


def main():
    for slug, expected in EXPECTED.items():
        sql = block(slug, "sql")
        sql = re.sub(r"DATE '(\d{4}-\d{2}-\d{2})'", r"'\1'", sql)
        sql = sql.replace(" USING HASH (email)", " (email)")
        setup, query = sql.rsplit("\nSELECT ", 1)
        with sqlite3.connect(":memory:") as db:
            db.executescript(setup)
            actual = db.execute("SELECT " + query).fetchall()
        assert actual == expected, f"Wrong result in {slug}: {actual}"

    output = StringIO()
    with redirect_stdout(output):
        exec(compile(block("static-and-dynamic-hashing", "python"), "hash example", "exec"), {})
    assert output.getvalue().splitlines() == [
        "0 [20]",
        "1 []",
        "2 []",
        "3 [7, 11, 15]",
    ], output.getvalue()

    print("Checked 4 SQL results and the Python hash example in DBMS storage.")


if __name__ == "__main__":
    main()
