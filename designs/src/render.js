// Renders designs/svg/*.svg to designs/*.png
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const root = path.resolve(__dirname, '..');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 } });
  for (const f of fs.readdirSync(path.join(root, 'svg')).filter(f => f.endsWith('.svg')).sort()) {
    await page.goto('file://' + path.join(root, 'svg', f));
    await page.screenshot({ path: path.join(root, f.replace('.svg', '.png')) });
    console.log('rendered', f);
  }
  await browser.close();
})();
