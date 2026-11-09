# Relatórios semanais · padrão Grupo Opera

Um PDF por cliente, no mesmo visual do update da EGO (capa azul, comparativo lado a lado, leitura e próximos passos).

## Semana 02 a 08/11/2026 (comparada com 26/10 a 01/11)

Pasta `2026-11-02_a_08/`:

| Cliente | Arquivo | Destaque da semana |
|---|---|---|
| CEMED | `CEMED_Semanal_02-08nov2026.pdf` | 82 contatos (+28%), Google Ads com 66 conversões |
| D'Placido Odonto | `DPlacido_Semanal_02-08nov2026.pdf` | 110 conversas a R$ 6,75 |
| Dreisson | `Dreisson_Semanal_02-08nov2026.pdf` | 24 conversas (+14%), custo por conversa −13% |
| EGO Odontologia | `EGO_Odontologia_Semanal_02-08nov2026.pdf` | verba −37%, 35 conversas a R$ 18,10 |
| Fiorini Odonto | `Fiorini_Semanal_02-08nov2026.pdf` | Meta +29% de conversas; **Google Ads sem veiculação** |
| Instituto Sanrire | `Instituto_Sanrire_Semanal_02-08nov2026.pdf` | custo por conversa −19%; Google estável |
| Luisa Alves Tattoo | `Luisa_Alves_Tattoo_Semanal_02-08nov2026.pdf` | **anúncios pausados desde 31/10** |
| Trait Odontologia | `Trait_Odontologia_Semanal_02-08nov2026.pdf` | conversas −34%, conversões Google −67% |

Fonte: Reportei, extração em 09/11/2026.

## Como gerar a próxima semana (automático)

Peça ao Claude Code, nesta pasta do repositório:

> Rode o workflow relatorio-semanal com inicio 2026-11-09

O workflow `.claude/workflows/relatorio-semanal.js` faz tudo, com um agente por cliente rodando em paralelo:

1. **Descobrir** – lista clientes e contas no Reportei (cliente novo entra sozinho) e grava `semana.json`.
2. **Coletar** – puxa as métricas das duas semanas, as séries diárias e os posts (usa `_gerador/catalogo_reportei.md`, sem perder tempo procurando métrica).
3. **Conferir** – outro agente busca de novo, sem ver os valores, os números principais (investimento, conversas, custo do Google, conversões, alcance). Se divergir, um terceiro desempata pela mediana.
4. **Redigir** – escreve o JSON do cliente seguindo `_gerador/guia_redacao.md` e o relatório da semana anterior como modelo, e gera o PDF.
5. **Revisar** – um revisor cético recalcula cada número e percentual dos textos, confere o gráfico e o português, e corrige.
6. **Fechar** – gera todos os PDFs juntos e acrescenta a semana neste README.

Parâmetros (`args`): `inicio` (obrigatório, AAAA-MM-DD), `fim` (padrão: inicio + 6 dias), `clientes` (ex.: `["CEMED","Fiorini"]` para refazer só alguns), `exemplo` (pasta usada como modelo; padrão `2026-11-02_a_08`), `atualizar_readme` (padrão `true`).
No fim ele devolve, por cliente: manchete, alertas, divergências encontradas na conferência e correções do revisor. Vale ler os alertas antes de enviar.

## Como ajustar à mão

Os dados e textos de cada cliente ficam em `_gerador/dados/<pasta>/clientes/<arquivo>.json` (formato descrito no guia de redação). Depois de editar, na pasta `_gerador`:

```bash
python3 gerar.py 2026-11-02_a_08 --validar
```

```bash
python3 gerar.py 2026-11-02_a_08 CEMED Fiorini
```

O primeiro só confere a estrutura; o segundo gera os PDFs dos clientes indicados (sem nomes, gera todos).
O gerador imprime a folga de cada página até o rodapé e sai com código 3 ("ESTOURO") se algo encostar nele: encurte textos ou remova linhas da tabela.
Tabelas com mais de 14 linhas (somando os títulos de grupo) ou clientes sem posts levam o gráfico para a página 3 automaticamente.

Requisitos: Python 3 e Node com Playwright (Chromium). As fontes Poppins e Inter estão em `_gerador/fonts/` (licença OFL).
