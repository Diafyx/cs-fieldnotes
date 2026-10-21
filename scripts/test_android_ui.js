// Run the bundled Android pages in a phone-sized browser without network access.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const playwrightPath = path.join(root, '.mobile-test', 'node_modules', 'playwright');
if (!fs.existsSync(playwrightPath)) {
  throw new Error('Playwright is missing. See PLAY_STORE.md for the local UI test setup.');
}
const { chromium } = require(playwrightPath);
const assets = path.join(root, 'android', 'app', 'src', 'main', 'assets');
const origin = 'https://appassets.androidplatform.net';
const types = {
  '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.png': 'image/png', '.ttf': 'font/ttf'
};
const csp = "default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data:; connect-src 'self'; manifest-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'";

async function main() {
  const browser = await chromium.launch({ headless: true });
  try {
    for (const width of [320, 360, 412, 768]) {
      const context = await browser.newContext({
        viewport: { width, height: 800 }, isMobile: width < 768,
        hasTouch: true, serviceWorkers: 'block'
      });
      let externalRequests = 0;
      const errors = [];
      const signals = [];
      await context.route('**/*', async route => {
        const url = new URL(route.request().url());
        if (url.origin !== origin) {
          externalRequests++;
          return route.abort();
        }
        if (url.pathname.startsWith('/__app_theme__/')) {
          signals.push(url.pathname);
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
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(origin + '/index.html');
      await page.getByRole('heading', { name: 'Learn one idea well.' }).waitFor();
      assert.equal(await page.locator('[data-install-app]').count(), 0);
      const selectedSubjectIsVisible = () => page.locator('.side-nav').evaluate(nav => {
        const selected = nav.querySelector('.nav-link.active');
        if (!selected) return false;
        const navBox = nav.getBoundingClientRect();
        const selectedBox = selected.getBoundingClientRect();
        return selectedBox.left >= navBox.left - 1 && selectedBox.right <= navBox.right + 1;
      });
      await page.locator('.side-nav a[href="/subjects/lld.html"]').click();
      await page.getByRole('heading', { name: 'Low-Level Design' }).waitFor();
      assert(await selectedSubjectIsVisible(), `Selected rightmost subject is off screen at ${width}px`);
      await page.reload();
      assert(await selectedSubjectIsVisible(), `Selected subject moved off screen after reload at ${width}px`);
      for (const subject of ['oop', 'networks', 'os', 'dbms', 'sql', 'dbms', 'os', 'networks', 'oop', 'lld']) {
        await page.locator(`.side-nav a[href="/subjects/${subject}.html"]`).click();
        await page.waitForURL(`**/subjects/${subject}.html`);
        assert(await selectedSubjectIsVisible(), `Selected ${subject} subject is off screen at ${width}px`);
      }
      await page.goto(origin + '/index.html');
      await page.getByRole('button', { name: /theme/i }).click();
      await page.waitForFunction(() => document.documentElement.dataset.theme === 'dark');
      assert(signals.includes('/__app_theme__/dark'), 'Android theme signal was not sent');

      await page.getByRole('button', { name: 'Search topics' }).click();
      const searchBox = await page.locator('#search-dialog').boundingBox();
      assert(searchBox && searchBox.y <= 40, `Search opened too low at ${width}px: ${searchBox?.y}px`);
      await page.getByRole('searchbox', { name: 'Search topics' }).fill('CPU Affinity');
      const result = page.getByRole('link', { name: /CPU Affinity, Cache Locality, and NUMA/ }).first();
      await result.waitFor();
      await result.click();
      await page.getByRole('heading', { name: 'CPU Affinity, Cache Locality, and NUMA' }).waitFor();

      await page.getByRole('button', { name: 'Search topics' }).click();
      assert.equal(await page.locator('.search-history-item').first().textContent(), 'CPU Affinity');
      await page.locator('.search-history-item').first().click();
      assert.equal(await page.getByRole('searchbox', { name: 'Search topics' }).inputValue(), 'CPU Affinity');
      await page.getByRole('button', { name: 'Close search' }).click();
      for (let number = 1; number <= 6; number++) {
        await page.getByRole('button', { name: 'Search topics' }).click();
        await page.getByRole('searchbox', { name: 'Search topics' }).fill(`test search ${number}`);
        await page.getByRole('searchbox', { name: 'Search topics' }).press('Enter');
        await page.getByRole('button', { name: 'Close search' }).click();
      }
      await page.reload();
      await page.getByRole('button', { name: 'Search topics' }).click();
      assert.deepEqual(await page.locator('.search-history-item').allTextContents(),
        ['test search 6', 'test search 5', 'test search 4', 'test search 3', 'test search 2']);
      await page.getByRole('searchbox', { name: 'Search topics' }).fill('TEST SEARCH 6');
      await page.getByRole('searchbox', { name: 'Search topics' }).press('Enter');
      await page.getByRole('button', { name: 'Close search' }).click();
      await page.getByRole('button', { name: 'Search topics' }).click();
      assert.deepEqual(await page.locator('.search-history-item').allTextContents(),
        ['TEST SEARCH 6', 'test search 5', 'test search 4', 'test search 3', 'test search 2']);
      await page.getByRole('button', { name: 'Clear' }).click();
      assert.equal(await page.locator('.search-history-item').count(), 0);
      await page.getByRole('button', { name: 'Close search' }).click();

      await page.goto(origin + '/subjects/os.html');
      await page.locator('h1').getByText('Operating Systems', { exact: true }).waitFor();
      const modules = page.locator('details.module');
      assert.equal(await modules.nth(0).evaluate(element => element.open), true);
      assert.equal(await modules.nth(1).evaluate(element => element.open), true);
      await modules.nth(0).locator('summary').click();
      await modules.nth(1).locator('summary').click();
      await modules.nth(2).locator('a').first().click();
      await page.getByRole('heading', { name: 'Scheduling Queues and Schedulers' }).waitFor();
      assert(await selectedSubjectIsVisible(), `Selected subject is off screen in an article at ${width}px`);
      await page.goBack();
      await page.reload();
      assert(await selectedSubjectIsVisible(), `Selected subject is off screen after Back at ${width}px`);
      assert.equal(await modules.nth(0).evaluate(element => element.open), false,
        'First closed module reopened after returning to the subject');
      assert.equal(await modules.nth(1).evaluate(element => element.open), false,
        'Second closed module reopened after returning to the subject');
      assert.equal(await modules.nth(2).evaluate(element => element.open), true,
        'The open module closed after returning to the subject');
      await page.goto(origin + '/privacy.html');
      await page.getByRole('heading', { name: 'Privacy policy' }).waitFor();
      await page.getByText('This app does not ask for internet').waitFor();
      const size = await page.evaluate(() => ({ viewport: innerWidth, page: document.documentElement.scrollWidth }));
      assert(size.page <= size.viewport + 1, `Horizontal overflow at ${width}px`);

      await page.goto(origin + '/index.html');
      await page.getByRole('button', { name: 'Search topics' }).click();
      await page.getByRole('searchbox', { name: 'Search topics' })
        .fill('<img src=x onerror=window.__searchCodeRan=true>');
      assert.equal(await page.evaluate(() => window.__searchCodeRan), undefined, 'Search ran HTML as code');
      assert.deepEqual(errors, [], `Page errors at ${width}px`);
      assert.equal(externalRequests, 0, `A page tried to make a remote request at ${width}px`);
      await context.close();
      console.log(`Android UI passed at ${width}px`);
    }
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
