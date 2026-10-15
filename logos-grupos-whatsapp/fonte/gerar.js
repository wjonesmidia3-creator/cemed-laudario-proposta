// Gera as fotos de grupo do WhatsApp (PNG 1080x1080) a partir de logo-grupo.html.
// Uso: node gerar.js "CEMED" "D’Plácido"
const path = require("path");
const { chromium } = require("playwright");

const clientes = process.argv.slice(2);
if (clientes.length === 0) {
  console.error('Informe ao menos um cliente. Ex.: node gerar.js "CEMED"');
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1080 } });
  const html = "file://" + path.join(__dirname, "logo-grupo.html");

  for (const cliente of clientes) {
    await page.goto(html + "?cliente=" + encodeURIComponent(cliente));
    await page.waitForSelector("body[data-pronto='1']");
    // Nome do arquivo sem acentos, apóstrofos ou espaços: "D’Plácido" -> "DPlacido".
    const slug = cliente.normalize("NFD").replace(/[^A-Za-z0-9]/g, "");
    const arquivo = path.join(__dirname, "..", `${slug}_GO_WhatsApp.png`);
    await page.locator("#logo").screenshot({ path: arquivo });
    console.log("ok:", arquivo);
  }

  await browser.close();
})();
