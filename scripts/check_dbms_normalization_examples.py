"""Check portable SQL and Python examples in the normalization pages.

The SQL examples use syntax shared by SQLite and PostgreSQL. This does not
replace a PostgreSQL runtime check.
"""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "dbms"

SQL_EXPECTED = {
    "redundancy-and-update-anomalies": [
        ("Mina", "Support"),
        ("Dev", "Support"),
        ("Lee", "Research"),
    ],
    "functional-dependencies-and-keys": [
        ("Mina", "Databases", "A"),
        ("Mina", "Networks", "B"),
        ("Dev", "Databases", "A"),
    ],
    "decomposition-quality-and-normalization-algorithms": [
        (1, "Mina", 10),
        (2, "Dev", 20),
    ],
    "multivalued-dependencies-4nf-join-dependencies-and-5nf": [
        ("Mina", "English", "Chess"),
        ("Mina", "English", "Cycling"),
        ("Mina", "Hindi", "Chess"),
        ("Mina", "Hindi", "Cycling"),
    ],
}


def blocks(slug, language):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    return re.findall(rf"```{language}\n(.*?)\n```", article, flags=re.DOTALL)


def main():
    for slug, expected in SQL_EXPECTED.items():
        examples = blocks(slug, "sql")
        assert len(examples) == 1, f"Expected one SQL block in {slug}"
        setup, query = examples[0].rsplit("\nSELECT ", 1)
        with sqlite3.connect(":memory:") as db:
            db.execute("PRAGMA foreign_keys = ON")
            db.executescript(setup)
            actual = db.execute("SELECT " + query).fetchall()
        assert actual == expected, f"Wrong SQL result in {slug}: {actual}"

    python_examples = blocks("armstrongs-axioms-attribute-closure-and-minimal-cover", "python")
    assert len(python_examples) == 1, "Expected one closure example"
    output = StringIO()
    with redirect_stdout(output):
        exec(compile(python_examples[0], "closure example", "exec"), {})
    assert output.getvalue().splitlines() == [
        "['A', 'B', 'C', 'D', 'E']",
        "['B', 'C']",
    ], output.getvalue()

    print("Checked 4 SQL examples and the Python closure example in DBMS normalization.")


if __name__ == "__main__":
    main()
