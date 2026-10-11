"""Check generated links, content style, and complete inventory mapping."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build import CONTENT, DIST, ROOT, read_inventory


EXPECTED_HEADINGS = 1372


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "a" and "href" in values:
            self.links.append(values["href"])


def main():
    topics = read_inventory()
    headings = sum(len(t["placements"]) for t in topics)
    assert headings == EXPECTED_HEADINGS, f"Expected {EXPECTED_HEADINGS} headings, found {headings}"
    assert len({t["id"] for t in topics}) == len(topics), "Topic IDs are not unique"
    catalog = json.loads((DIST / "catalog.json").read_text(encoding="utf-8"))
    assert len(catalog) == len(topics), "Search catalog is missing topics"
    ready = {t["id"] for t in topics if (CONTENT / t["subject"] / f'{t["slug"]}.md').exists()}
    assert sum(item["ready"] for item in catalog) == len(ready), "Ready count differs from content files"

    for source in list(CONTENT.glob("*/*.md")) + [ROOT / "CONTENT_GUIDE.md"]:
        text = source.read_text(encoding="utf-8")
        assert "\u2014" not in text and "\u2013" not in text, f"Long dash in {source}"
        assert "\ufffd" not in text, f"Replacement character in {source}"

    pages = list(DIST.rglob("*.html"))
    for page in pages:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        assert len(parser.ids) == len(set(parser.ids)), f"Duplicate HTML ID in {page}"
        for href in parser.links:
            if not href.startswith("/"):
                continue
            path = urlsplit(href).path
            target = DIST / (path.lstrip("/") or "index.html")
            assert target.exists(), f"Broken link {href} in {page}"
    for item in catalog:
        path = urlsplit(item["url"]).path
        assert (DIST / path.lstrip("/")).exists(), f"Broken search result: {item['url']}"
    print(f"Checked {headings} headings, {len(topics)} shared topics, {len(ready)} articles, and {len(pages)} pages.")


if __name__ == "__main__":
    main()
