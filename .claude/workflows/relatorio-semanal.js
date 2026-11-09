export const meta = {
  name: 'relatorio-semanal',
  description: 'Relatório semanal Grupo Opera: coleta no Reportei, confere os números, redige, revisa e gera um PDF por cliente',
  whenToUse: 'Gerar os relatórios semanais de todos os clientes do Reportei. args: {inicio: "AAAA-MM-DD" (1º dia da semana), fim?: "AAAA-MM-DD", clientes?: ["CEMED", ...], pasta?: string, exemplo?: "2026-11-02_a_08" | null, atualizar_readme?: boolean}',
  phases: [
    { title: 'Descobrir', detail: 'clientes e integrações no Reportei; grava semana.json' },
    { title: 'Coletar', detail: 'um agente por cliente puxa as métricas das duas semanas' },
    { title: 'Conferir', detail: 'segunda leitura independente dos números principais, com desempate' },
    { title: 'Redigir', detail: 'escreve o JSON do cliente e gera o PDF' },
    { title: 'Revisar', detail: 'revisor cético confere cada número e cada frase' },
    { title: 'Fechar', detail: 'gera todos os PDFs juntos e atualiza o README' },
  ],
}

// ------------------------------------------------------------------ parâmetros e datas
const A = args || {}
if (!A.inicio || !/^\d{4}-\d{2}-\d{2}$/.test(A.inicio)) {
  throw new Error('Informe args.inicio no formato AAAA-MM-DD (primeiro dia da semana do relatório).')
}
const MES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
const MESL = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
const p2 = (n) => String(n).padStart(2, '0')
const dia = (s) => { const [y, m, d] = s.split('-').map(Number); return new Date(Date.UTC(y, m - 1, d)) }
const iso = (dt) => dt.toISOString().slice(0, 10)
const soma = (dt, n) => new Date(dt.getTime() + n * 86400000)
const ddmm = (dt) => `${p2(dt.getUTCDate())}/${p2(dt.getUTCMonth() + 1)}`
const mesmoMes = (a, b) => a.getUTCMonth() === b.getUTCMonth()
const curto = (a, b) => (mesmoMes(a, b) ? `${p2(a.getUTCDate())} a ${ddmm(b)}` : `${ddmm(a)} a ${ddmm(b)}`)

const ini = dia(A.inicio)
const fim = A.fim ? dia(A.fim) : soma(ini, 6)
const nDias = Math.round((fim - ini) / 86400000) + 1
if (nDias !== 7) throw new Error(`A semana precisa ter 7 dias (recebi ${nDias}).`)
const cIni = soma(ini, -7)
const cFim = soma(ini, -1)
const S = {
  inicio: iso(ini), fim: iso(fim), comp_inicio: iso(cIni), comp_fim: iso(cFim),
  prev_curto: curto(cIni, cFim),
  cur_curto: curto(ini, fim),
  cur_longo: mesmoMes(ini, fim)
    ? `${p2(ini.getUTCDate())} a ${p2(fim.getUTCDate())} de ${MESL[fim.getUTCMonth()]}/${fim.getUTCFullYear()}`
    : `${p2(ini.getUTCDate())} de ${MESL[ini.getUTCMonth()]} a ${p2(fim.getUTCDate())} de ${MESL[fim.getUTCMonth()]}/${fim.getUTCFullYear()}`,
  dias: Array.from({ length: 14 }, (_, i) => ddmm(soma(cIni, i))),
  pasta: A.pasta || (mesmoMes(ini, fim) ? `${iso(ini)}_a_${p2(fim.getUTCDate())}` : `${iso(ini)}_a_${p2(fim.getUTCMonth() + 1)}-${p2(fim.getUTCDate())}`),
  sufixo: mesmoMes(ini, fim)
    ? `${p2(ini.getUTCDate())}-${p2(fim.getUTCDate())}${MES[fim.getUTCMonth()]}${fim.getUTCFullYear()}`
    : `${p2(ini.getUTCDate())}${MES[ini.getUTCMonth()]}-${p2(fim.getUTCDate())}${MES[fim.getUTCMonth()]}${fim.getUTCFullYear()}`,
}
const EXEMPLO = A.exemplo === undefined ? '2026-11-02_a_08' : A.exemplo
const ATUALIZAR_README = A.atualizar_readme !== false
const SO = Array.isArray(A.clientes) && A.clientes.length ? new Set(A.clientes) : null

const G = 'relatorios-semanais/_gerador'
const RAIZ = 'Trabalhe na raiz do repositório git (rode `cd "$(git rev-parse --show-toplevel)"` antes de qualquer comando); todos os caminhos abaixo são relativos a ela.'

// nomes de arquivo e de exibição já usados nos relatórios (mantém os PDFs com o mesmo nome toda semana)
const CONHECIDOS = {
  'CEMED': ['CEMED', 'CEMED'],
  'Dreisson': ['Dreisson', 'Dreisson'],
  'D`placido': ['DPlacido', "D'Placido Odonto"],
  'EGO Odontologia': ['EGO_Odontologia', 'EGO Odontologia'],
  'Fiorini': ['Fiorini', 'Fiorini Odonto'],
  'Instituto Sanrire': ['Instituto_Sanrire', 'Instituto Sanrire'],
  'Luisa Alves Tattoo': ['Luisa_Alves_Tattoo', 'Luisa Alves Tattoo'],
  'Trait Odontologia': ['Trait_Odontologia', 'Trait Odontologia'],
}

// ------------------------------------------------------------------ schemas
const NUM = { type: ['number', 'null'] }
const DESC = {
  type: 'object',
  properties: {
    clientes: { type: 'array', items: { type: 'object', properties: {
      projectId: { type: 'integer' }, nome: { type: 'string' }, arquivo: { type: 'string' }, nome_exibicao: { type: 'string' },
      integracoes: { type: 'array', items: { type: 'object', properties: {
        id: { type: 'integer' }, slug: { type: 'string' }, nome: { type: 'string' }, status: { type: 'string' } },
        required: ['id', 'slug', 'status'] } } },
      required: ['projectId', 'nome', 'arquivo', 'nome_exibicao', 'integracoes'] } },
    semana_gravada: { type: 'boolean' },
  },
  required: ['clientes', 'semana_gravada'],
}
const BRUTO = {
  type: 'object',
  properties: {
    integracoes: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'integer' }, slug: { type: 'string' }, nome: { type: 'string' },
      situacao: { type: 'string', enum: ['ok', 'sem_dados', 'inativa', 'erro'] }, observacao: { type: 'string' } },
      required: ['id', 'slug', 'situacao'] } },
    metricas: { type: 'array', items: { type: 'object', properties: {
      integracao_id: { type: 'integer' }, slug: { type: 'string' }, chave: { type: 'string' }, rotulo: { type: 'string' }, cur: NUM, prev: NUM },
      required: ['integracao_id', 'slug', 'chave', 'cur', 'prev'] } },
    diarios: { type: 'array', items: { type: 'object', properties: {
      integracao_id: { type: 'integer' }, chave: { type: 'string' },
      datas: { type: 'array', items: { type: 'string' } }, valores: { type: 'array', items: { type: 'number' } } },
      required: ['integracao_id', 'chave', 'datas', 'valores'] } },
    posts: { type: 'array', items: { type: 'object', properties: {
      integracao_id: { type: 'integer' }, data: { type: 'string' }, tipo: { type: 'string' }, tema: { type: 'string' },
      alcance: NUM, views: NUM, interacoes: NUM, engajamento_pct: NUM, comentarios: NUM, url: { type: 'string' } },
      required: ['data', 'tipo', 'tema'] } },
    projeto: { type: 'array', items: { type: 'object', properties: {
      slug: { type: 'string' }, chave: { type: 'string' }, cur: NUM, prev: NUM },
      required: ['slug', 'chave', 'cur', 'prev'] } },
    avisos: { type: 'array', items: { type: 'string' } },
  },
  required: ['integracoes', 'metricas', 'diarios', 'posts', 'projeto', 'avisos'],
}
const CONF = {
  type: 'object',
  properties: {
    conferidos: { type: 'array', items: { type: 'object', properties: {
      integracao_id: { type: 'integer' }, chave: { type: 'string' }, cur: NUM, prev: NUM },
      required: ['integracao_id', 'chave', 'cur', 'prev'] } },
    avisos: { type: 'array', items: { type: 'string' } },
  },
  required: ['conferidos', 'avisos'],
}
const REDACAO = {
  type: 'object',
  properties: {
    manchete: { type: 'string' },
    alertas: { type: 'array', items: { type: 'string' } },
    gerou_pdf: { type: 'boolean' },
  },
  required: ['manchete', 'alertas', 'gerou_pdf'],
}
const REVISAO = {
  type: 'object',
  properties: {
    correcoes: { type: 'array', items: { type: 'string' } },
    pendencias: { type: 'array', items: { type: 'string' } },
    gerou_pdf: { type: 'boolean' },
  },
  required: ['correcoes', 'pendencias', 'gerou_pdf'],
}
const FECHAR = {
  type: 'object',
  properties: {
    pdfs: { type: 'array', items: { type: 'string' } },
    ok: { type: 'boolean' },
    observacoes: { type: 'array', items: { type: 'string' } },
  },
  required: ['pdfs', 'ok', 'observacoes'],
}

// ------------------------------------------------------------------ 1. descobrir clientes
phase('Descobrir')
const semanaJson = JSON.stringify(S, null, 2)
const desc = await agent(`${RAIZ}

Liste os clientes (projetos) e as contas (integrações) no Reportei e prepare a pasta da semana.

1. Carregue as ferramentas com ToolSearch "select:mcp__Reportei__list_projects,mcp__Reportei__list_integrations".
2. Chame list_projects e list_integrations (sem filtro, perPage 100) e percorra TODAS as páginas (meta.last_page).
3. Para cada projeto, devolva projectId, nome, arquivo, nome_exibicao e as integrações (id, slug, nome, status "active"/"inactive"). Contas com o mesmo nome são integrações diferentes: liste todas.
   - arquivo e nome_exibicao: para os projetos abaixo use exatamente estes valores; para projetos novos, arquivo = nome sem acentos com "_" no lugar de espaços e símbolos, nome_exibicao = nome do projeto.
${Object.entries(CONHECIDOS).map(([k, [a, n]]) => `     - "${k}" → arquivo "${a}", nome_exibicao "${n}"`).join('\n')}
4. Crie a pasta ${G}/dados/${S.pasta}/clientes/ e grave ${G}/dados/${S.pasta}/semana.json com EXATAMENTE este conteúdo:
${semanaJson}
Responda semana_gravada = true só se o arquivo foi gravado.`, { label: 'descobrir', phase: 'Descobrir', schema: DESC })

if (!desc || !desc.semana_gravada) throw new Error('Não consegui listar os clientes ou gravar semana.json.')
let clientes = desc.clientes.filter((c) => c.integracoes.some((i) => i.status === 'active'))
const semAtivas = desc.clientes.filter((c) => !clientes.includes(c)).map((c) => c.nome)
if (semAtivas.length) log(`Sem integrações ativas (fora do relatório): ${semAtivas.join(', ')}`)
if (SO) {
  const fora = clientes.filter((c) => !SO.has(c.arquivo)).map((c) => c.arquivo)
  clientes = clientes.filter((c) => SO.has(c.arquivo))
  if (fora.length) log(`Filtrado por args.clientes; não serão gerados: ${fora.join(', ')}`)
}
log(`Semana ${S.cur_curto} vs ${S.prev_curto} · ${clientes.length} cliente(s): ${clientes.map((c) => c.arquivo).join(', ')}`)

// ------------------------------------------------------------------ prompts por cliente
const listaInteg = (c) => c.integracoes.map((i) => `  - id ${i.id} · ${i.slug} · "${i.nome || ''}" · ${i.status === 'active' ? 'ativa' : 'INATIVA'}`).join('\n')

const promptColetar = (c) => `${RAIZ}

Você coleta dados do Reportei para o relatório semanal do cliente "${c.nome}" (projectId ${c.projectId}).
Semana atual: ${S.inicio} a ${S.fim}. Semana anterior (comparação): ${S.comp_inicio} a ${S.comp_fim}.
Integrações:
${listaInteg(c)}

1. Leia ${G}/catalogo_reportei.md: ele tem os objetos de métrica EXATOS por tipo de integração e as instabilidades conhecidas. Não chame list_metrics para o que já está lá.
2. Carregue as ferramentas: ToolSearch "select:mcp__Reportei__get_metrics_data,mcp__Reportei__compare_periods".
3. Para cada integração ATIVA, faça as chamadas do catálogo para o tipo dela (pode chamar várias integrações em paralelo):
   - números com comparação: start=${S.inicio}, end=${S.fim}, comparisonStart=${S.comp_inicio}, comparisonEnd=${S.comp_fim};
   - série diária de 14 dias SEM comparação (start=${S.comp_inicio}, end=${S.fim}): ig:reach_over_time (Instagram), fb:page_reach (página do Facebook, use trend.data), fb_ads:spend_by_date (Meta Ads);
   - posts do Instagram da semana atual: ig:media_datatable com start=${S.inicio}, end=${S.fim};
   - Meta Ads por plataforma (p1 a p4 do catálogo) quando a conta teve conversas.
   Em timeout ou Bad Gateway, repita até 3 vezes; se persistir, divida as métricas em lotes menores.
4. Chame compare_periods(projectId ${c.projectId}, mesmas datas) uma vez e copie para "projeto" as métricas de youtube, chatgpt_ads, google_my_business e gads:conversions / gads:all_conversions.
5. Integração inativa: não consulte, marque situacao "inativa".

Regras do retorno:
- "metricas": uma entrada por (integração, reference_key) com cur = semana atual e prev = semana anterior, sempre NÚMERO (converta texto). null só quando a API não trouxer o valor. Integração sem dado nenhum nas duas semanas → situacao "sem_dados".
- "diarios": 14 datas (AAAA-MM-DD, de ${S.comp_inicio} a ${S.fim}) e 14 valores; dia ausente = 0.
- "posts": data AAAA-MM-DD, tipo (Reels, Carrossel, Imagem), tema = resumo de 3 a 8 palavras da legenda, engajamento_pct em % (0,125 → 12.5).
- "avisos": tudo que for estranho (queda brusca, conta sem dados, aviso da API, chamada que falhou mesmo após repetir).
- NÃO invente nem estime valores. Não escreva arquivos.`

const promptConferir = (c, alvos, desempate) => `${RAIZ}

${desempate ? 'Terceira leitura (desempate)' : 'Conferência independente'} de números do Reportei para o cliente "${c.nome}". Busque os valores você mesmo, do zero: não há valores de referência, só a lista do que buscar.
Semana atual: ${S.inicio} a ${S.fim}. Semana anterior: ${S.comp_inicio} a ${S.comp_fim}.
Use get_metrics_data (carregue com ToolSearch "select:mcp__Reportei__get_metrics_data") na integração indicada, com comparação, usando o objeto de métrica do arquivo ${G}/catalogo_reportei.md cuja reference_key é a chave. Junte as chaves de uma mesma integração numa única chamada.
Itens:
${alvos.map((a) => `- integração ${a.integracao_id} (${a.slug}): ${a.chave}`).join('\n')}
Devolva cur (semana atual) e prev (semana anterior) como números; null se a API não devolver. Em timeout, repita até 3 vezes. Não escreva arquivos.`

const promptRedigir = (c, dados) => `${RAIZ}

Você escreve o relatório semanal do cliente "${c.nome_exibicao}" para a agência Grupo Opera. O leitor é o próprio cliente.
Semana atual: ${S.cur_curto} (${S.inicio} a ${S.fim}). Semana anterior: ${S.prev_curto} (${S.comp_inicio} a ${S.comp_fim}).

Leia antes de escrever:
1. ${G}/guia_redacao.md (regras de número, estrutura do JSON, limites de texto, alertas obrigatórios).
2. ${EXEMPLO
    ? `Modelo pronto: ${G}/dados/${EXEMPLO}/clientes/${c.arquivo}.json (se não existir, qualquer arquivo da mesma pasta). Copie estrutura e tom; os NÚMEROS de lá são de outra semana e não valem aqui.`
    : `Não abra ${G}/dados/2026-11-02_a_08/ (semana em validação). Siga apenas o guia.`}

Dados coletados e conferidos — a ÚNICA fonte de números:
\`\`\`json
${JSON.stringify(dados.bruto)}
\`\`\`
${dados.divergencias.length ? `Divergências entre leituras, já resolvidas pela mediana: ${JSON.stringify(dados.divergencias)}` : 'A conferência independente bateu com a coleta.'}
Se houver feriado nacional entre ${S.inicio} e ${S.fim}, cite na fonte.

Grave ${G}/dados/${S.pasta}/clientes/${c.arquivo}.json com "arquivo": "${c.arquivo}" e "nome": "${c.nome_exibicao}".
Depois, dentro de ${G}, rode:
  python3 gerar.py ${S.pasta} ${c.arquivo} --validar
  python3 gerar.py ${S.pasta} ${c.arquivo}
e corrija até os dois saírem com código 0 (ESTOURO = encurte textos ou tire linhas secundárias da tabela).
Não edite arquivos de outros clientes nem gerar.py, estilo.css ou pdf.js.
Retorne a manchete (1 frase com o principal resultado da semana) e os alertas (anúncios parados, contas sem dados, quedas fortes, rastreamento suspeito).`

const promptRevisar = (c, dados) => `${RAIZ}

Você é o revisor final, cético, do relatório semanal do cliente "${c.nome_exibicao}". Parta do princípio de que há erros e procure cada um.
Arquivo: ${G}/dados/${S.pasta}/clientes/${c.arquivo}.json · Guia: ${G}/guia_redacao.md
Dados de referência (a única fonte válida de números):
\`\`\`json
${JSON.stringify(dados.bruto)}
\`\`\`

Confira, um por um:
1. Tabela (grupos) e KPIs: cur e prev batem com os dados; custos derivados estão certos (custo por conversa = investimento ÷ conversas; custo por conversão = custo ÷ conversões); "melhor" no sentido certo (custos "down", volumes "up", investimento null); fmt adequado.
2. Cada número e percentual citado em QUALQUER texto (titulo, lead, destaque, faixa, intro_p2, intro_p3, insights, leitura, proximos, fonte, posts): recalcule com a regra do guia (abaixo de 10% uma casa decimal, de 10% para cima inteiro) e confirme que bate com os dados e com a própria tabela.
3. Gráfico: as séries prev/cur são os 7+7 valores certos de "diarios" (ordem cronológica); no Instagram, a soma dos 7 dias atuais deve bater com ig:reach da semana.
4. Afirmações: toda conclusão é sustentada pelos dados? Nada inventado, nada comparando com outros clientes, nenhuma causa afirmada como fato sem evidência (use "indica", "sugere").
5. Alertas obrigatórios do guia: anúncios parados, conversões caindo muito mais que cliques, integração sem dados ou inativa, feriado na semana.
6. Português: ortografia, acentos, concordância.
Corrija direto no arquivo. Depois, dentro de ${G}, rode python3 gerar.py ${S.pasta} ${c.arquivo} (código 0; se ESTOURO, encurte e rode de novo).
Retorne cada correção feita no formato "campo: antes → depois" e as pendências que precisam de decisão humana.`

// ------------------------------------------------------------------ conferência com desempate
const PRINCIPAIS = new Set([
  'fb_ads:spend', 'fb_ads:actions_onsite_conversion.messaging_conversation_started_7d',
  'gads:cost_micros', 'gads:all_conversions', 'ig:reach', 'ig:views', 'fb:page_reach',
])
const chave = (m) => `${m.integracao_id}|${m.chave}`
const difere = (a, b) => {
  if (a == null || b == null) return (a == null) !== (b == null)
  return Math.abs(a - b) > Math.max(0.01 * Math.max(Math.abs(a), Math.abs(b)), 0.5)
}
const mediana = (vs) => {
  const v = vs.filter((x) => x != null).sort((x, y) => x - y)
  return v.length ? v[Math.floor((v.length - 1) / 2)] : null
}

async function conferir(bruto, c) {
  const alvos = bruto.metricas.filter((m) => PRINCIPAIS.has(m.chave))
  if (!alvos.length) return { bruto, divergencias: [], conferidos: 0 }
  const r1 = await agent(promptConferir(c, alvos, false), { label: `conferir:${c.arquivo}`, phase: 'Conferir', schema: CONF })
  if (!r1) { log(`${c.arquivo}: conferência falhou; seguindo só com a coleta`); return { bruto, divergencias: [], conferidos: 0 } }
  const m1 = new Map(r1.conferidos.map((x) => [chave(x), x]))
  const diverg = alvos.filter((m) => m1.has(chave(m)) && (difere(m.cur, m1.get(chave(m)).cur) || difere(m.prev, m1.get(chave(m)).prev)))
  const registro = []
  if (diverg.length) {
    log(`${c.arquivo}: ${diverg.length} número(s) divergente(s) entre leituras → desempate`)
    const r2 = await agent(promptConferir(c, diverg, true), { label: `desempate:${c.arquivo}`, phase: 'Conferir', schema: CONF })
    const m2 = new Map((r2 ? r2.conferidos : []).map((x) => [chave(x), x]))
    for (const m of diverg) {
      const a = m1.get(chave(m)), b = m2.get(chave(m))
      const final = { cur: mediana([m.cur, a.cur, b && b.cur]), prev: mediana([m.prev, a.prev, b && b.prev]) }
      registro.push({ integracao_id: m.integracao_id, chave: m.chave,
        coleta: { cur: m.cur, prev: m.prev }, conferencia: { cur: a.cur, prev: a.prev },
        desempate: b ? { cur: b.cur, prev: b.prev } : null, final })
      m.cur = final.cur
      m.prev = final.prev
    }
  }
  return { bruto, divergencias: registro, conferidos: m1.size }
}

// ------------------------------------------------------------------ pipeline por cliente
const resultados = await pipeline(
  clientes,
  (c) => agent(promptColetar(c), { label: `coletar:${c.arquivo}`, phase: 'Coletar', schema: BRUTO }),
  (bruto, c) => {
    if (!bruto) throw new Error(`coleta de ${c.arquivo} falhou`)
    const semDados = bruto.integracoes.filter((i) => i.situacao !== 'ok').map((i) => `${i.slug} ${i.id}: ${i.situacao}`)
    if (semDados.length) log(`${c.arquivo}: ${semDados.join(' · ')}`)
    return conferir(bruto, c)
  },
  async (dados, c) => {
    const red = await agent(promptRedigir(c, dados), { label: `redigir:${c.arquivo}`, phase: 'Redigir', schema: REDACAO })
    if (!red) throw new Error(`redação de ${c.arquivo} falhou`)
    return { ...dados, redacao: red }
  },
  async (dados, c) => {
    const rev = await agent(promptRevisar(c, dados), { label: `revisar:${c.arquivo}`, phase: 'Revisar', schema: REVISAO })
    if (rev) log(`${c.arquivo}: revisão com ${rev.correcoes.length} correção(ões), ${rev.pendencias.length} pendência(s)`)
    return { arquivo: c.arquivo, nome: c.nome_exibicao, ...dados, revisao: rev }
  },
)

const prontos = resultados.filter(Boolean)
const falharam = clientes.filter((c) => !prontos.some((r) => r.arquivo === c.arquivo)).map((c) => c.arquivo)
if (falharam.length) log(`ATENÇÃO: sem relatório para ${falharam.join(', ')}`)

// ------------------------------------------------------------------ fechamento (precisa de todos os clientes)
phase('Fechar')
const manchetes = prontos.map((r) => `- ${r.nome} (${r.arquivo}): ${r.redacao.manchete}`).join('\n')
const fechamento = await agent(`${RAIZ}

Feche o relatório semanal da pasta ${S.pasta}.
1. Dentro de ${G}, rode: python3 gerar.py ${S.pasta}
   Deve sair com código 0 e um PDF por cliente em relatorios-semanais/${S.pasta}/. Se algum cliente der ERRO ou ESTOURO, corrija só o JSON dele (encurtar texto ou tirar linha secundária) e rode de novo.
2. Confira com ls que existem ${prontos.length} PDFs e que nenhum arquivo _tmp_ ficou em ${G}/fonts/.
3. ${ATUALIZAR_README
    ? `Atualize relatorios-semanais/README.md: acima da seção da semana mais recente, adicione "## Semana ${S.cur_curto}/${S.fim.slice(0, 4)} (comparada com ${S.prev_curto})" no mesmo formato da seção existente (pasta + tabela Cliente | Arquivo | Destaque), usando estas manchetes resumidas:\n${manchetes}`
    : 'Não altere o README.'}
Não faça commit. Liste os PDFs gerados (caminho relativo) e qualquer observação.`, { label: 'fechar', phase: 'Fechar', schema: FECHAR })

return {
  semana: S,
  pdfs: fechamento ? fechamento.pdfs : [],
  fechamento_ok: fechamento ? fechamento.ok : false,
  observacoes: fechamento ? fechamento.observacoes : ['fechamento falhou'],
  falharam,
  clientes: prontos.map((r) => ({
    arquivo: r.arquivo,
    manchete: r.redacao.manchete,
    alertas: r.redacao.alertas,
    conferidos: r.conferidos,
    divergencias: r.divergencias,
    correcoes_revisao: r.revisao ? r.revisao.correcoes : null,
    pendencias: r.revisao ? r.revisao.pendencias : null,
    avisos_coleta: r.bruto.avisos,
    bruto: r.bruto,
  })),
}
