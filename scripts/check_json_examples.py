"""Check JSON literals in the PostgreSQL JSON section.

This checks literal syntax, not PostgreSQL execution. A PostgreSQL server is
needed to run the SQL examples themselves.
"""

import json
from pathlib import Path
import re


CONTENT = Path(__file__).resolve().parents[1] / "content" / "sql"
SLUGS = (
    "json-in-sql",
    "dummy-data-setup",
    "json-insertion-data-loading",
    "json-read-query-commands",
    "json-arrays-and-search",
    "json-updates",
    "json-output-builders",
    "performance-and-indexing",
    "upsert-power-features",
)


def main():
    literal_count = 0
    for slug in SLUGS:
        article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```sql\n(.*?)\n```", article, flags=re.DOTALL)
        assert blocks, f"No SQL example in {slug}"
        for block in blocks:
            for match in re.finditer(r"'((?:[^']|'')*)'::jsonb", block, flags=re.DOTALL):
                literal = match.group(1).replace("''", "'")
                try:
                    json.loads(literal)
                except json.JSONDecodeError as error:
                    raise AssertionError(f"Invalid JSON literal in {slug}: {literal}") from error
                literal_count += 1
    assert literal_count >= 20, f"Unexpectedly few JSON literals: {literal_count}"
    print(f"Checked {literal_count} JSONB literals across {len(SLUGS)} JSON articles.")


if __name__ == "__main__":
    main()
