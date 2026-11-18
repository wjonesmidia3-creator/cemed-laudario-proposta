# Guia de redação · relatório semanal Grupo Opera

O relatório vai para o **cliente**. Tom: claro, direto, honesto e construtivo, em português do Brasil. Nada de jargão sem explicação, nada de comparar um cliente com outro, nada de número que não esteja nos dados coletados.

Exemplos prontos (um por cliente): `dados/2026-11-02_a_08/clientes/*.json`. Siga a mesma estrutura e o mesmo nível de texto.

## Regras de número

- Formato brasileiro: `1.486,79`, `R$ 18,10`, `12,3 mil`.
- Variação percentual = (atual − anterior) ÷ anterior. Abaixo de 10% use uma casa decimal (`4,8%`); de 10% para cima, inteiro (`37%`). É a mesma regra que o gerador usa nos selos.
- Nos campos numéricos (`cur`, `prev` de KPIs e linhas) use o valor **sem arredondar** (ex.: `18.0951`). O gerador arredonda na exibição.
- Todo número citado em texto precisa bater com os dados coletados e com as tabelas do próprio relatório.
- Custo por conversa = investimento ÷ conversas. Custo por conversão no Google = custo ÷ conversões.
- `ig:reach` é "Alcance (soma diária)": diga isso no rótulo.
- O CPC do Meta (`fb_ads:cpc`) é calculado sobre **todos os cliques**, não só os cliques no link: rotule como "CPC (todos os cliques)" para ninguém tentar dividir investimento por cliques no link.

## Marcação nos textos

- `{{texto}}` = destaque laranja (títulos da capa, destaque, faixa). No `titulo_p3` vira a parte laranja do título.
- `**texto**` = negrito (lead, intros, insights, leitura).
- Nos rótulos de KPI, `\n` quebra a linha.

## Estrutura do JSON (`dados/<pasta>/clientes/<arquivo>.json`)

| Campo | O que é | Limite para caber |
|---|---|---|
| `arquivo`, `nome` | nome do arquivo (sem acento/espaço) e nome exibido | — |
| `titulo` | 2 linhas da capa; a 1ª com um `{{destaque}}` | até ~30 caracteres por linha |
| `lead` | "Resumo semanal de **canais** do cliente, comparando a semana de X com a semana anterior (Y)." | até ~230 |
| `destaque` | `num` (número grande, até 6 caracteres), `rotulo` (ex.: CONVERSAS), `titulo` (frase com 1–2 `{{}}`), `texto` (contexto) | titulo ~120 · texto ~220 |
| `faixa` | 4 itens `{valor, legenda}` no rodapé da capa; valor curto com `{{}}` | valor até ~9 caracteres · legenda ~60 |
| `intro_p2` | 1–2 frases sobre a semana | até ~160 |
| `kpis` | 4 cartões `{valor, ref?, rotulo, cur, prev, melhor}`; `ref` é o "/72" ao lado do valor | rótulo 2 linhas de ~22 |
| `grupos` | tabela: `{titulo, linhas:[{rotulo, prev, cur, fmt, melhor, destaque?}]}` | **linhas + títulos de grupo ≤ 14** (com posts) |
| `grafico` | `{titulo, sub, unidade?, prev:[7], cur:[7]}`; `unidade: "brl"` para R$ | — |
| `fonte` | "Fonte: Reportei (canais). " + observações (feriado, conta sem dados, integração inativa) | até ~2 linhas |
| `titulo_p3`, `intro_p3` | ex.: `Conteúdo e {{próximos passos}}` / `O que mudou e {{próximos passos}}` | — |
| `posts` | até 4 `{data:"05/NOV", tag, titulo, metricas:[[valor, rótulo]]}` | título ~45 |
| `insights` | 3 (ou 4) `{tipo: bom/ruim/neu, titulo, texto}` | título ~32 · texto ~140 |
| `leitura` | 2–3 frases: a interpretação da semana | até ~380 |
| `proximos` | 3 `{titulo, texto}`: ações concretas da agência | título ~28 · texto ~110 |
| `nota_p3` | opcional, ex.: "Visualizações e interações dos posts são orgânicas e acumuladas desde a publicação até DD/MM." | — |
| `denso` | `true` quando a tabela passa de ~16 linhas (aperta o espaçamento) | — |

`fmt`: `int` (inteiro), `brl` (R$ com centavos), `brl0` (R$ sem centavos).
`melhor`: `"up"` quando subir é bom (conversas, alcance, cliques), `"down"` quando cair é bom (custos, CPC), `null` quando é neutro (investimento).
`destaque: true` nas linhas principais (conversas, custo por conversa, conversões e o que mais mudou): elas ganham cor e selo de variação.

## Tom: texto amarrado, vendendo o trabalho, sem cara de IA (vale para PDF e WhatsApp)

- **Uma história só por cliente.** Escolha o fio da semana (ex.: "mais conversas com custo menor" ou "anúncios pararam dois dias") e amarre tudo nele: título da capa, destaque, intro, insights, leitura, próximos passos e mensagem contam a mesma história, sem repetir a mesma frase.
- **Vender o trabalho da agência com fatos.** Ligue o resultado à gestão: "a campanha de mensagens segue trazendo contato a R$ 18", "o Google Ads entregou o menor custo por conversão do mês", "identificamos a queda e já ajustamos…" só se o ajuste for fato. Nunca invente ação que não foi feita; quando não souber, fale do próximo passo ("vamos ajustar", "a proposta é…"). Em semana ruim, venda o controle: mostramos que vimos o problema cedo e temos o plano.
- **Escrita de gente.** Frases curtas, voz ativa, primeira pessoa do plural ("a gente", "nós", "vamos"). Português do dia a dia de quem cuida da conta.
- **Proibido (soa IA):** travessão longo (—) no meio da frase, "vale destacar", "além disso", "em resumo", "nesse sentido", "é importante ressaltar", "não apenas… mas também", "alavancar", "potencializar", "robusto", "jornada", "estratégico" solto, trios de adjetivos, exclamações em série, emoji no começo de cada linha.
- **Sem exagero.** Nada de "resultado incrível/excelente". Deixe o número falar ("35 conversas, 5 a mais que na semana anterior").

## Mensagem de WhatsApp (campo `whatsapp`)

Vai no grupo do cliente junto com o PDF. Tem de parecer escrita pelo gestor da conta. Até ~900 caracteres (máximo 1100).

```
Oi, pessoal! Passando o resumo da semana de 09 a 15/11 da Nome do cliente.

Parágrafo de 2 a 3 frases com o principal resultado e o porquê, com 1–2 *números em negrito*.

*Números da semana* (vs. 02 a 08/11)
• 3 a 5 linhas: "Conversas pelo Instagram/Facebook: 40 (antes 35)"

Parágrafo curto com o ponto de atenção (se houver) e o que vamos fazer nesta semana, em 2 a 3 frases ou lista 1. 2. 3.

O relatório completo está no PDF abaixo. Qualquer dúvida, é só chamar.
```

- No máximo 1 emoji na mensagem inteira (ou nenhum). Formatação do WhatsApp: `*negrito*`, `_itálico_`; nada de `**` ou `#`.
- Mesmos números e mesmas regras de percentual do PDF; cada número tem de estar no relatório.
- Cuidado com o período: um pico ou queda da semana anterior não pode parecer desta semana.
- Escreva para o dono do negócio: sem siglas soltas (CPC = "custo por clique"), nada de Reportei/API/integração/coleta, sem culpar o cliente.

## O que escolher

- **Destaque da capa**: o resultado principal da semana (conversas, contatos ou conversões). Se algo grave aconteceu (anúncios parados, conta sem veiculação), o destaque é isso.
- **KPIs**: os 4 números que o cliente precisa ver primeiro, com a comparação.
- **Tabela**: um grupo por canal (`ANÚNCIOS · META ADS`, `GOOGLE ADS`, `INSTAGRAM`, `FACEBOOK`…). Corte linhas secundárias para respeitar o limite.
- **Gráfico** (14 dias): alcance diário do Instagram se houver dados; senão, alcance diário da página do Facebook; senão, investimento diário no Meta Ads (`unidade: "brl"`).
- **Posts**: os da semana atual, no máximo 4, ordenados por engajamento; marque na `tag` o tipo (REELS, CARROSSEL, IMAGEM) e, se couber, "· MAIS ENGAJAMENTO" / "· MAIS ALCANCE". Use um título curto que descreva o tema (não copie a legenda inteira).
- **Insights**: o que subiu, o que caiu e o principal ponto de atenção.
- **Próximos passos**: ações que a agência pode fazer ou propor (ajustar verba, renovar criativos, revisar rastreamento, retomar posts). Escreva para o cliente: nada de linguagem interna (Reportei, API, coleta, integração).

## Alertas que sempre aparecem

- Conta com investimento ~0 na semana e > 0 na anterior: **anúncios parados** (diga a data da última veiculação, se o diário mostrar).
- Dias com investimento ~0 **no meio da semana** (série diária do Meta): **pausa parcial**. Diga as datas e trate como causa provável da queda, não como "verba menor" (foi o caso da EGO em 03 e 04/11).
- Google Ads com 0 conversões nas duas semanas, mesmo com cliques: sugerir conferir a tag e as ações de conversão.
- Conversões caindo muito mais que cliques: sugerir **revisar o rastreamento de conversões**.
- Integração que não retornou dados ou está inativa: citar na `fonte` ou num insight.
- Feriado nacional dentro da semana: citar na `fonte` (ex.: "Semana com feriado de Finados (02/11).").

## Depois de escrever

```bash
python3 gerar.py <pasta> <arquivo> --validar   # estrutura
python3 gerar.py <pasta> <arquivo>             # gera o PDF e mede a folga até o rodapé
```
Código 3 / "ESTOURO" = conteúdo encostando no rodapé: encurte textos ou tire linhas da tabela e gere de novo.
