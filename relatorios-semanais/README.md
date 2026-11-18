# Relatórios semanais · padrão Grupo Opera

Um PDF por cliente, no mesmo visual do update da EGO (capa azul, comparativo lado a lado, leitura e próximos passos).

## Semana 09 a 15/11/2026 (comparada com 02 a 08/11)

Pasta `2026-11-09_a_15/` · para baixar: `downloads/Relatorios_Semanais_09-15nov2026.zip` (os 8 PDFs) ou `downloads/09-15nov2026/`. Mensagens para os grupos de WhatsApp (tom de gestor da conta, sem emoji): `downloads/Mensagens_WhatsApp_09-15nov2026.zip` ou `downloads/mensagens_09-15nov2026/`.

| Cliente | Destaque da semana |
|---|---|
| CEMED | 63 contatos, 61 pelo Google; **Meta sem veiculação desde 10/11** (ainda parado em 17/11) |
| D'Placido Odonto | 109 conversas a R$ 6,85; Instagram sem posts na semana |
| Dreisson | custo por conversa estável (R$ 19,81); **anúncios parados de 12 a 15/11** (voltaram em 16/11) |
| EGO Odontologia | 53 conversas (+51%) a R$ 14,19, Meta no ar os 7 dias; Google sem conversões |
| Fiorini Odonto | 73 conversas no Meta; **Google Ads parado desde 02/11** |
| Instituto Sanrire | 32 conversas, alcance do Meta +28%; conversões principais do Google −28%; ChatGPT Ads parado |
| Luisa Alves Tattoo | anúncios de volta: 99 conversas a R$ 3,14 |
| Trait Odontologia | 43 conversas (+87%) a R$ 19,76; **Google Ads parado desde 07/11** |

Fonte: Reportei, extração em 18/11/2026. Dados brutos de cada cliente em `_gerador/dados/2026-11-09_a_15/bruto/`.

## Semana 02 a 08/11/2026 (comparada com 26/10 a 01/11)

Pasta `2026-11-02_a_08/` · para baixar: `downloads/Relatorios_Semanais_02-08nov2026.zip` (os 8 PDFs) ou `downloads/02-08nov2026/`. Mensagens curtas para os grupos de WhatsApp: `downloads/Mensagens_WhatsApp_02-08nov2026.zip` ou `downloads/mensagens_02-08nov2026/` (um .txt por cliente e `_TODAS_AS_MENSAGENS.txt`):

| Cliente | Arquivo | Destaque da semana |
|---|---|---|
| CEMED | `CEMED_Semanal_02-08nov2026.pdf` | 82 contatos (+28%), Google Ads com 66 conversões |
| D'Placido Odonto | `DPlacido_Semanal_02-08nov2026.pdf` | 110 conversas a R$ 6,75 |
| Dreisson | `Dreisson_Semanal_02-08nov2026.pdf` | 24 conversas (+14%), custo por conversa −13% |
| EGO Odontologia | `EGO_Odontologia_Semanal_02-08nov2026.pdf` | **Meta quase parado em 03 e 04/11**; 35 conversas a R$ 18,10 |
| Fiorini Odonto | `Fiorini_Semanal_02-08nov2026.pdf` | Meta +29% de conversas; **Google Ads sem veiculação** |
| Instituto Sanrire | `Instituto_Sanrire_Semanal_02-08nov2026.pdf` | custo por conversa −19%; Google estável |
| Luisa Alves Tattoo | `Luisa_Alves_Tattoo_Semanal_02-08nov2026.pdf` | **anúncios pausados desde 31/10** |
| Trait Odontologia | `Trait_Odontologia_Semanal_02-08nov2026.pdf` | conversas −34%, conversões Google −67% |

Fonte: Reportei, extração em 09/11/2026. Os 112 números brutos desta semana foram conferidos de novo, do zero, pelo workflow (validação em 09/11): todos bateram.

## Como gerar a próxima semana (automático)

Peça ao Claude Code, nesta pasta do repositório:

> Rode o workflow relatorio-semanal com inicio 2026-11-09

O workflow `.claude/workflows/relatorio-semanal.js` faz tudo, com um agente por cliente rodando em paralelo:

1. **Descobrir** – lista clientes e contas no Reportei (cliente novo entra sozinho) e grava `semana.json`.
2. **Coletar** – puxa as métricas das duas semanas, as séries diárias e os posts (usa `_gerador/catalogo_reportei.md`, sem perder tempo procurando métrica).
3. **Conferir** – outro agente busca de novo, sem ver os valores, os números principais (investimento, conversas, custo do Google, conversões, alcance). Se divergir, um terceiro desempata pela mediana.
4. **Redigir** – escreve o JSON do cliente seguindo `_gerador/guia_redacao.md` e o relatório da semana anterior como modelo, e gera o PDF.
5. **Revisar** – um revisor cético recalcula cada número e percentual dos textos, confere o gráfico e o português, e corrige.
6. **Fechar** – gera todos os PDFs juntos, atualiza a pasta `downloads/` (PDFs, .zip da semana e mensagens de WhatsApp de cada cliente) e acrescenta a semana neste README.

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
