# Catálogo Reportei para o relatório semanal

Objetos de métrica **exatos** já testados com `get_metrics_data` (copie como estão; não precisa chamar `list_metrics`).
Sempre use `start`/`end` = semana atual e `comparisonStart`/`comparisonEnd` = semana anterior nas chamadas "com comparação".

## Instabilidade conhecida

- O MCP do Reportei às vezes demora mais de 60 s ou devolve `Bad Gateway`. Repita a chamada (até 3 vezes); se insistir, divida as métricas em lotes menores.
- Valores podem vir como texto (`"633.33"`): converta para número.
- `{"warning": "There is no data for the selected period"}` em todas as métricas = conta sem veiculação nas duas semanas (registre como "sem dados").
- `get_top_content` NÃO serve (devolve seguidores por cidade). Para posts use `ig:media_datatable`.
- `compare_periods(projectId)` cobre YouTube, ChatGPT Ads, Google Meu Negócio e conversões do Google, mas **não** traz investimento nem conversas do Meta Ads, nem custo do Google Ads.

## facebook_ads — números (com comparação)

```json
[{"id":"a1","reference_key":"fb_ads:spend","component":"number_v1","metrics":["spend"],"type":["spend","ads-cost_per_conversion"]},
 {"id":"a2","reference_key":"fb_ads:actions_onsite_conversion.messaging_conversation_started_7d","component":"number_v1","metrics":["actions:onsite_conversion.messaging_conversation_started_7d"]},
 {"id":"a3","reference_key":"fb_ads:spend-actions_onsite_conversion.messaging_conversation_started_7d","component":"number_v1","metrics":["spend:onsite_conversion.messaging_conversation_started_7d"]},
 {"id":"a4","reference_key":"fb_ads:cpc","component":"number_v1","metrics":["cpc"]},
 {"id":"a5","reference_key":"fb_ads:reach","component":"number_v1","metrics":["reach"],"type":"reach"},
 {"id":"a6","reference_key":"fb_ads:impressions","component":"number_v1","metrics":["impressions"],"type":"impressions"},
 {"id":"a7","reference_key":"fb_ads:inline_link_clicks","component":"number_v1","metrics":["inline_link_clicks"]},
 {"id":"a8","reference_key":"fb_ads:actions_lead","component":"number_v1","metrics":["actions:lead"]}]
```
a1 investimento (R$) · a2 conversas iniciadas por mensagem · a3 custo por conversa (R$) · a4 CPC sobre **todos os cliques** (R$; não é investimento ÷ a7) · a5 alcance · a6 impressões · a7 cliques no link · a8 leads.

## facebook_ads — por plataforma (com comparação, opcional)

```json
[{"id":"p1","reference_key":"fb_ads:actions_onsite_conversion.messaging_conversation_started_7d_instagram","component":"number_v1","metrics":["actions:onsite_conversion.messaging_conversation_started_7d"],"dimensions":[{"field":"publisher_platform","operator":"IN","value":["instagram"]}]},
 {"id":"p2","reference_key":"fb_ads:actions_onsite_conversion.messaging_conversation_started_7d_facebook","component":"number_v1","metrics":["actions:onsite_conversion.messaging_conversation_started_7d"],"dimensions":[{"field":"publisher_platform","operator":"IN","value":["facebook"]}]},
 {"id":"p3","reference_key":"fb_ads:spend_instagram","component":"number_v1","metrics":["spend"],"dimensions":[{"field":"publisher_platform","operator":"IN","value":["instagram"]}]},
 {"id":"p4","reference_key":"fb_ads:spend_facebook","component":"number_v1","metrics":["spend"],"dimensions":[{"field":"publisher_platform","operator":"IN","value":["facebook"]}]}]
```

## facebook_ads — investimento diário (SEM comparação, start = início da semana anterior, end = fim da semana atual → 14 dias)

```json
[{"id":"s1","reference_key":"fb_ads:spend_by_date","component":"chart_v1","dimensions":[{"field":"date_start"}],"metrics":["spend"]}]
```
Dias sem veiculação não aparecem nos `labels`: complete com 0.

## google_adwords — números (com comparação)

```json
[{"id":"g1","reference_key":"gads:cost_micros","component":"number_v1","metrics":["metrics.cost_micros"],"type":["spend","ads-cost_per_conversion"]},
 {"id":"g2","reference_key":"gads:clicks","component":"number_v1","metrics":["metrics.clicks"],"type":"clicks"},
 {"id":"g3","reference_key":"gads:impressions","component":"number_v1","metrics":["metrics.impressions"],"type":"impressions"},
 {"id":"g4","reference_key":"gads:all_conversions","component":"number_v1","metrics":["metrics.all_conversions"]}]
```
g1 já vem em reais (não divida por 1.000.000). Conversões **principais** (`gads:conversions`) vêm em `compare_periods`; muitas contas só registram em "todas as conversões" (g4).

## instagram_business — números (com comparação)

```json
[{"id":"i1","reference_key":"ig:reach","component":"number_v1","metrics":["reach"]},
 {"id":"i2","reference_key":"ig:views","component":"number_v1","metrics":["views"],"type":"total_impressions"},
 {"id":"i3","reference_key":"ig:profile_views","component":"number_v1","metrics":["profile_views"]},
 {"id":"i4","reference_key":"ig:new_followers_count","component":"number_v1","metrics":["new_followers"],"type":"new_followers"}]
```
`ig:reach` é a **soma do alcance diário** (escreva assim no relatório). i4 pode vir com aviso de "sem histórico": trate como sem dado.

## instagram_business — alcance diário (SEM comparação, 14 dias)

```json
[{"id":"d1","reference_key":"ig:reach_over_time","component":"chart_v1","metrics":["reach"],"dimensions":["date"]}]
```

## instagram_business — posts da semana (SEM comparação, só a semana atual)

```json
[{"id":"m1","reference_key":"ig:media_datatable","component":"datatable_v1","metrics":["type","reach","views","total_interactions","post_interactions_rate","likes","comments","saved","follows","profile_visits","shares","created_at"],"dimensions":["media"],"sort":["-reach"],"custom":{"sendByWebhook":true}}]
```
Colunas na ordem: media(texto, url) · tipo · alcance · views · interações · taxa de engajamento (0,125 = 12,5%) · curtidas · comentários · salvos · follows · visitas ao perfil · compartilhamentos · data.

## facebook (página) — números (com comparação; `trend.data` traz o diário da semana atual)

```json
[{"id":"f1","reference_key":"fb:page_reach","component":"number_v1","metrics":["page_impressions_unique"]},
 {"id":"f2","reference_key":"fb:page_media_views","component":"number_v1","metrics":["page_media_view"]}]
```
Para o diário de 14 dias: chame f1 SEM comparação com start = início da semana anterior e end = fim da semana atual (`trend.data` com 14 valores).

## Integrações inativas

Integrações com `status: "inactive"` não devem ser consultadas; cite na fonte do relatório ("integração inativa no Reportei").
