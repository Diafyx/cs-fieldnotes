# Fieldnotes

Fieldnotes is a personal study site for SQL, DBMS, operating systems, computer networks, object-oriented programming, and low-level design. The site is built from Markdown and plain Python. It has no package installation step.

## Run it locally

From this directory:

```text
python build.py
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000` in a browser. Stop the server with `Ctrl+C`. Run `python build.py` again after editing a note.

## Install the website on Android

Open the deployed site in Chrome on your Android phone. Open the browser menu and tap **Install app** or **Add to Home screen**. You may also see an **Install app** button on the site's home page.

Keep the site open until it says **Notes ready for offline reading**. The first download saves the finished articles, subject pages, search catalog, and site layout. Planned topics stay visible, but they have no article yet. Open the site online after new notes are published to update the offline copy. An installed web app needs no Android Studio, APK, or Play Store account.

The offline copy is made by `build.py` from the same files as the website. `site/manifest.webmanifest` sets the app name and icons. `site/sw.js` saves the generated pages. `scripts/make_icons.py` recreates the PNG icons with Python if they need to change. Run `python scripts/check_pwa.py` after a build to check the offline copy.

The site uses no accounts, analytics, or external scripts. Its fonts are stored in `site/fonts` and are covered by the license files there. Cloudflare Pages reads the generated `dist/_headers` file to apply the site's security headers. The offline copy checks its download before it replaces an older saved version.

## Build the standalone Android app

The `android/` project makes an APK with the finished notes inside it. It reads local pages and does not request internet access. Search, subject pages, and finished articles work without Cloudflare. Reference links can open in a separate browser if you choose to tap them. New notes reach the APK only when you install a new version.

You need Python 3.9 or newer, JDK 17, Android SDK Platform 36, and Android SDK Build Tools 36.0.0. The Gradle wrapper is included. From this directory, run:

```text
python scripts/prepare_android.py
python scripts/check_android.py
cd android
.\gradlew.bat assembleDebug
```

The test APK is `android/app/build/outputs/apk/debug/app-debug.apk`. Copy it to your phone and install it for your own testing. Android may ask you to allow installs from the app you used to open the APK. The website and the APK store their theme choices separately.

The files in `android/app/src/main/assets/` are made from the same Markdown as the website. They are ignored by Git and rebuilt before each Android build. The Android bundle leaves out the browser install code and service worker. Run `python scripts/check_android.py` after preparing it to check that every local link resolves and all finished articles are present.

Before sharing an APK with other people, make a signed release build. Keep its signing key private and back it up. Android uses that same key to check future updates. Increase `versionCode` in `android/app/build.gradle` for each release. A debug APK is for testing, not public distribution.

On this Windows workspace, run `.\scripts\release_android.ps1 -CreateKey` once from the project directory. The JDK asks you for a password. The key stays in the ignored `.android-tools/signing/` directory. Back up the key and its password somewhere safe before sharing any release APK. Do not send the password to anyone or put it in a tracked file.

Run `.\scripts\release_android.ps1` to build the signed APK and the Google Play app bundle. It asks for the password in your terminal, runs Android lint, checks the signatures and APK permissions, and prints SHA-256 hashes. The installable APK is `android/app/build/outputs/apk/release/app-release.apk`. The Play Store upload file is `android/app/build/outputs/bundle/release/app-release.aab`. The script uses only the toolchain and build folders inside this project. If your phone has the debug APK, uninstall that test app before installing the release APK. Android treats the two signing keys as different, so one cannot update the other. Your theme choice will reset when you uninstall the debug app.

The app is not published on Google Play by building these files. Run `.\scripts\test_play_ready.ps1` before each Play release. See `PLAY_STORE.md` for the signed upload file, store listing, testing, and Play Console steps. The owner creates and submits the Play listing. Do not upload the private `.jks` key or share its password.

## How the content is organized

- `source-topics.md` is the course inventory for this site. It contains the included subjects and leaves out DSA and C++.
- `content/<subject>/<topic>.md` holds reviewed articles. Each file starts with the exact topic heading.
- `build.py` maps every included heading to a page. An exact title repeated in several courses uses one article. SQL topics repeated in DBMS also use one article.
- `dist/` is the generated static site. It can be served by any host that serves plain files.
- `scripts/check.py` checks inventory counts, generated links, duplicate HTML IDs, and the writing rules.

The subject pages list every heading, including those that still need an article. Planned headings are clearly marked. The coverage page shows how many articles are ready. This keeps gaps visible while the writing continues.

## Writing a new article

1. Find the exact title in `source-topics.md`.
2. Find its generated slug in `dist/catalog.json` or use the lowercase words joined with hyphens.
3. Add `content/<subject>/<slug>.md` with that exact title as the first heading.
4. Follow `CONTENT_GUIDE.md`.
5. Run `python build.py`, then run every `scripts/check*.py` file. Each checker reports what it verified.

The site uses PostgreSQL for SQL examples unless an article says otherwise. Python and Java are the application languages used in examples. No C++ examples are planned.

## Deploy with GitHub and Cloudflare Pages

Make this `tuf-study` directory the root of a new GitHub repository. Create an empty repository on GitHub first. Leave its README, license, and `.gitignore` options unchecked because this directory already has a README and `.gitignore`.

Run the Git commands yourself from this directory. The first push should go to the repository's `main` branch. Then, in Cloudflare, open **Workers & Pages**, create a **Pages** application, and import the GitHub repository. Use these settings:

| Setting | Value |
| --- | --- |
| Production branch | `main` |
| Framework preset | `None` |
| Root directory | Leave blank |
| Build command | `python3 build.py` |
| Build output directory | `dist` |

Cloudflare builds `dist/` from the source files on each push. The generated directory is ignored by Git. There are no package dependencies to install.
