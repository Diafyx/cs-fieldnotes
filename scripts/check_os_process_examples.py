"""Run the process and thread examples and check their module headings."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import read_inventory


def run_example(slug, expected):
    text = (ROOT / "content" / "os" / f"{slug}.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
    assert len(blocks) == 1, f"Expected one Python block in {slug}"
    output = StringIO()
    with redirect_stdout(output):
        exec(blocks[0], {})
    assert output.getvalue().splitlines() == expected, slug


def main():
    run_example(
        "program-vs-process-vs-thread",
        ["thread shares process: True", "child has another PID: True"],
    )
    run_example("process-creation-and-termination", ["child ran", "3"])

    module = "Module-2 (Process Management in Operating System)"
    topics = [
        topic
        for topic in read_inventory()
        if any(
            placement["course"] == "Operating Systems"
            and placement["sections"][0] == module
            for placement in topic["placements"]
        )
    ]
    assert len(topics) == 4, f"Expected four module headings, found {len(topics)}"
    for topic in topics:
        path = ROOT / "content" / topic["subject"] / f'{topic["slug"]}.md'
        assert path.exists(), f"Missing OS article: {topic['title']}"
        assert path.read_text(encoding="utf-8").splitlines()[0] == f'# {topic["title"]}'

    print("Checked process and thread examples and all four process module articles.")


if __name__ == "__main__":
    main()
