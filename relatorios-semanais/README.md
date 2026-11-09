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

## Como gerar a próxima semana

1. Copie `_gerador/semana_2026_11_02.py` para um novo arquivo (ex.: `semana_2026_11_09.py`).
2. Atualize `SEMANA` (rótulos, dias do gráfico, pasta e sufixo) e, em `CLIENTES`, os números e textos de cada cliente.
3. Rode na pasta `_gerador`:

```bash
python3 gerar.py semana_2026_11_09
```

Para gerar só alguns clientes, passe o nome do arquivo depois do módulo (ex.: `python3 gerar.py semana_2026_11_09 CEMED Fiorini`).

O script imprime a folga de cada página até o rodapé; se aparecer "conteúdo passa", encurte textos ou remova linhas da tabela.
Tabelas com mais de 14 linhas (somando os títulos de grupo) ou clientes sem posts levam o gráfico para a página 3 automaticamente.

Requisitos: Python 3 e Node com Playwright (Chromium). As fontes Poppins e Inter estão em `_gerador/fonts/` (licença OFL).
