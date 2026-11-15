# Relatórios semanais · Grupo Opera

Gera um PDF por marca, no visual do Grupo Opera (o mesmo do update da EGO em `../EGO_Update_Set-Out_2026.pdf`), comparando a semana atual (segunda a domingo) com a anterior. Os números vêm do Reportei.

## Como gerar

```bash
cd relatorios-semanais
node gerar.mjs modelo 2026-11-09     # cria dados/2026-11-09/<marca>.json, um por marca, com os campos vazios
# preencher os JSONs com os números do Reportei (ver abaixo)
node gerar.mjs pdf 2026-11-09        # gera saida/2026-11-09/Relatorio-Semanal_<Marca>_09-15nov2026.pdf
node gerar.mjs pdf 2026-11-09 ego    # só uma marca
node gerar.mjs exemplo --png         # prévia do layout com dados fictícios (marca d'água EXEMPLO)
```

A data é sempre a **segunda-feira** que abre a semana. Sem data, o script usa a última semana já encerrada. Domingo é o último dia da semana, então os números de domingo só ficam completos na segunda.

Uma marca sem nenhum número preenchido é pulada, para não sair PDF vazio. Precisa de Node 18+ e do Playwright com Chromium.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `marcas.json` | As 8 marcas, o `project_id` no Reportei e as contas (`integration_id`) de cada uma. `ativa: false` marca contas desconectadas, que ficam fora do relatório e aparecem na nota de fonte. |
| `metricas.json` | Quais métricas entram por plataforma, com o `reference_key` do Reportei, o formato e se subir é bom ou ruim (pinta a variação de verde ou vermelho). |
| `template/relatorio.html` | O template. Monta capa, página de números, gráfico diário, conteúdo, leitura e próximos passos, e pagina sozinho. |
| `template/fontes/` | Poppins e Inter embutidas (licença OFL), para o PDF sair igual sem internet. |
| `dados/<segunda>/<marca>.json` | Os números de cada semana. |
| `saida/<segunda>/` | Os PDFs gerados. |

## Preenchendo os dados

Cada `dados/<segunda>/<marca>.json` tem:

- `valores.<integration_id>.<métrica>` com `atual` e `anterior`. O `reference_key` de cada métrica está em `metricas.json`. Linha vazia ou com 0 nas duas semanas não aparece no PDF.
- `grafico`: os 7 valores diários de cada semana para a série indicada em `_ref`.
- `texto`, todo opcional (sem ele, o template monta textos e destaques automáticos):
  - `titulo` e `subtitulo` da capa. Use `*palavra*` para laranja e `**palavra**` para negrito.
  - `resumo`: o parágrafo da capa.
  - `destaque`: `{ numero, rotulo, titulo, texto }`, o cartão grande da capa.
  - `kpis_capa`: os 4 números da faixa da capa, `{ valor, texto }`.
  - `kpis`: os 4 cartões da página de números, `{ valor, rotulo, variacao, classe }`. `classe` é `pos`, `neg` ou `neu`.
  - `intro_numeros`, `leitura`, `proximos` (até 3 `{ titulo, texto }`).
- `conteudo` (opcional): posts da semana para a página de conteúdo. O formato está em `exemplo-ficticio.json`.

Com o conector do Reportei no Claude, o fluxo é pedir: *"preenche os dados da semana 2026-11-09 de todas as marcas pelo Reportei e gera os PDFs"*. O Claude usa `get_metrics_data` com os `reference_key` de `metricas.json` para cada conta de `marcas.json`.

## Pendências no Reportei

Estas contas estão desconectadas e precisam ser reconectadas para voltar ao relatório:

- Fiorini: página do Facebook (inativa desde 27/07/2026)
- Instituto Sanrire: Instagram `instituto.sanrire` (inativo desde 09/11/2026)
- Trait Odontologia: página do Facebook (inativa desde 13/07/2026)
