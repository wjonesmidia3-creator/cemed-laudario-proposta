# Relatórios semanais · 18 a 24/10/2026

Modelo Grupo Opera. Semana atual 18 a 24/10/2026, comparada com 11 a 17/10/2026; acumulado de outubro de 01 a 25/10/2026.

| Marca | Pasta | Canais |
|---|---|---|
| CEMED · Mirassol | `CEMED/` | Meta Ads, Google Ads |
| Dreisson · Vivo Imóveis | `Dreisson_Vivo_Imoveis/` | Meta Ads |
| D’Placido Odontologia | `DPlacido_Odontologia/` | Meta Ads, Instagram |
| EGO Odontologia | `EGO_Odontologia/` | Meta Ads, Google Ads, Instagram, Facebook |
| Fiorini Odonto & Estética | `Fiorini_Odonto/` | Meta Ads, Google Ads |
| Trait Odontologia | `Trait_Odontologia/` | Meta Ads, Google Ads, Instagram, Perfil da Empresa no Google |
| Instituto Sanrire (reduzido) | `Instituto_Sanrire/` | Google Ads, YouTube, ChatGPT Ads (semana e mês) |

Cada pasta tem o PDF do relatório e o texto de envio (`Texto_envio_WhatsApp.txt`); todos os textos juntos estão em `TEXTOS_PARA_ENVIO.md`. Fontes: Reportei para todos os canais, exceto o ChatGPT Ads da Sanrire, que vem dos prints do OpenAI Ads Manager de 26/10/2026.

## Como gerar de novo

```bash
cd gerador
python3 build.py <pasta_saida>            # gera os HTML (todas as marcas; ou passe as chaves: ego cemed sanrire ...)
node render.js <pasta_saida> - <pasta_saida>/*.html   # gera os PDF A4 (Playwright/Chromium)
```

Os números ficam em `gerador/dados/*.json`. Os textos de análise ficam em `build.py` (uma função por marca) e `sanrire.py`.
