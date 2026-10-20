# Plano Black November · fonte

Modelo no padrão visual Grupo Opera (A4, Poppins + Inter) usado para gerar um PDF por clínica.

- `template.html`: conteúdo e layout. `{{NOME}}`, `{{DA}}`, `{{NA}}` etc. são trocados pelo nome de cada clínica.
- `clientes.json`: lista de clínicas. `artigo` é `"a"` ou `"o"` (gera "da EGO" / "do Instituto Sanrire").
- `gerar.js`: gera os PDFs na pasta de cima.

```bash
NODE_PATH=$(npm root -g) node gerar.js              # todas as clínicas
NODE_PATH=$(npm root -g) node gerar.js Fiorini      # só uma (campo "arquivo")
```

Precisa do Playwright com Chromium instalado.
