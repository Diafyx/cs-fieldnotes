"""Check the Google Play listing files and built Android artifacts."""

import argparse
import json
import re
import struct
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / ".android-tools"
ASSETS = ROOT / "android/app/src/main/assets"
POLICY_URL = "https://fieldnotes-15h.pages.dev/privacy"
PACKAGE = "org.diafyx.fieldnotes"
UPLOAD_CERT = "2072ef88ab6be2055dd154366e5458c0a3647a511b10ac7aca8d1ff5ff14df28"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def png_info(path):
    with path.open("rb") as stream:
        header = stream.read(26)
    require(header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR", f"Not a PNG: {path}")
    width, height, depth, color = struct.unpack(">IIBB", header[16:26])
    return width, height, depth, color


def jpeg_info(path):
    data = path.read_bytes()
    require(data[:2] == b"\xff\xd8", f"Not a JPEG: {path}")
    offset = 2
    while offset + 4 < len(data):
        require(data[offset] == 0xFF, f"Broken JPEG marker: {path}")
        while data[offset] == 0xFF:
            offset += 1
        marker = data[offset]
        offset += 1
        if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
            continue
        length = int.from_bytes(data[offset:offset + 2], "big")
        require(length >= 2 and offset + length <= len(data), f"Broken JPEG segment: {path}")
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height = int.from_bytes(data[offset + 3:offset + 5], "big")
            width = int.from_bytes(data[offset + 5:offset + 7], "big")
            components = data[offset + 7]
            require(components == 3, f"Screenshot JPEG must have three color channels: {path}")
            return width, height
        offset += length
    raise ValueError(f"JPEG dimensions not found: {path}")


def version_info():
    text = (ROOT / "android/app/build.gradle").read_text(encoding="utf-8")
    values = {}
    patterns = {
        "package": r"(?m)^\s*applicationId '([^']+)'\s*$",
        "code": r"(?m)^\s*versionCode (\d+)\s*$",
        "name": r"(?m)^\s*versionName '([^']+)'\s*$",
        "target": r"(?m)^\s*targetSdk (\d+)\s*$",
        "min": r"(?m)^\s*minSdk (\d+)\s*$",
    }
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        require(len(matches) == 1, f"Expected one {key} in android/app/build.gradle")
        values[key] = matches[0]
    require(values["package"] == PACKAGE, "Android package name changed")
    require(int(values["code"]) > 0, "Version code must be positive")
    require(int(values["target"]) >= 36, "Target SDK is below the current Play phone app minimum, API 36")
    require(int(values["min"]) <= int(values["target"]), "Minimum SDK exceeds target SDK")
    return values


def check_store_files(version, submission):
    icon = ROOT / "play-store/icon.png"
    feature = ROOT / "play-store/feature.png"
    require(icon.is_file() and feature.is_file(), "Store icon or feature graphic is missing")
    require(png_info(icon) == (512, 512, 8, 6), "Store icon must be a 512 by 512, 32-bit PNG")
    require(icon.stat().st_size <= 1024 * 1024, "Store icon exceeds 1024 KB")
    require(png_info(feature) == (1024, 500, 8, 2), "Feature graphic must be a 1024 by 500, 24-bit PNG")

    guide = (ROOT / "PLAY_STORE.md").read_text(encoding="utf-8")
    name = re.search(r"(?m)^\*\*Name:\*\* (.+)$", guide)
    short = re.search(r"(?m)^\*\*Short description:\*\* (.+)$", guide)
    full = re.search(r"(?s)\*\*Full description:\*\*\s*\n\n(.*?)\n\n## ", guide)
    require(name and len(name.group(1)) <= 30, "Store name is missing or longer than 30 characters")
    require(short and len(short.group(1)) <= 80, "Short description is missing or longer than 80 characters")
    require(full and 1 <= len(full.group(1)) <= 4000, "Full description is missing or longer than 4000 characters")

    notes = ROOT / "play-store/release-notes" / f'{version["code"]}.txt'
    require(notes.is_file(), f"Release notes are missing: {notes}")
    note = notes.read_text(encoding="utf-8").strip()
    require(1 <= len(note) <= 500, "Release notes must contain 1 to 500 characters")

    privacy = ROOT / "dist/privacy.html"
    require(privacy.is_file(), "Build the site before checking the Play listing")
    html = privacy.read_text(encoding="utf-8")
    for expected in ("Privacy policy", "Standalone Android app", "Data retention and deletion",
                     "GitHub Issues", "does not ask for internet access"):
        require(expected in html, f"Local privacy page is missing: {expected}")

    screenshots = []
    folder = ROOT / "play-store/screenshots"
    if folder.exists():
        screenshots = sorted(path for path in folder.iterdir() if path.suffix.lower() in (".png", ".jpg", ".jpeg"))
    for path in screenshots:
        if path.suffix.lower() == ".png":
            width, height, depth, color = png_info(path)
            require((depth, color) == (8, 2), f"Screenshot must be a 24-bit PNG without alpha: {path}")
        else:
            width, height = jpeg_info(path)
        require(320 <= min(width, height) and max(width, height) <= 3840,
                f"Screenshot dimensions are outside Play limits: {path}")
        require(max(width, height) <= 2 * min(width, height), f"Screenshot is too long for its width: {path}")
    if submission:
        require(len(screenshots) >= 2, "Add at least two real app screenshots to play-store/screenshots")
    return len(screenshots)


def check_apk(path, version, owner_key):
    require(path.is_file(), f"APK is missing: {path}")
    expected_assets = {"assets/" + item.relative_to(ASSETS).as_posix(): item
                       for item in ASSETS.rglob("*") if item.is_file()}
    require(expected_assets, "Bundled Android pages are missing")
    with zipfile.ZipFile(path) as apk:
        require(apk.testzip() is None, "APK contains a damaged ZIP entry")
        entries = set(apk.namelist())
        missing = set(expected_assets) - entries
        require(not missing, f"APK is missing {len(missing)} local asset files")
        for name, source in expected_assets.items():
            require(apk.read(name) == source.read_bytes(), f"APK has stale content: {name}")
        require("assets/sw.js" not in entries, "Web service worker was packed into Android")
    build_tools = TOOLS / "android-sdk/build-tools/36.0.0"
    aapt = build_tools / "aapt.exe"
    signer = build_tools / "lib/apksigner.jar"
    jdk = next((item for item in (TOOLS / "jdk17").iterdir() if item.is_dir()), None)
    require(jdk is not None, "Local JDK 17 is missing")
    java = jdk / "bin/java.exe"
    require(aapt.is_file() and signer.is_file() and java.is_file(), "Local Android build tools are missing")
    badging = subprocess.run([str(aapt), "dump", "badging", str(path)], capture_output=True, text=True, check=True).stdout
    package = re.search(r"(?m)^package: name='([^']+)' versionCode='([^']+)' versionName='([^']+)'", badging)
    require(package and package.groups() == (PACKAGE, version["code"], version["name"]),
            "Built APK package or version differs from android/app/build.gradle")
    permissions = subprocess.run([str(aapt), "dump", "permissions", str(path)], capture_output=True, text=True, check=True).stdout
    require(not re.search(r"(?m)^uses-permission", permissions), "Built APK requests an Android permission")
    signed = subprocess.run([str(java), "-jar", str(signer), "verify", "--print-certs", str(path)],
                            capture_output=True, text=True, check=True).stdout
    if owner_key:
        match = re.search(r"Signer #1 certificate SHA-256 digest: ([0-9a-fA-F]{64})", signed)
        require(match and match.group(1).lower() == UPLOAD_CERT, "APK uses the wrong upload key")


def check_bundle(path, owner_key):
    require(path.is_file(), f"App bundle is missing: {path}")
    expected = {"base/assets/" + item.relative_to(ASSETS).as_posix(): item for item in ASSETS.rglob("*") if item.is_file()}
    require(expected, "Bundled Android pages are missing")
    with zipfile.ZipFile(path) as bundle:
        require(bundle.testzip() is None, "App bundle contains a damaged ZIP entry")
        entries = set(bundle.namelist())
        require("base/manifest/AndroidManifest.xml" in entries, "App bundle has no base manifest")
        missing = set(expected) - entries
        require(not missing, f"App bundle is missing {len(missing)} local asset files")
        for name, source in expected.items():
            require(bundle.read(name) == source.read_bytes(), f"App bundle has stale content: {name}")
        require("base/assets/sw.js" not in entries, "Web service worker was packed into Android")
    jdk = next((item for item in (TOOLS / "jdk17").iterdir() if item.is_dir()), None)
    require(jdk is not None, "Local JDK 17 is missing")
    jarsigner = jdk / "bin/jarsigner.exe"
    verified = subprocess.run([str(jarsigner), "-verify", str(path)], capture_output=True, text=True)
    require(verified.returncode == 0 and "jar verified" in verified.stdout, "App bundle signature is invalid")
    if owner_key:
        keytool = jdk / "bin/keytool.exe"
        cert = subprocess.run([str(keytool), "-printcert", "-jarfile", str(path)], capture_output=True, text=True, check=True).stdout
        fingerprint = re.search(r"SHA256:\s*([0-9A-Fa-f:]{95})", cert)
        require(fingerprint and fingerprint.group(1).replace(":", "").lower() == UPLOAD_CERT,
                "App bundle uses the wrong upload key")
    return len(expected)


def check_live_privacy():
    request = urllib.request.Request(POLICY_URL, headers={"User-Agent": "Fieldnotes release check"})
    with urllib.request.urlopen(request, timeout=20) as response:
        require(response.status == 200, f"Privacy page returned HTTP {response.status}")
        text = response.read().decode("utf-8")
    require("Standalone Android app" in text and "Data retention and deletion" in text
            and "up to five recent searches" in text and "GitHub Issues" in text,
            "Public privacy page is still the old version. Publish the latest site first.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apk", type=Path, help="APK to inspect")
    parser.add_argument("--bundle", type=Path, help="AAB to inspect")
    parser.add_argument("--owner-key", action="store_true", help="Require the real Fieldnotes upload key")
    parser.add_argument("--submission", action="store_true", help="Require screenshots and the live privacy policy")
    parser.add_argument("--live", action="store_true", help="Check the public privacy page")
    parser.add_argument("--support-email", help="Public email entered in Play Console")
    args = parser.parse_args()
    require(not args.owner_key or (args.apk and args.bundle), "Owner key check needs both --apk and --bundle")
    version = version_info()
    count = check_store_files(version, args.submission)
    if args.submission:
        require(args.support_email and re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", args.support_email),
                "Pass the public Play support email with --support-email")
    if args.submission or args.live:
        check_live_privacy()
    if args.apk:
        check_apk(args.apk, version, args.owner_key)
    assets = check_bundle(args.bundle, args.owner_key) if args.bundle else 0
    print(f'Play checks passed for {version["name"]} ({version["code"]}): '
          f'{count} screenshots, {assets} verified AAB assets.')
    if not args.submission and not args.live:
        print("For submission, add screenshots and run again with --submission --support-email YOUR_EMAIL.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        print(f"Play check failed: {error}", file=sys.stderr)
        sys.exit(1)
