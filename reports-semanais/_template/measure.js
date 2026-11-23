// Mede a altura (px) de cada bloco .blk[data-i] de um HTML gerado pelo build.py.
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await page.goto('file://' + process.argv[2], { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const h = await page.evaluate(() => {
    const out = {};
    document.querySelectorAll('.blk[data-i]').forEach((el) => { out[el.dataset.i] = Math.ceil(el.getBoundingClientRect().height); });
    return out;
  });
  process.stdout.write(JSON.stringify(h));
  await browser.close();
})();
