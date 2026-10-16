"""Run the OS launch example and check the first module's article map."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import read_inventory


def main():
    slug = "what-happens-when-we-open-an-app"
    text = (ROOT / "content" / "os" / f"{slug}.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
    assert len(blocks) == 1, "Expected one Python launch example"
    output = StringIO()
    with redirect_stdout(output):
        exec(blocks[0], {})
    assert output.getvalue().splitlines() == ["hello from child", "0"]

    module = "Module-1 (Operating System Basics and OS Introduction)"
    topics = [
        topic
        for topic in read_inventory()
        if any(
            placement["course"] == "Operating Systems"
            and placement["sections"][0] == module
            for placement in topic["placements"]
        )
    ]
    assert len(topics) == 5, f"Expected five module headings, found {len(topics)}"
    for topic in topics:
        path = ROOT / "content" / topic["subject"] / f'{topic["slug"]}.md'
        assert path.exists(), f"Missing OS article: {topic['title']}"
        assert path.read_text(encoding="utf-8").splitlines()[0] == f'# {topic["title"]}'

    print("Checked OS child process example and all five first-module articles.")


if __name__ == "__main__":
    main()
