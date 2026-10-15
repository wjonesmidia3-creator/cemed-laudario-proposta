// Gera Contrato_Grupo_Opera_CEMED.pdf a partir de contrato.html.
// Uso: NODE_PATH="$(npm root -g)" node contratos/cemed/gerar-pdf.js
const path = require("path");
const { chromium } = require("playwright");

const dir = __dirname;
const entrada = path.join(dir, "contrato.html");
const saida = path.join(dir, "Contrato_Grupo_Opera_CEMED.pdf");

const rodape = `
<div style="width:100%;padding:0 16mm;font:500 7pt/1 Inter,Arial,sans-serif;color:#677190;display:flex;justify-content:space-between;">
  <span><b style="color:#00247D;font-weight:700">Grupo Opera<span style="color:#E85D1B">.</span></b>&nbsp;&nbsp;·&nbsp;&nbsp;Contrato de gestão de tráfego pago&nbsp;&nbsp;·&nbsp;&nbsp;CEMED</span>
  <span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span>
</div>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + entrada, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);

  const pendentes = await page.evaluate(() => window.__pendentes || []);
  await page.pdf({
    path: saida,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: "<div></div>",
    footerTemplate: rodape,
  });
  await browser.close();

  console.log("PDF gerado:", saida);
  if (pendentes.length) {
    console.log("Campos a preencher no CONFIG de contrato.html:");
    pendentes.forEach((p) => console.log("  -", p));
  }
})();
