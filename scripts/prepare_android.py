"""Build the site and bundle its pages into the standalone Android app."""

from pathlib import Path
import json
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DEST = ROOT / "android" / "app" / "src" / "main" / "assets"
SKIP = {"_headers", "sw.js", "offline-pack.json", "manifest.webmanifest"}


def main():
    subprocess.run([sys.executable, str(ROOT / "build.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "make_android_icons.py")], cwd=ROOT, check=True)
    if not DEST.resolve().is_relative_to(ROOT.resolve()) or DEST.name != "assets":
        raise ValueError("Android assets path is outside this project")
    if DEST.exists():
        shutil.rmtree(DEST)
    shutil.copytree(DIST, DEST, ignore=lambda _directory, names: SKIP.intersection(names))

    for page in DEST.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        html = html.replace('  <link rel="manifest" href="/manifest.webmanifest">\n', "")
        page.write_text(html, encoding="utf-8")

    home = DEST / "index.html"
    html = home.read_text(encoding="utf-8")
    app_note = '<section class="phone-section"><div><div class="eyebrow">OFFLINE APP</div><h2>Notes on your device</h2><p>Finished notes are included in this app. Search and reading work without internet. New notes arrive with app updates.</p></div></section>'
    html, count = re.subn(r'<section class="phone-section">.*?</section>', app_note, html, count=1)
    if count != 1:
        raise ValueError("Could not replace the browser install instructions")
    home.write_text(html, encoding="utf-8")

    privacy = DEST / "privacy.html"
    html = privacy.read_text(encoding="utf-8")
    body = '<div class="page-intro"><div class="eyebrow">ABOUT THIS APP</div><h1>Privacy and safety</h1><p>Finished notes are stored inside this app. Reading and search work without internet.</p></div><div class="privacy-copy"><h2>What stays on your device</h2><p>The articles, search list, fonts, and icons come with the app. Search runs on your device. Your color theme is saved on your device. You can remove the saved theme in Android app settings by clearing this app\'s data.</p><h2>Internet and permissions</h2><p>This app does not ask for internet, camera, location, or microphone access. Reference links open in your browser, where that browser\'s own rules apply.</p><h2>Updates</h2><p>New articles arrive when you install a new version of this app. The app does not download notes in the background.</p><h2>Check the source</h2><p>The <a href="https://github.com/Diafyx/cs-fieldnotes">source code is public</a>. You can see how the app and notes are made.</p></div>'
    body = body.replace('<h1>Privacy and safety</h1>', '<h1>Privacy policy</h1>')
    body = body.replace('<h2>Check the source</h2>', '<h2>Privacy questions</h2><p>You can ask a privacy question through <a href="https://github.com/Diafyx/cs-fieldnotes/issues">Fieldnotes GitHub Issues</a>.</p><h2>Check the source</h2>')
    html, count = re.subn(r'<main id="main">.*?</main>', f'<main id="main">{body}</main>', html, count=1)
    if count != 1:
        raise ValueError("Could not replace the browser privacy text")
    privacy.write_text(html, encoding="utf-8")

    catalog = json.loads((DEST / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog:
        if item["ready"] and not (DEST / item["url"].lstrip("/")).is_file():
            raise ValueError(f"Android app is missing {item['url']}")
    print(f"Bundled {sum(item['ready'] for item in catalog)} finished articles for Android.")


if __name__ == "__main__":
    main()
