const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('../.mobile-test/node_modules/playwright');

async function main() {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1024, height: 500 }, deviceScaleFactor: 1 });
    await page.goto(pathToFileURL(path.join(__dirname, 'feature.html')).href);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(__dirname, 'feature.png') });
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
