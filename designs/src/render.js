// Renders designs/svg/*.svg to designs/*.png
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const root = path.resolve(__dirname, '..');
  const sub = process.argv[2] === 'wb' ? 'svg-wb' : 'svg';
  const outDir = process.argv[2] === 'wb' ? path.join(root, 'bronkhorst-style') : root;
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 } });
  for (const f of fs.readdirSync(path.join(root, sub)).filter(f => f.endsWith('.svg')).sort()) {
    await page.goto('file://' + path.join(root, sub, f));
    await page.screenshot({ path: path.join(outDir, f.replace('.svg', '.png')) });
    console.log('rendered', f);
  }
  await browser.close();
})();
