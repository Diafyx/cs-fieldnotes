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
      await page.getByRole('button', { name: /theme/i }).click();
      await page.waitForFunction(() => document.documentElement.dataset.theme === 'dark');
      assert(signals.includes('/__app_theme__/dark'), 'Android theme signal was not sent');

      await page.getByRole('button', { name: 'Search topics' }).click();
      await page.getByRole('searchbox', { name: 'Search topics' }).fill('CPU Affinity');
      const result = page.getByRole('link', { name: /CPU Affinity, Cache Locality, and NUMA/ }).first();
      await result.waitFor();
      await result.click();
      await page.getByRole('heading', { name: 'CPU Affinity, Cache Locality, and NUMA' }).waitFor();

      await page.goto(origin + '/subjects/os.html');
      await page.locator('h1').getByText('Operating Systems', { exact: true }).waitFor();
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
