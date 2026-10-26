# Relatórios semanais · 18 a 24/10/2026

Modelo Grupo Opera. Semana atual 18 a 24/10/2026, comparada com 11 a 17/10/2026; acumulado de outubro de 01 a 25/10/2026.

| Marca | Arquivo | Canais |
|---|---|---|
| CEMED · Mirassol | `Relatorio_Semanal_CEMED_18-24out2026.pdf` | Meta Ads, Google Ads |
| Dreisson · Vivo Imóveis | `Relatorio_Semanal_Dreisson_Vivo_Imoveis_18-24out2026.pdf` | Meta Ads |
| D’Placido Odontologia | `Relatorio_Semanal_DPlacido_Odontologia_18-24out2026.pdf` | Meta Ads, Instagram |
| EGO Odontologia | `Relatorio_Semanal_EGO_Odontologia_18-24out2026.pdf` | Meta Ads, Google Ads, Instagram, Facebook |
| Fiorini Odonto & Estética | `Relatorio_Semanal_Fiorini_Odonto_18-24out2026.pdf` | Meta Ads, Google Ads |
| Trait Odontologia | `Relatorio_Semanal_Trait_Odontologia_18-24out2026.pdf` | Meta Ads, Google Ads, Instagram, Perfil da Empresa no Google |
| Instituto Sanrire (reduzido) | `Relatorio_Semanal_Reduzido_Instituto_Sanrire_18-24out2026.pdf` | Google Ads, YouTube, ChatGPT Ads (semana e mês) |

Fontes: Reportei para todos os canais, exceto o ChatGPT Ads da Sanrire, que vem dos prints do OpenAI Ads Manager de 26/10/2026.

## Como gerar de novo

```bash
cd gerador
python3 build.py <pasta_saida>            # gera os HTML (todas as marcas; ou passe as chaves: ego cemed sanrire ...)
node render.js <pasta_saida> - <pasta_saida>/*.html   # gera os PDF A4 (Playwright/Chromium)
```

Os números ficam em `gerador/dados/*.json`. Os textos de análise ficam em `build.py` (uma função por marca) e `sanrire.py`.
