// Converte os HTML gerados pelo build.py em PDF (A4) com o Chromium do Playwright.
// Uso: node render_pdf.js '[{"html": "...", "pdf": "..."}]'
const { chromium } = require('playwright');

(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const job of jobs) {
    await page.goto('file://' + job.html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForFunction(() => window.__fitted === true);
    // aviso se algum bloco passar do limite da página
    const overflow = await page.evaluate(() =>
      [...document.querySelectorAll('.page')].map((p, i) => {
        const c = p.querySelector('.content');
        if (!c) return null;
        const footer = p.querySelector('.footer').getBoundingClientRect().top;
        const last = [...c.children].pop();
        const bottom = last ? last.getBoundingClientRect().bottom : 0;
        return bottom > footer - 4 ? `página ${i + 1}: conteúdo passa ${Math.round(bottom - footer + 4)}px do rodapé` : null;
      }).filter(Boolean)
    );
    overflow.forEach((m) => console.warn('AVISO', job.pdf.split('/').pop(), m));
    await page.pdf({ path: job.pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
    console.log('pdf:', job.pdf);
  }
  await browser.close();
})();
