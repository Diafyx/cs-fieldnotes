"""Build the local study site from the topic inventory and hand-written Markdown."""

from collections import defaultdict
from html import escape
from pathlib import Path
import hashlib
import json
import re
import shutil
import unicodedata


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
TOPICS = ROOT / "source-topics.md"
CONTENT = ROOT / "content"
CSP = "default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data:; connect-src 'self'; manifest-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"
BINARY_ASSETS = ("/assets/icon-192.png", "/assets/icon-512.png", "/assets/fonts/DMSans.ttf", "/assets/fonts/Fraunces.ttf")

SUBJECTS = {
    "sql": ("SQL and Data Engineering", "Queries, data models, and production database work."),
    "dbms": ("DBMS", "How databases store, protect, and retrieve data."),
    "os": ("Operating Systems", "Processes, memory, files, and concurrency."),
    "networks": ("Computer Networks", "How machines exchange data across networks."),
    "oop": ("Object-Oriented Programming", "Objects, Java, and design choices."),
    "lld": ("Low-Level Design", "Designing maintainable systems and APIs."),
}
SUBJECT_ORDER = ["sql", "dbms", "os", "networks", "oop", "lld"]


def slugify(value):
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-") or "topic"


def subject_for(course):
    if course.startswith("SQL"):
        return "sql"
    if course.startswith("DBMS"):
        return "dbms"
    if course.startswith("Operating Systems"):
        return "os"
    if course.startswith("Computer Networks"):
        return "networks"
    if course == "OOPS":
        return "oop"
    if course.startswith("Low Level Design"):
        return "lld"
    return None


def read_inventory():
    group = course = None
    sections = []
    topics = {}
    by_slug = {}
    for raw in TOPICS.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^(#{1,6}) (.+)$", raw)
        if heading:
            level, title = len(heading.group(1)), heading.group(2).strip()
            if level == 1:
                group = title
                course = None
            elif level == 2:
                course = title
                sections = []
            else:
                sections = sections[: level - 3] + [title]
            continue
        if not raw.startswith("- ") or not course or group == "DSA":
            continue
        subject = subject_for(course)
        if not subject:
            raise ValueError(f"Unknown course: {course}")
        title = raw[2:].strip()
        identity = (subject, title.casefold())
        if identity not in topics:
            base = slugify(title)
            slug = base
            if (subject, slug) in by_slug and by_slug[(subject, slug)] != identity:
                digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:6]
                slug = f"{base}-{digest}"
            by_slug[(subject, slug)] = identity
            topics[identity] = {
                "id": f"{subject}/{slug}",
                "subject": subject,
                "title": title,
                "slug": slug,
                "placements": [],
            }
        topics[identity]["placements"].append({"subject": subject, "course": course, "sections": sections.copy()})
    by_title = defaultdict(list)
    for topic in topics.values():
        by_title[topic["title"].casefold()].append(topic)
    shared = []
    for versions in by_title.values():
        canonical = next((topic for topic in versions if topic["subject"] == "sql"), versions[0])
        canonical["placements"] = [placement for topic in versions for placement in topic["placements"]]
        shared.append(canonical)
    return shared


def render_inline(raw):
    parts = []
    token = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*|\[[^]]+\]\([^)]+\))")
    for piece in token.split(raw):
        if piece.startswith("`") and piece.endswith("`"):
            parts.append(f"<code>{escape(piece[1:-1])}</code>")
        elif piece.startswith("**") and piece.endswith("**"):
            parts.append(f"<strong>{escape(piece[2:-2])}</strong>")
        elif piece.startswith("[") and "](" in piece and piece.endswith(")"):
            label, href = piece[1:-1].split("](", 1)
            if href.startswith(("https://", "http://", "#")) or (href.startswith("/") and not href.startswith("//")):
                parts.append(f'<a href="{escape(href, quote=True)}">{escape(label)}</a>')
            else:
                parts.append(escape(piece))
        else:
            parts.append(escape(piece))
    return "".join(parts)


def render_markdown(source):
    lines = source.splitlines()
    out = []
    headings = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("```"):
            language = re.sub(r"[^a-z0-9+-]", "", line[3:].lower())
            body = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                body.append(lines[index])
                index += 1
            out.append(f'<pre><code class="language-{language}">{escape(chr(10).join(body))}</code></pre>')
            index += 1
            continue
        match = re.match(r"^(#{1,6}) (.+)$", line)
        if match:
            level, title = len(match.group(1)), match.group(2).strip()
            if level == 1 and not out:
                index += 1
                continue
            anchor = slugify(title)
            headings.append((level, title, anchor))
            out.append(f'<h{level} id="{anchor}">{render_inline(title)}</h{level}>')
            index += 1
            continue
        if line.startswith("- ") or re.match(r"^\d+\. ", line):
            ordered = not line.startswith("- ")
            tag = "ol" if ordered else "ul"
            items = []
            while index < len(lines):
                current = lines[index]
                if ordered:
                    item = re.match(r"^\d+\. (.+)$", current)
                    if not item:
                        break
                    items.append(f"<li>{render_inline(item.group(1))}</li>")
                else:
                    if not current.startswith("- "):
                        break
                    items.append(f"<li>{render_inline(current[2:])}</li>")
                index += 1
            out.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        if line.startswith("> "):
            quote = []
            while index < len(lines) and lines[index].startswith("> "):
                quote.append(lines[index][2:])
                index += 1
            out.append(f"<blockquote>{render_inline(' '.join(quote))}</blockquote>")
            continue
        paragraph = []
        while index < len(lines) and lines[index].strip() and not re.match(r"^(#{1,6} |```|- |\d+\. |> )", lines[index]):
            paragraph.append(lines[index].strip())
            index += 1
        if paragraph:
            out.append(f"<p>{render_inline(' '.join(paragraph))}</p>")
        else:
            index += 1
    return "\n".join(out), headings


def layout(title, description, body, active=None, page_type=""):
    nav = "".join(
        f'<a class="nav-link {"active" if active == key else ""}" href="/subjects/{key}.html">{escape(SUBJECTS[key][0])}</a>'
        for key in SUBJECT_ORDER
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#176f5b">
  <title>{escape(title)} | Fieldnotes</title>
  <link rel="manifest" href="/manifest.webmanifest">
  <link rel="icon" href="/assets/icon-192.png" sizes="192x192" type="image/png">
  <link rel="stylesheet" href="/assets/style.css">
  <script src="/assets/app.js" defer></script>
</head>
<body class="{page_type}">
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <a class="brand" href="/">Fieldnotes<span class="brand-dot">.</span></a>
    <nav class="top-nav" aria-label="Main navigation"><a href="/">Home</a><a href="/coverage.html">Coverage</a></nav>
    <div class="header-actions"><button type="button" class="search-button" data-open-search aria-label="Search topics">Search <kbd>/</kbd></button><button type="button" class="theme-button" data-theme-toggle aria-label="Toggle color theme">Theme</button></div>
  </header>
  <div class="site-shell"><aside class="side-nav" aria-label="Subjects"><span class="side-label">LIBRARY</span>{nav}<a class="nav-link side-coverage" href="/coverage.html">Coverage</a><div class="side-foot">Made for slow, careful study.<br>Python / Java / SQL</div></aside><main id="main">{body}</main></div>
  <dialog class="search-dialog" id="search-dialog" aria-label="Search topics"><div class="search-top"><input id="search-input" type="search" placeholder="Search topics and courses" autocomplete="off" aria-label="Search topics"><button type="button" data-close-search aria-label="Close search">Esc</button></div><div id="search-results" class="search-results"></div></dialog>
  <footer class="site-footer"><span>Fieldnotes</span><span>Built from a complete topic inventory. Articles are reviewed as they are written. <a href="/privacy.html">Privacy policy</a></span></footer>
</body>
</html>"""


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build():
    topics = read_inventory()
    content_ids = set()
    for topic in topics:
        path = CONTENT / topic["subject"] / f'{topic["slug"]}.md'
        topic["ready"] = path.is_file()
        if topic["ready"]:
            content_ids.add(topic["id"])
    orphaned = [str(p.relative_to(CONTENT)) for p in CONTENT.glob("*/*.md") if f"{p.parent.name}/{p.stem}" not in content_ids]
    if orphaned:
        raise ValueError(f"Content missing from inventory: {orphaned}")
    if DIST.exists():
        if not DIST.resolve().is_relative_to(ROOT.resolve()) or DIST.resolve() == ROOT.resolve():
            raise ValueError("Refusing to remove a build directory outside the project")
        shutil.rmtree(DIST)
    (DIST / "assets").mkdir(parents=True)
    shutil.copyfile(ROOT / "site" / "style.css", DIST / "assets" / "style.css")
    shutil.copyfile(ROOT / "site" / "app.js", DIST / "assets" / "app.js")
    for size in (192, 512):
        shutil.copyfile(ROOT / "site" / f"icon-{size}.png", DIST / "assets" / f"icon-{size}.png")
    shutil.copytree(ROOT / "site" / "fonts", DIST / "assets" / "fonts")
    shutil.copyfile(ROOT / "site" / "manifest.webmanifest", DIST / "manifest.webmanifest")

    by_subject = defaultdict(list)
    for topic in topics:
        for subject in dict.fromkeys(p["subject"] for p in topic["placements"]):
            by_subject[subject].append(topic)
    for subject in SUBJECT_ORDER:
        name, summary = SUBJECTS[subject]
        entries = by_subject[subject]
        ready = sum(t["ready"] for t in entries)
        courses = list(dict.fromkeys(p["course"] for t in entries for p in t["placements"] if p["subject"] == subject))
        cards = []
        anchored = set()
        for course in courses:
            placements = [(t, p) for t in entries for p in t["placements"] if p["course"] == course and p["subject"] == subject]
            modules = defaultdict(list)
            for topic, placement in placements:
                module = placement["sections"][0] if placement["sections"] else "Other topics"
                modules[module].append((topic, placement))
            blocks = []
            for module, items in modules.items():
                rows = []
                for topic, placement in items:
                    section = " / ".join(placement["sections"][1:])
                    if topic["ready"]:
                        title = f'<a href="/topics/{topic["id"]}.html">{escape(topic["title"])}</a>'
                        state = '<span class="state ready">Read</span>'
                    else:
                        title = escape(topic["title"])
                        state = '<span class="state planned">Planned</span>'
                    anchor = ""
                    if topic["id"] not in anchored:
                        anchor = f' id="{topic["slug"]}"'
                        anchored.add(topic["id"])
                    rows.append(f'<li{anchor}><span class="topic-title">{title}<small>{escape(section)}</small></span>{state}</li>')
                blocks.append(f'<details class="module" {"open" if items[0][0]["ready"] else ""}><summary><span>{escape(module)}</span><span>{len(items)} topics</span></summary><ul class="topic-list">{"".join(rows)}</ul></details>')
            cards.append(f'<section class="course-block"><div class="section-heading"><h2>{escape(course)}</h2><span>{len(placements)} headings</span></div>{"".join(blocks)}</section>')
        intro = f'<div class="page-intro"><div class="eyebrow">SUBJECT / {escape(subject.upper())}</div><h1>{escape(name)}</h1><p>{escape(summary)}</p><div class="stat-line"><strong>{len(entries)}</strong> topics <span>/</span> <strong>{ready}</strong> articles ready <span>/</span> <strong>{len(courses)}</strong> course paths</div></div>'
        write(DIST / "subjects" / f"{subject}.html", layout(name, summary, intro + ''.join(cards), active=subject, page_type="subject-page"))

    for topic in topics:
        if not topic["ready"]:
            continue
        source = (CONTENT / topic["subject"] / f'{topic["slug"]}.md').read_text(encoding="utf-8")
        first = re.search(r"^# (.+)$", source, re.M)
        if not first or first.group(1).strip() != topic["title"]:
            raise ValueError(f"Title mismatch in {topic['id']}: expected {topic['title']}")
        article, headings = render_markdown(source)
        if len(article) < 1200:
            raise ValueError(f"Article looks incomplete: {topic['id']}")
        toc = ''.join(f'<a href="#{anchor}">{escape(label)}</a>' for level, label, anchor in headings if level == 2)
        placements = ''.join(f'<li>{escape(p["course"])} / {escape(" / ".join(p["sections"]))}</li>' for p in topic["placements"])
        subject_name = SUBJECTS[topic["subject"]][0]
        body = f'<div class="article-layout"><article class="article"><div class="breadcrumbs"><a href="/subjects/{topic["subject"]}.html">{escape(subject_name)}</a><span>/</span><span>{escape(topic["title"])}</span></div><div class="eyebrow">STUDY NOTE</div><h1>{escape(topic["title"])}</h1><div class="article-body">{article}</div><div class="article-end"><h2>Where this appears</h2><ul>{placements}</ul><a href="/subjects/{topic["subject"]}.html">Back to {escape(subject_name)}</a></div></article><aside class="on-this-page"><span>ON THIS PAGE</span>{toc}</aside></div>'
        write(DIST / "topics" / topic["subject"] / f'{topic["slug"]}.html', layout(topic["title"], f'Study note on {topic["title"]}', body, active=topic["subject"], page_type="article-page"))

    subject_cards = ''.join(f'<a class="subject-card" href="/subjects/{key}.html"><span class="subject-number">0{i + 1}</span><h2>{escape(SUBJECTS[key][0])}</h2><p>{escape(SUBJECTS[key][1])}</p><span class="card-footer">{len(by_subject[key])} topics</span></a>' for i, key in enumerate(SUBJECT_ORDER))
    home = f'<div class="hero"><div class="eyebrow">A PERSONAL STUDY LIBRARY</div><h1>Learn one idea<br><em>well.</em></h1><p>Clear notes for SQL, databases, systems, networks, and software design. Every topic from the source courses has a place here. Articles are added after careful review.</p><div class="hero-actions"><a class="primary-button" href="/subjects/sql.html">Start with SQL</a><a class="text-button" href="/coverage.html">See coverage</a></div></div><section class="home-section"><div class="section-heading"><div><div class="eyebrow">THE LIBRARY</div><h2>Choose a subject</h2></div><p>Follow a course path or search for one topic.</p></div><div class="subject-grid">{subject_cards}</div></section><section class="phone-section"><div><div class="eyebrow">ON YOUR PHONE</div><h2>Read anywhere</h2><p>Open this site in Chrome on Android. In the browser menu, tap Install app or Add to Home screen. Keep this page open until your notes are ready for offline reading.</p><p class="offline-status" data-offline-status role="status">Checking offline notes...</p></div><button type="button" class="primary-button install-button" data-install-app hidden>Install app</button></section>'
    write(DIST / "index.html", layout("Home", "A personal library for software engineering study", home, page_type="home-page"))

    total_ready = sum(t["ready"] for t in topics)
    source_count = sum(len(t["placements"]) for t in topics)
    rows = ''.join(f'<tr><th><a href="/subjects/{key}.html">{escape(SUBJECTS[key][0])}</a></th><td>{len(by_subject[key])}</td><td>{sum(t["ready"] for t in by_subject[key])}</td></tr>' for key in SUBJECT_ORDER)
    coverage = f'<div class="page-intro"><div class="eyebrow">EDITORIAL TRACKER</div><h1>Coverage</h1><p>The source inventory is complete. Each heading remains visible while its article is researched and written. Repeated headings point to one shared article.</p><div class="stat-line"><strong>{source_count}</strong> source headings <span>/</span> <strong>{len(topics)}</strong> unique pages <span>/</span> <strong>{total_ready}</strong> articles ready</div></div><div class="coverage-table"><table><thead><tr><th>Subject</th><th>Topics</th><th>Articles ready</th></tr></thead><tbody>{rows}</tbody></table></div>'
    write(DIST / "coverage.html", layout("Coverage", "Editorial coverage of every included topic", coverage, page_type="coverage-page"))
    privacy = '<div class="page-intro"><div class="eyebrow">ABOUT THIS APP</div><h1>Privacy and safety</h1><p>Fieldnotes is a reading site. You can install it from your browser and save the finished notes for offline use.</p></div><div class="privacy-copy"><h2>What stays on your device</h2><p>Search runs in your browser. The words you type into search are not sent to this site. Your color theme is saved in your browser. The offline copy stores pages, fonts, and icons on your device. You can remove the saved data in your browser\'s site settings.</p><h2>What the host receives</h2><p>The web host receives normal requests when you open pages online. Fieldnotes has no account, ads, or analytics code. It does not ask for camera, location, or microphone access.</p><h2>Links and updates</h2><p>References in the notes may open other websites. Those sites have their own rules. The offline copy updates when you return online and open Fieldnotes again.</p><h2>Check the source</h2><p>The <a href="https://github.com/Diafyx/cs-fieldnotes">source code is public</a>. You can see how the pages and offline copy are made.</p></div>'
    privacy = privacy.replace('<h1>Privacy and safety</h1>', '<h1>Privacy policy</h1>')
    privacy = privacy.replace('Fieldnotes is a reading site. You can install it from your browser and save the finished notes for offline use.', 'Fieldnotes is a study website and a standalone Android reading app. Both let you read finished notes offline.')
    privacy = privacy.replace('<h2>Check the source</h2>', '<h2>Standalone Android app</h2><p>The Android app includes the finished notes, search list, fonts, and icons. It does not ask for internet access, and it does not send search words or other user data to Fieldnotes. Your color theme stays on your device until you clear the app data or uninstall the app. The app has no account, ads, or analytics. Reference links open in your browser, which has its own privacy rules.</p><h2>Data retention and deletion</h2><p>Fieldnotes does not store Android app search words, theme choices, or reading history on a server. To remove the app data kept on your device, clear Fieldnotes storage in Android settings or uninstall the app. For the website, clear Fieldnotes site data in your browser. The web host may keep normal request logs under its own policy.</p><h2>Privacy questions</h2><p>Fieldnotes is maintained by the Diafyx project. You can ask a privacy question through <a href="https://github.com/Diafyx/cs-fieldnotes/issues">Fieldnotes GitHub Issues</a>.</p><h2>Check the source</h2>')
    write(DIST / "privacy.html", layout("Privacy policy", "How Fieldnotes stores notes and handles your data", privacy, page_type="privacy-page"))
    search_data = []
    for topic in topics:
        placement = next(p for p in topic["placements"] if p["subject"] == topic["subject"])
        search_data.append({
            "title": topic["title"],
            "subject": topic["subject"],
            "course": placement["course"],
            "url": f'/topics/{topic["id"]}.html' if topic["ready"] else f'/subjects/{topic["subject"]}.html#{topic["slug"]}',
            "ready": topic["ready"],
        })
    write(DIST / "catalog.json", json.dumps(search_data, ensure_ascii=False, separators=(",", ":")))
    offline_files = {}
    for path in sorted(DIST.rglob("*")):
        if path.is_file() and path.suffix in (".html", ".css", ".js", ".json", ".webmanifest"):
            offline_files["/" + path.relative_to(DIST).as_posix()] = path.read_text(encoding="utf-8")
    offline_files["/"] = offline_files["/index.html"]
    pack = json.dumps(offline_files, ensure_ascii=False, separators=(",", ":"))
    write(DIST / "offline-pack.json", pack)
    pack_bytes = pack.encode("utf-8")
    binary_data = {url: (DIST / url.lstrip("/")).read_bytes() for url in BINARY_ASSETS}
    asset_hashes = {url: hashlib.sha256(data).hexdigest() for url, data in binary_data.items()}
    version = hashlib.sha256(pack_bytes + b"".join(binary_data.values())).hexdigest()[:16]
    worker = (ROOT / "site" / "sw.js").read_text(encoding="utf-8")
    worker = worker.replace("__CACHE_VERSION__", version).replace("__PACK_SHA256__", hashlib.sha256(pack_bytes).hexdigest())
    worker = worker.replace("__ASSET_HASHES__", json.dumps(asset_hashes, separators=(",", ":"))).replace("__CSP__", json.dumps(CSP))
    write(DIST / "sw.js", worker)
    headers = f"/*\n  Content-Security-Policy: {CSP}\n  X-Content-Type-Options: nosniff\n  X-Frame-Options: DENY\n  Referrer-Policy: no-referrer\n  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()\n\n/sw.js\n  Cache-Control: no-cache\n\n/offline-pack.json\n  Cache-Control: no-cache\n"
    write(DIST / "_headers", headers)
    print(f"Built {len(topics)} unique topics from {source_count} source headings; {total_ready} articles ready.")


if __name__ == "__main__":
    build()
