// Visit every bundled page and write a mobile UI audit report.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const playwrightPath = path.join(root, '.mobile-test', 'node_modules', 'playwright');
if (!fs.existsSync(playwrightPath)) {
  throw new Error('Playwright is missing. Run scripts/setup_play_tests.ps1 first.');
}
const { chromium } = require(playwrightPath);
const assets = path.join(root, 'android', 'app', 'src', 'main', 'assets');
const reportDir = path.join(root, '.mobile-test', 'audit');
const shotDir = path.join(reportDir, 'screenshots');
const origin = 'https://appassets.androidplatform.net';
const widths = [320, 390];
const types = {
  '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.png': 'image/png', '.ttf': 'font/ttf'
};
const csp = "default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data:; connect-src 'self'; manifest-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'";

function pagesUnder(folder, prefix = '') {
  return fs.readdirSync(folder, { withFileTypes: true }).flatMap(entry => {
    const name = path.posix.join(prefix, entry.name);
    if (entry.isDirectory()) return pagesUnder(path.join(folder, entry.name), name);
    return entry.isFile() && name.endsWith('.html') ? [name] : [];
  });
}

function markdownCell(value) {
  return String(value).replaceAll('|', '\\|').replaceAll('\n', ' ');
}

async function main() {
  const pages = pagesUnder(assets).sort();
  assert(pages.length > 0, 'Prepare the Android pages before running the audit');
  const gradle = fs.readFileSync(path.join(root, 'android', 'app', 'build.gradle'), 'utf8');
  const appVersion = gradle.match(/versionName '([^']+)'/)?.[1];
  const versionCode = gradle.match(/versionCode (\d+)/)?.[1];
  assert(appVersion && versionCode, 'Android app version is missing');
  fs.mkdirSync(shotDir, { recursive: true });
  const issues = [];
  const results = [];
  const samples = [];
  const journeys = [];
  const started = new Date();
  const browser = await chromium.launch({ headless: true });
  try {
    for (const width of widths) {
      const context = await browser.newContext({
        viewport: { width, height: 800 }, isMobile: true, hasTouch: true,
        serviceWorkers: 'block'
      });
      await context.route('**/*', async route => {
        const url = new URL(route.request().url());
        if (url.origin !== origin) {
          issues.push({ severity: 'error', width, page: url.pathname,
            message: `External request: ${url.origin}` });
          return route.abort();
        }
        if (url.pathname.startsWith('/__app_theme__/')) {
          return route.fulfill({ status: 204, body: '' });
        }
        const filename = path.resolve(assets, '.' + (url.pathname === '/' ? '/index.html' : url.pathname));
        if (!filename.startsWith(assets + path.sep) || !fs.existsSync(filename)) {
          return route.fulfill({ status: 404, body: 'Not Found' });
        }
        return route.fulfill({
          status: 200, body: fs.readFileSync(filename),
          contentType: types[path.extname(filename)] || 'application/octet-stream',
          headers: { 'content-security-policy': csp, 'x-content-type-options': 'nosniff' }
        });
      });

      const page = await context.newPage();
      let activePage = '';
      page.on('pageerror', error => issues.push({ severity: 'error', width, page: activePage,
        message: `JavaScript error: ${error.message}` }));
      page.on('console', message => {
        if (message.type() === 'error') issues.push({ severity: 'error', width, page: activePage,
          message: `Browser console: ${message.text()}` });
      });

      for (const [index, name] of pages.entries()) {
        activePage = name;
        const before = issues.length;
        try {
          const response = await page.goto(`${origin}/${name}`, { waitUntil: 'load', timeout: 15000 });
          assert(response && response.status() === 200, `HTTP ${response?.status() || 'no response'}`);
          const view = await page.evaluate(() => {
            const visible = element => element.getClientRects().length > 0;
            const headings = [...document.querySelectorAll('h1')].filter(visible);
            const brokenImages = [...document.images].filter(image => !image.complete || image.naturalWidth === 0)
              .map(image => image.getAttribute('src'));
            const smallControls = [...document.querySelectorAll('button, summary')]
              .filter(visible)
              .filter(element => {
                const box = element.getBoundingClientRect();
                return box.width < 24 || box.height < 24;
              })
              .map(element => element.getAttribute('aria-label') || element.textContent.trim().slice(0, 50));
            const subjectNav = document.querySelector('.side-nav');
            const selectedSubject = subjectNav?.querySelector('.nav-link.active');
            const navBox = subjectNav?.getBoundingClientRect();
            const selectedBox = selectedSubject?.getBoundingClientRect();
            return {
              title: document.title,
              headings: headings.map(heading => heading.textContent.trim()),
              pageWidth: document.documentElement.scrollWidth,
              viewportWidth: innerWidth,
              brokenImages,
              smallControls,
              selectedSubjectVisible: selectedBox
                ? selectedBox.left >= navBox.left - 1 && selectedBox.right <= navBox.right + 1
                : null
            };
          });
          results.push({ page: name, width, ...view });
          if (view.headings.length !== 1) issues.push({ severity: 'error', width, page: name,
            message: `Expected one visible page heading, found ${view.headings.length}` });
          if (view.pageWidth > view.viewportWidth + 1) issues.push({ severity: 'error', width, page: name,
            message: `Page is ${view.pageWidth}px wide in a ${view.viewportWidth}px viewport` });
          if (view.selectedSubjectVisible === false) issues.push({ severity: 'error', width, page: name,
            message: 'Selected subject is outside the visible menu' });
          for (const src of view.brokenImages) issues.push({ severity: 'error', width, page: name,
            message: `Image did not load: ${src}` });
          for (const label of view.smallControls) issues.push({ severity: 'warning', width, page: name,
            message: `Control smaller than 24px: ${label}` });

          if (width === 390 && (name === 'index.html' || name.startsWith('subjects/'))) {
            const shot = `screenshots/${name.replaceAll('/', '_').replace('.html', '')}-390.png`;
            await page.screenshot({ path: path.join(reportDir, shot), fullPage: false });
            samples.push(shot);
          }
          if (issues.length > before && samples.length < 30) {
            const shot = `screenshots/issue-${name.replaceAll('/', '_').replace('.html', '')}-${width}.png`;
            await page.screenshot({ path: path.join(reportDir, shot), fullPage: false });
            samples.push(shot);
          }
        } catch (error) {
          issues.push({ severity: 'error', width, page: name, message: `Page audit failed: ${error.message}` });
        }
        if ((index + 1) % 50 === 0 || index + 1 === pages.length) {
          console.log(`Audited ${index + 1}/${pages.length} pages at ${width}px`);
        }
      }

      if (width === 390) {
        for (const subject of ['sql', 'dbms', 'os', 'networks', 'oop', 'lld']) {
          activePage = `subjects/${subject}.html`;
          try {
            await page.goto(`${origin}/${activePage}`);
            const modules = page.locator('details.module');
            const count = await modules.count();
            assert(count > 0, 'No modules on subject page');
            const first = modules.first();
            const original = await first.evaluate(element => element.open);
            await first.locator('summary').click();
            const changed = !original;
            await page.reload();
            assert.equal(await modules.first().evaluate(element => element.open), changed,
              'Module state changed on reload');

            const ready = page.locator('details.module').filter({ has: page.locator('a[href^="/topics/"]') }).first();
            if (await ready.count()) {
              if (!await ready.evaluate(element => element.open)) await ready.locator('summary').click();
              const states = await modules.evaluateAll(elements => elements.map(element => element.open));
              await ready.locator('a[href^="/topics/"]').first().click();
              assert(page.url().includes('/topics/'), 'Article link did not open');
              await page.goBack();
              await page.reload();
              assert.deepEqual(await modules.evaluateAll(elements => elements.map(element => element.open)), states,
                'Module state changed after article and Back');
            }
            journeys.push({ subject, result: 'passed' });
          } catch (error) {
            journeys.push({ subject, result: 'failed' });
            issues.push({ severity: 'error', width, page: activePage,
              message: `Subject journey failed: ${error.message}` });
          }
        }
      }
      await context.close();
    }
  } finally {
    await browser.close();
  }

  const report = {
    started: started.toISOString(), completed: new Date().toISOString(),
    appVersion, versionCode, pages: pages.length, widths,
    checks: results.length, journeys, issues, samples
  };
  fs.writeFileSync(path.join(reportDir, 'audit.json'), JSON.stringify(report, null, 2) + '\n');
  const errors = issues.filter(issue => issue.severity === 'error');
  const warnings = issues.filter(issue => issue.severity === 'warning');
  const lines = [
    '# Android page audit', '',
    `App version: ${appVersion} (${versionCode})`,
    `Pages: ${pages.length}`, `Widths: ${widths.join(', ')}px`,
    `Page checks: ${results.length}`, `Errors: ${errors.length}`, `Warnings: ${warnings.length}`, '',
    'The browser used the same bundled pages and security policy as the Android app. It blocked external requests.',
    'This check cannot see Android system bars, WebView crashes, or behavior that only happens on a phone.', '',
    '## Subject journeys', '',
    ...journeys.map(journey => `- ${journey.subject}: ${journey.result}`), '',
    '## Issues', ''
  ];
  if (issues.length) {
    lines.push('| Level | Width | Page | Observation |', '| --- | --- | --- | --- |');
    for (const issue of issues) lines.push(`| ${issue.severity} | ${issue.width} | ${markdownCell(issue.page)} | ${markdownCell(issue.message)} |`);
  } else {
    lines.push('No issues found by these checks.');
  }
  lines.push('', '## Screenshots', '', ...samples.map(shot => `- [${shot}](${shot})`), '');
  fs.writeFileSync(path.join(reportDir, 'audit.md'), lines.join('\n'));
  console.log(`Audit report: ${path.join(reportDir, 'audit.md')}`);
  console.log(`${errors.length} errors, ${warnings.length} warnings across ${results.length} page checks.`);
  if (errors.length) process.exitCode = 1;
}

main().catch(error => { console.error(error); process.exitCode = 1; });
