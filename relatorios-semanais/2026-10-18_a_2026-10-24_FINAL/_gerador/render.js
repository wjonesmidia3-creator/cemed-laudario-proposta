// Renderiza cada HTML em PDF A4 (e PNG de conferência por página).
// Uso: node render.js <saida_pdf_dir> <preview_dir|-> arquivo1.html [arquivo2.html ...]
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [outDir, previewDir, ...files] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  for (const f of files) {
    await page.goto('file://' + path.resolve(f), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const overflow = await page.evaluate(() =>
      [...document.querySelectorAll('.page')].map((p, i) => {
        const c = p.querySelector('.content');
        const f = p.querySelector('.foot');
        if (!c || !f) return { page: i + 1, ok: true };
        const cb = c.getBoundingClientRect().bottom, ft = f.getBoundingClientRect().top;
        return { page: i + 1, free: Math.round(ft - cb) };
      })
    );
    const fonts = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight));
    const base = path.basename(f, '.html');
    await page.pdf({ path: path.join(outDir, base + '.pdf'), format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    if (previewDir !== '-') {
      const pages = await page.$$('.page');
      for (let i = 0; i < pages.length; i++) {
        await pages[i].screenshot({ path: path.join(previewDir, `${base}-p${i + 1}.png`) });
      }
    }
    console.log(base, JSON.stringify(overflow), 'fonts:', [...new Set(fonts)].length);
  }
  await browser.close();
})();
