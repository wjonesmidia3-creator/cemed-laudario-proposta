// Converte HTML -> PDF (A4) com o Chromium do Playwright.
// Uso: node pdf.js lista.json   (lista = [[html, pdf, png?], ...])
const { chromium } = require('playwright');
const fs = require('fs');
let estouro = false;

(async () => {
  const pares = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  for (const [html, pdf, png] of pares) {
    await page.goto('file://' + html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    // checagem: nenhum bloco de conteúdo pode encostar no rodapé
    const problemas = await page.evaluate(() => {
      const out = [];
      document.querySelectorAll('.page').forEach((pg, i) => {
        const ftr = pg.querySelector('.ftr');
        const body = pg.querySelector('.body');
        if (!ftr || !body) return;
        const limite = ftr.getBoundingClientRect().top - 6;
        let fundo = 0;
        body.querySelectorAll(':scope > *').forEach(el => { fundo = Math.max(fundo, el.getBoundingClientRect().bottom); });
        if (fundo > limite) out.push(`página ${i + 1}: conteúdo passa ${Math.round(fundo - limite)}px do limite`);
        else out.push(`página ${i + 1}: folga ${Math.round(limite - fundo)}px`);
      });
      return out;
    });
    const nome = pdf.split('/').pop();
    console.log(nome, '|', problemas.join(' | '));
    if (problemas.some(p => p.includes('passa'))) {
      estouro = true;
      console.log(`ESTOURO ${nome}: encurte textos ou remova linhas da tabela e gere de novo`);
    }
    await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true,
                     margin: { top: 0, bottom: 0, left: 0, right: 0 } });
    if (png) await page.screenshot({ path: png, fullPage: true });
    console.log('ok', pdf);
  }
  await browser.close();
  if (estouro) process.exit(3);
})();
