"""Check that the installable app includes every finished page offline."""

from pathlib import Path
import hashlib
import json
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build import BINARY_ASSETS, CSP, render_inline


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def main():
    manifest = json.loads((DIST / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert manifest["start_url"] == manifest["scope"] == "/"
    assert manifest["display"] == "standalone"
    assert manifest["name"] and manifest["short_name"]
    sizes = set()
    for icon in manifest["icons"]:
        path = DIST / icon["src"].lstrip("/")
        data = path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n", path
        width, height = struct.unpack(">II", data[16:24])
        assert width == height and str(width) + "x" + str(height) == icon["sizes"], path
        sizes.add(width)
    assert {192, 512}.issubset(sizes)

    pack_bytes = (DIST / "offline-pack.json").read_bytes()
    pack = json.loads(pack_bytes)
    assert pack["/"] == pack["/index.html"]
    for path in DIST.rglob("*"):
        if path.is_file() and path.suffix in (".html", ".css", ".js", ".json", ".webmanifest") and path.name not in ("offline-pack.json", "sw.js"):
            url = "/" + path.relative_to(DIST).as_posix()
            assert pack[url] == path.read_text(encoding="utf-8"), url

    catalog = json.loads(pack["/catalog.json"])
    for item in catalog:
        if item["ready"]:
            assert item["url"] in pack, item["url"]
    binary_data = {url: (DIST / url.lstrip("/")).read_bytes() for url in BINARY_ASSETS}
    for url in ("/assets/fonts/DMSans.ttf", "/assets/fonts/Fraunces.ttf"):
        assert binary_data[url][:4] in (b"\x00\x01\x00\x00", b"OTTO"), url
    version = hashlib.sha256(pack_bytes + b"".join(binary_data.values())).hexdigest()[:16]
    worker = (DIST / "sw.js").read_text(encoding="utf-8")
    assert f"fieldnotes-{version}" in worker
    assert hashlib.sha256(pack_bytes).hexdigest() in worker
    for data in binary_data.values():
        assert hashlib.sha256(data).hexdigest() in worker
    assert "__CACHE_VERSION__" not in worker and "__PACK_SHA256__" not in worker
    headers = (DIST / "_headers").read_text(encoding="utf-8")
    assert f"Content-Security-Policy: {CSP}" in headers
    assert json.dumps(CSP) in worker
    assert "X-Content-Type-Options: nosniff" in headers
    assert "Referrer-Policy: no-referrer" in headers
    assert "fonts.googleapis.com" not in pack["/assets/style.css"]
    assert render_inline("[bad](//other.example)") == "[bad](//other.example)"
    assert render_inline("<script>alert(1)</script>") == "&lt;script&gt;alert(1)&lt;/script&gt;"
    assert 'rel="manifest" href="/manifest.webmanifest"' in pack["/"]
    assert 'data-offline-status' in pack["/"]
    print(f"Checked Android icons, app manifest, and {len(pack)} offline files, including {sum(item['ready'] for item in catalog)} articles.")


if __name__ == "__main__":
    main()
