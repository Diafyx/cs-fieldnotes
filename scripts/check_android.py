"""Check that the Android app can read every bundled page offline."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import posixpath
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build import CSP


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "android" / "app" / "src" / "main" / "assets"
MAIN = ROOT / "android" / "app" / "src" / "main"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for attr in ("href", "src"):
            if value := values.get(attr):
                self.links.append((tag, attr, value))


def bundled_path(page, href):
    url = urlsplit(href)
    if url.scheme or url.netloc or not url.path:
        return None
    decoded = unquote(url.path)
    if decoded.startswith("/"):
        name = posixpath.normpath(decoded).lstrip("/")
    else:
        name = posixpath.normpath(posixpath.join(page.parent.relative_to(ASSETS).as_posix(), decoded))
    if name in ("", "."):
        name = "index.html"
    if name.startswith("../") or name == "..":
        raise AssertionError(f"Link escapes Android assets: {page}: {href}")
    return ASSETS / name


def main():
    assert (MAIN / "res" / "drawable-nodpi" / "app_icon.png").is_file()
    assert (ASSETS / "index.html").is_file(), "Run python scripts/prepare_android.py first"
    assert not any((ASSETS / name).exists() for name in ("sw.js", "offline-pack.json", "manifest.webmanifest", "_headers"))

    manifest = ET.parse(MAIN / "AndroidManifest.xml").getroot()
    android = "{http://schemas.android.com/apk/res/android}"
    assert not manifest.findall("uses-permission"), "The offline app must not request permissions"
    application = manifest.find("application")
    assert application is not None and application.get(android + "usesCleartextTraffic") == "false"
    assert application.get(android + "allowBackup") == "false"

    java = (MAIN / "java" / "org" / "diafyx" / "fieldnotes" / "MainActivity.java").read_text(encoding="utf-8")
    assert f'CSP = "{CSP}"' in java, "Android CSP differs from the website CSP"
    assert 'new WebViewAssetLoader.AssetsPathHandler(this)' in java
    assert 'settings.setAllowFileAccess(false)' in java
    assert 'settings.setAllowContentAccess(false)' in java
    assert 'if (!isLocal(uri)) return blocked(403, "Forbidden")' in java
    assert "location.hostname === 'appassets.androidplatform.net'" in (ASSETS / "assets" / "app.js").read_text(encoding="utf-8")

    catalog = json.loads((ASSETS / "catalog.json").read_text(encoding="utf-8"))
    assert len(catalog) == 707
    ready = sum(bool(item["ready"]) for item in catalog)
    assert ready > 0, "No finished articles were bundled"
    for item in catalog:
        path = bundled_path(ASSETS / "index.html", item["url"])
        assert path and path.is_file(), f"Missing catalog link: {item['url']}"

    pages = list(ASSETS.rglob("*.html"))
    assert len(pages) >= ready
    for page in pages:
        html = page.read_text(encoding="utf-8")
        assert 'rel="manifest"' not in html, f"Browser install tag in {page}"
        parser = Links()
        parser.feed(html)
        for tag, attr, href in parser.links:
            if tag in ("script", "link", "img") and urlsplit(href).scheme:
                raise AssertionError(f"Remote page resource in {page}: {href}")
            target = bundled_path(page, href)
            assert target is None or target.is_file(), f"Broken bundled link in {page}: {href}"

    home = (ASSETS / "index.html").read_text(encoding="utf-8")
    privacy = (ASSETS / "privacy.html").read_text(encoding="utf-8")
    assert "Notes on your device" in home and "Install app" not in home
    assert "does not ask for internet" in privacy
    assert not re.search(r"https?://(fieldnotes-15h\.pages\.dev|takeuforward\.org)", home)
    print(f"Android bundle checked: {ready} articles, {len(pages)} pages, local links, no app permissions.")


if __name__ == "__main__":
    main()
