# Reports semanais · padrão Grupo Opera

PDFs semanais por cliente do Reportei, no mesmo visual do `EGO_Update_Set-Out_2026.pdf`
(capa azul com destaque, comparativo semana × semana, gráfico diário, campanhas,
conteúdo, leitura e próximos passos).

## Estrutura

```
reports-semanais/
  _template/              gerador (comum a todas as semanas)
    build.py              monta o HTML de cada cliente e chama o render
    report.html.j2        layout (Jinja2 + CSS)
    measure.js            mede a altura real de cada bloco (paginação)
    render_pdf.js         HTML -> PDF A4 (Playwright/Chromium)
    summarize.py          resumo em texto dos dados, para escrever a narrativa
    fonts/                Poppins, Inter e Sora (locais)
  2026-11-16_22/          uma pasta por semana
    data/<cliente>.json        números coletados no Reportei
    narrativas/<cliente>.json  textos: título, destaque, leitura, próximos passos
    pdf/                       saída final
    html/                      HTML intermediário
```

## Gerar uma semana nova

1. Criar `reports-semanais/AAAA-MM-DD_DD/data/` com um JSON por cliente, no formato de
   `2026-11-16_22/data/ego-odontologia.json` (coleta pelo conector do Reportei:
   Meta Ads, Google Ads, Instagram, Facebook e outras plataformas).
2. Ver o resumo dos números para escrever os textos:

   ```bash
   cd reports-semanais/_template && python3 summarize.py ../AAAA-MM-DD_DD <slug>
   ```
3. Escrever `narrativas/<slug>.json` (copiar o de uma semana anterior e ajustar).
   Em textos, `**negrito**` e `*destaque em laranja*`.
4. Gerar os PDFs (todos ou só alguns slugs):

   ```bash
   cd reports-semanais/_template && python3 build.py ../AAAA-MM-DD_DD
   ```

Regras automáticas: contas de Meta Ads com menos de R$ 20 nas duas semanas ficam fora
da tabela; leads só aparecem quando são relevantes frente às conversas; métricas zeradas
nas duas semanas em "outras plataformas" são omitidas; o gráfico sobe de página quando
há espaço sobrando.
