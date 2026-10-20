// Gera um PDF do Plano Black November por cliente a partir de template.html.
// Uso: NODE_PATH=$(npm root -g) node gerar.js [arquivo-do-cliente]
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const dir = __dirname;
const saida = path.join(dir, '..');
const template = fs.readFileSync(path.join(dir, 'template.html'), 'utf8');
const clientes = JSON.parse(fs.readFileSync(path.join(dir, 'clientes.json'), 'utf8'));
const filtro = process.argv[2];

function preencher(c) {
  const m = c.artigo === 'o';
  const vars = {
    NOME: c.nome,
    NOME_UP: c.nome.toUpperCase(),
    DA: `${m ? 'do' : 'da'} ${c.nome}`,
    NA: `${m ? 'no' : 'na'} ${c.nome}`,
    DA_CLINICA: `${m ? 'do' : 'da'} ${c.nome}`,
  };
  return template.replace(/\{\{(\w+)\}\}/g, (_, k) => {
    if (!(k in vars)) throw new Error(`Variável desconhecida: ${k}`);
    return vars[k];
  });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const c of clientes) {
    if (filtro && c.arquivo !== filtro) continue;
    const html = path.join(dir, `.tmp_${c.arquivo}.html`);
    fs.writeFileSync(html, preencher(c));
    await page.goto('file://' + html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.emulateMedia({ media: 'print' });
    const pdf = path.join(saida, `Black_November_${c.arquivo}_2026.pdf`);
    await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
    fs.unlinkSync(html);
    console.log('ok', path.relative(process.cwd(), pdf));
  }
  await browser.close();
})();
