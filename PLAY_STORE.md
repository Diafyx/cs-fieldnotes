# Publish Fieldnotes on Google Play

Fieldnotes is not on Google Play yet. The Android app reads its own bundled pages. It works offline and asks for no Android permissions. The website and app use the same articles. The app gets new articles only through an app update.

The Android package is `org.diafyx.fieldnotes`. The first Play upload uses version `1.0.5`, code `6`. The current project has 334 finished articles. Run the tests again after each content change so the uploaded bundle matches the latest articles. Google Play requires API 36 for new phone apps in 2026; this app targets API 36.

## Finish these items before submitting

1. Publish the latest site. `https://fieldnotes-15h.pages.dev/privacy` must say that up to five recent searches stay on the device. Run `python scripts/check_play_store.py --live` after your Cloudflare deployment. Do not enter the old policy in Play Console.
2. Choose a public support email that you can read. Play shows it on the listing. Use that same address when running the submission check. Do not use the release key password as part of any email or form.
3. Install the current app on a phone and take at least two real screenshots. Save them in `play-store/screenshots/`. Read [screenshots/README.md](play-store/screenshots/README.md) for the suggested screens. The store icon and feature image are already in `play-store/`.
4. Back up `.android-tools/signing/fieldnotes-release.jks` and its password privately. They are the upload key for future versions. Never put them in Git or send the password to anyone.

## Run the local tests

From the `tuf-study` directory in PowerShell:

```powershell
.\scripts\test_play_ready.ps1
```

This builds the site and Android pages, runs the content checks, runs Android lint, builds a debug APK and bundle, checks the package, version, permissions, signature, and bundled files, and opens the pages in a phone-sized browser at four widths. The debug bundle is only for tests. Do not upload it to Play.

For a wider check, run `.\scripts\test_play_ready.ps1 -DeepAudit`. This visits every bundled page at 320px and 390px, checks for page errors, missing images, horizontal overflow, small controls, and external requests, and tests Back and module state on all six subjects. Read `.mobile-test/audit/audit.md` afterward. It also saves sample screenshots there. The submission check runs this audit too.

The browser test uses Node.js and Playwright. This computer already has them under the ignored `.mobile-test/` folder. On another computer, install Node.js 20 or newer and run `.\scripts\setup_play_tests.ps1` once. It downloads the test browser into `.mobile-test/`. The local Android build also needs Python, JDK 17, Android SDK Platform 36, Build Tools 36.0.0, and Gradle 9.6.0 in `.android-tools/` on this computer.

After the public privacy page, screenshots, and support email are ready, run:

```powershell
.\scripts\test_play_ready.ps1 -Submission -SupportEmail you@example.com
```

The submission check checks the live privacy page and store images as well. It cannot judge whether a screenshot looks good or whether a Play Console form was answered honestly. Review those yourself.

## Build the signed Play file

For the first upload, run:

```powershell
.\scripts\prepare_play_release.ps1 -UseCurrentVersion
```

Enter the release key password in your own terminal. The script builds and verifies the signed APK and AAB. It checks that the bundle contains the current articles and that both files use the expected upload key. It saves the upload file at `.android-tools/play-releases/6-1.0.5/fieldnotes.aab` and the notes at `release-notes.txt` in the same folder. **Upload the AAB, not the APK.** The older `5-1.0.4` release does not include the subject menu fix. Do not upload or use it for screenshots.

If the signed build finished but archiving stopped later, run `.\scripts\prepare_play_release.ps1 -UseCurrentVersion -ArchiveExisting`. This checks both existing files, their bundled pages, and their signatures before saving the release folder. It does not ask for the key password again.

The local release key has SHA-256 fingerprint `2072ef88ab6be2055dd154366e5458c0a3647a511b10ac7aca8d1ff5ff14df28`. Let Google create the Play App Signing key when the Console asks. Google will use our key as the upload key. An app installed from Play has a different signature from a directly installed release APK. Uninstall a directly installed copy before installing the Play test version. This clears the saved theme and recent searches.

## Create the app in Play Console

1. Open [Play Console](https://play.google.com/console/), choose **Home**, then **Create app**.
2. Choose **English (United States)** as the default language, unless you want another English locale. Enter **Fieldnotes** as the app name. Choose **App** and **Free**.
3. Enter your public support email. Read and accept the developer policy, export law, and Play App Signing declarations. Choose **Create app**.
4. Open the app's **Dashboard**. Complete its setup tasks. The Console can add tasks based on your account and app, so use the dashboard as the final list.

The package name `org.diafyx.fieldnotes` comes from the first AAB you upload. Check it before accepting the upload. You cannot change the package name for that Play app later.

## Fill in the store listing

In **Grow users > Store presence > Main store listing**, enter the text below. In **Store settings**, choose the **Education** category and suitable tags. Add your public support email and the website `https://fieldnotes-15h.pages.dev/`. Choose the countries and regions where you want the app available. The Console may place these fields in a different order.

**Name:** Fieldnotes

**Short description:** Offline notes for SQL, databases, operating systems, networks, and design

**Full description:**

Fieldnotes is a study library for SQL, databases, operating systems, computer networks, object-oriented programming, and low-level design.

Read finished articles without an internet connection. Browse by subject or search for a topic. Each note uses plain English, examples, practice questions, and references. Topics that still need an article are marked as planned.

The app has no account, ads, or analytics. Its articles and search list are included with the app. New articles arrive when you install an update. Reference links open in your browser.

Upload `play-store/icon.png` as the app icon, `play-store/feature.png` as the feature graphic, and the real phone screenshots from `play-store/screenshots/`. Google requires at least two phone screenshots. Four clear portrait screenshots at 1080 by 1920 or higher help the listing qualify for more places on Play. Do not use a screenshot from the website if the app looks different.

## Complete App content

Open **Policy and programs > App content**, or use each dashboard task. Check every answer against the version you upload. For this code, the expected answers are:

| Form | Answer to check |
| --- | --- |
| Privacy policy | `https://fieldnotes-15h.pages.dev/privacy` after the new page is live |
| App access | All content is available without sign-in, payment, or a special account |
| Ads | No ads |
| Data safety | The app itself collects and shares no user data; confirm every question in the form |
| Target audience | Choose the age groups you truly intend to serve. The app is a general study guide; do not claim it is made for children unless you plan for those rules |
| Content rating | Complete the questionnaire with the actual study content |
| Financial features | None |
| Health features | None |
| News or government | No, based on the current app |
| Advertising ID | No, based on the current app |

The app has no `INTERNET` permission, account, ads, analytics, or app data upload. Search and theme choice stay on the device. Tapping a reference opens the phone's browser, which is a separate app. Check any new library or feature before reusing these answers in a later release. The privacy policy must be public and must also be reachable inside the app; both are checked locally and in the browser test.

## Test through Google Play

1. Go to **Test and release > Testing**. If this is a new **personal** developer account created after 13 November 2023, start a **Closed testing** track. Google requires at least 12 testers opted in continuously for 14 days before you can apply for production access. Add testers by email or Google Group and give them the opt-in link after the track is published. If this is an **organization** account, use **Internal testing** first, then move to production when the app is ready. The Console will show any account-specific rule.
2. Create a release on the chosen track. Upload `.android-tools/play-releases/6-1.0.5/fieldnotes.aab`. Choose the Google-generated app signing key if asked. Paste `play-store/release-notes/6.txt` as the release notes. Review errors and warnings, then roll out the test release. Use **Publishing overview > Send for review** if the Console asks.
3. Wait for the test link or Play Store URL to work. Install from Play on a real phone. If a directly installed APK is already there, uninstall it first because Play uses a different signing key.
4. Test home, every subject, search, one finished article, a planned topic, theme change, back navigation from a scrolled page, offline reading in airplane mode, reference links, and the in-app privacy page. Check both light and dark themes. Record any problems and fix them before a public release.
5. Open **Test and release > Testing > Pre-launch report > Overview**. Google runs this after an upload, subject to test lab capacity. Review crashes, compatibility, performance, accessibility, and screenshots. Fix serious findings and upload a new version if needed.

The local browser suite does not run Android WebView on a real device. The Play test and pre-launch report cover that gap. They can still miss problems, so keep the real phone check.

## Publish

For a new personal account, finish the closed test and apply for production access from the Dashboard. Wait for approval. For an organization account, continue after the Play test and report are clean. In **Test and release > Production**, create the first release or promote the tested one if the Console offers it. Confirm the same AAB version, countries, listing, privacy policy, and App content forms. Review the release and submit it. Check **Publishing overview** for any final **Send for review** step. Watch the review status and answer any request from Google. The app is public only after Google approves and publishes it.

## Publish later updates

Write the new notes in `play-store/release-notes/7.txt`. Run the full local suite again. Build the next signed release with:

```powershell
.\scripts\prepare_play_release.ps1 -VersionName 1.0.6
```

This raises the version code to `7`, saves a new release folder, and stops if the notes are missing or the version would go backward. Use a higher version code for every later Play upload. Review the Data safety answers and screenshots again if the app changes. Run the submission suite, test the Play release, and only then move it to production. The signed files and key stay in ignored folders. You run any Git commands yourself.

## Official help

- [Create and set up an app](https://support.google.com/googleplay/android-developer/answer/9859152)
- [Set up the app dashboard](https://support.google.com/googleplay/android-developer/answer/9859454)
- [Target API requirement](https://developer.android.com/google/play/requirements/target-sdk)
- [Store images and screenshots](https://support.google.com/googleplay/android-developer/answer/9866151)
- [Prepare App content for review](https://support.google.com/googleplay/android-developer/answer/9859455)
- [Data safety form](https://support.google.com/googleplay/android-developer/answer/10787469)
- [Closed test rule for new personal accounts](https://support.google.com/googleplay/android-developer/answer/14151465)
- [Set up a test](https://support.google.com/googleplay/android-developer/answer/9845334)
- [Pre-launch report](https://support.google.com/googleplay/android-developer/answer/9842757)
- [Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756)
