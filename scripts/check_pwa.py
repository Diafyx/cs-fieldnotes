"""Check that the installable app includes every finished page offline."""

from pathlib import Path
import hashlib
import json
import struct


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
    icons = b"".join((DIST / "assets" / f"icon-{size}.png").read_bytes() for size in (192, 512))
    version = hashlib.sha256(pack_bytes + icons).hexdigest()[:16]
    worker = (DIST / "sw.js").read_text(encoding="utf-8")
    assert f"fieldnotes-{version}" in worker
    assert "__CACHE_VERSION__" not in worker
    assert 'rel="manifest" href="/manifest.webmanifest"' in pack["/"]
    assert 'data-offline-status' in pack["/"]
    print(f"Checked Android icons, app manifest, and {len(pack)} offline files, including {sum(item['ready'] for item in catalog)} articles.")


if __name__ == "__main__":
    main()
