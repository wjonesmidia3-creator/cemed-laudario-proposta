#!/usr/bin/env node
// Gera os relatórios semanais do Grupo Opera a partir dos dados do Reportei.
//
//   node gerar.mjs modelo [AAAA-MM-DD]          cria dados/<segunda>/<marca>.json vazios para preencher
//   node gerar.mjs pdf    [AAAA-MM-DD] [marca…] gera saida/<segunda>/*.pdf a partir dos dados preenchidos
//   node gerar.mjs exemplo                      gera saida/exemplo-ficticio.pdf (prévia do layout)
//
// A data é a segunda-feira que abre a semana. Sem data, usa a última semana de
// segunda a domingo cujo domingo já chegou.

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const AQUI = dirname(fileURLToPath(import.meta.url));
const MARCAS = JSON.parse(readFileSync(join(AQUI, 'marcas.json'), 'utf8'));
const METRICAS = JSON.parse(readFileSync(join(AQUI, 'metricas.json'), 'utf8'));
delete MARCAS._sobre; delete METRICAS._sobre;

const NOME_PLATAFORMA = {
  facebook_ads: 'anúncios Meta', google_adwords: 'Google Ads', chatgpt_ads: 'ChatGPT Ads',
  instagram_business: 'Instagram', facebook: 'Facebook', google_my_business: 'Google Meu Negócio', youtube: 'YouTube',
};
const FONTE_PLATAFORMA = {
  facebook_ads: 'Meta Ads', google_adwords: 'Google Ads', chatgpt_ads: 'ChatGPT Ads',
  instagram_business: 'Instagram Business', facebook: 'Página do Facebook', google_my_business: 'Google Meu Negócio', youtube: 'YouTube',
};

// ---------- datas ----------
const iso = (dt) => dt.toISOString().slice(0, 10);
const somaDias = (s, n) => { const dt = new Date(s + 'T12:00:00Z'); dt.setUTCDate(dt.getUTCDate() + n); return iso(dt); };
function segundaPadrao() {
  const hoje = new Date(); hoje.setUTCHours(12, 0, 0, 0);
  const dow = (hoje.getUTCDay() + 6) % 7; // 0 = segunda
  const seg = new Date(hoje); seg.setUTCDate(hoje.getUTCDate() - dow);
  if (dow !== 6) seg.setUTCDate(seg.getUTCDate() - 7); // semana corrente ainda não fechou
  return iso(seg);
}
function periodos(segunda) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(segunda)) throw new Error(`Data inválida: ${segunda} (use AAAA-MM-DD)`);
  if (new Date(segunda + 'T12:00:00Z').getUTCDay() !== 1) throw new Error(`${segunda} não é uma segunda-feira`);
  return {
    atual: { inicio: segunda, fim: somaDias(segunda, 6) },
    anterior: { inicio: somaDias(segunda, -7), fim: somaDias(segunda, -1) },
  };
}
const diasDe = (p) => Array.from({ length: 7 }, (_, i) => somaDias(p.inicio, i));

// ---------- modelo ----------
function modelo(marcaId, segunda) {
  const m = MARCAS[marcaId];
  const per = periodos(segunda);
  const valores = {};
  for (const f of m.fontes.filter((x) => x.ativa)) {
    const cat = METRICAS[f.slug];
    if (!cat) continue;
    valores[f.id] = { _conta: `${f.conta} (${f.slug})` };
    for (const l of cat.linhas) valores[f.id][l.id] = { atual: null, anterior: null };
  }
  let grafico = null;
  if (m.grafico) {
    const f = m.fontes.find((x) => x.id === m.grafico.fonte);
    const g = METRICAS[f.slug].graficos[m.grafico.tipo];
    grafico = {
      fonte: m.grafico.fonte, tipo: m.grafico.tipo, _ref: g.ref,
      anterior: diasDe(per.anterior).map((data) => ({ data, valor: null })),
      atual: diasDe(per.atual).map((data) => ({ data, valor: null })),
    };
  }
  return {
    marca: marcaId,
    periodo: per,
    valores,
    grafico,
    texto: {
      titulo: '', subtitulo: '', resumo: '',
      destaque: null,
      kpis_capa: null, kpis: null,
      intro_numeros: '',
      leitura: '',
      proximos: [],
    },
    conteudo: null,
  };
}

// ---------- normalização para o template ----------
const vazio = (v) => v === null || v === undefined || v === '';
function normalizar(dados) {
  // o exemplo fictício traz a própria configuração para não usar o nome de um cliente real
  const m = dados.ficticio && dados.marca_config ? dados.marca_config : MARCAS[dados.marca];
  if (!m) throw new Error(`Marca desconhecida: ${dados.marca}`);
  const grupos = [];
  const plataformas = [];
  const fontes = [];
  let preenchidos = 0;
  for (const f of m.fontes.filter((x) => x.ativa)) {
    const cat = METRICAS[f.slug];
    const vals = (dados.valores || {})[f.id] || {};
    const linhas = [];
    for (const l of cat.linhas) {
      const v = vals[l.id] || {};
      const a = vazio(v.atual) ? null : Number(v.atual);
      const b = vazio(v.anterior) ? null : Number(v.anterior);
      if (a === null && b === null) continue;
      if (!a && !b) continue; // 0 nas duas semanas não diz nada
      preenchidos++;
      linhas.push({ id: l.id, rotulo: l.rotulo, formato: l.formato, melhor: l.melhor, kpi: l.kpi, atual: a, anterior: b });
    }
    if (!linhas.length) continue;
    grupos.push({ titulo: f.rotulo || cat.grupo, linhas });
    if (!plataformas.includes(NOME_PLATAFORMA[f.slug])) plataformas.push(NOME_PLATAFORMA[f.slug]);
    if (!fontes.includes(FONTE_PLATAFORMA[f.slug])) fontes.push(FONTE_PLATAFORMA[f.slug]);
  }

  let grafico = null;
  const g = dados.grafico;
  if (g && (g.atual || []).some((x) => !vazio(x.valor))) {
    const f = m.fontes.find((x) => x.id === g.fonte);
    const meta = METRICAS[f.slug].graficos[g.tipo];
    const limpa = (arr) => (arr || []).map((x) => ({ data: x.data, valor: vazio(x.valor) ? 0 : Number(x.valor) }));
    grafico = { titulo: g.titulo || meta.titulo, subtitulo: g.subtitulo || meta.subtitulo, formato: meta.formato, anterior: limpa(g.anterior), atual: limpa(g.atual) };
  }

  const fora = m.fontes.filter((x) => !x.ativa).map((x) => `${FONTE_PLATAFORMA[x.slug]} (${x.conta})`);
  let fonte = `Fonte: Reportei (${fontes.join(', ')}). Variações comparam a semana atual com a semana anterior, de segunda a domingo.`;
  if (fora.length) fonte += ` Fora deste relatório por estar desconectado no Reportei: ${fora.join('; ')}.`;
  if (dados.texto && dados.texto.fonte_extra) fonte += ' ' + dados.texto.fonte_extra;

  const texto = {};
  for (const [k, v] of Object.entries(dados.texto || {})) {
    if (vazio(v) || (Array.isArray(v) && !v.length)) continue;
    texto[k] = v;
  }

  return {
    preenchidos,
    relatorio: {
      ficticio: !!dados.ficticio,
      marca: m.nome,
      periodo: dados.periodo,
      plataformas,
      grupos,
      grafico,
      texto,
      conteudo: dados.conteudo || null,
      fonte,
    },
  };
}

// ---------- render ----------
async function abrirNavegador() {
  const require = createRequire(import.meta.url);
  let pw;
  try { pw = require('playwright'); } catch { pw = await import('playwright'); }
  return pw.chromium.launch();
}

async function renderizar(browser, relatorio, destinoPdf, opcoes = {}) {
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: opcoes.escala || 1 });
  await page.addInitScript((r) => { window.RELATORIO = r; }, relatorio);
  const erros = [];
  page.on('pageerror', (e) => erros.push(e.message));
  await page.goto(pathToFileURL(join(AQUI, 'template', 'relatorio.html')).href);
  try {
    await page.waitForFunction(() => window.__pronto === true, null, { timeout: 20000 });
  } catch (e) {
    throw new Error(`Template não terminou de montar${erros.length ? ': ' + erros.join(' | ') : ''}`);
  }
  mkdirSync(dirname(destinoPdf), { recursive: true });
  await page.pdf({ path: destinoPdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
  const paginas = await page.locator('.page').count();
  if (opcoes.png) {
    for (let i = 0; i < paginas; i++) {
      await page.locator('.page').nth(i).screenshot({ path: destinoPdf.replace(/\.pdf$/, `-p${i + 1}.png`) });
    }
  }
  await page.close();
  return paginas;
}

const MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
function nomeArquivo(nomeMarca, per) {
  const [y, mo, d1] = per.atual.inicio.split('-').map(Number);
  const [, mo2, d2] = per.atual.fim.split('-').map(Number);
  const faixa = mo === mo2 ? `${String(d1).padStart(2, '0')}-${String(d2).padStart(2, '0')}${MESES[mo - 1]}${y}`
    : `${String(d1).padStart(2, '0')}${MESES[mo - 1]}-${String(d2).padStart(2, '0')}${MESES[mo2 - 1]}${y}`;
  const slug = nomeMarca.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Za-z0-9]+/g, '-').replace(/^-|-$/g, '');
  return `Relatorio-Semanal_${slug}_${faixa}.pdf`;
}

// ---------- comandos ----------
const [cmd = 'ajuda', ...args] = process.argv.slice(2);
const png = args.includes('--png');
const posicionais = args.filter((a) => !a.startsWith('--'));

if (cmd === 'modelo') {
  const segunda = posicionais[0] || segundaPadrao();
  const pasta = join(AQUI, 'dados', segunda);
  mkdirSync(pasta, { recursive: true });
  for (const id of Object.keys(MARCAS)) {
    const arq = join(pasta, `${id}.json`);
    if (existsSync(arq)) { console.log(`= ${arq} já existe, mantido`); continue; }
    writeFileSync(arq, JSON.stringify(modelo(id, segunda), null, 2) + '\n');
    console.log(`+ ${arq}`);
  }
  const p = periodos(segunda);
  console.log(`\nSemana atual ${p.atual.inicio} a ${p.atual.fim} · anterior ${p.anterior.inicio} a ${p.anterior.fim}`);
} else if (cmd === 'pdf') {
  const segunda = posicionais[0] && /^\d{4}/.test(posicionais[0]) ? posicionais[0] : segundaPadrao();
  const filtro = posicionais.filter((a) => !/^\d{4}/.test(a));
  const pasta = join(AQUI, 'dados', segunda);
  if (!existsSync(pasta)) { console.error(`Sem dados em ${pasta}. Rode antes: node gerar.mjs modelo ${segunda}`); process.exit(1); }
  const ids = readdirSync(pasta).filter((f) => f.endsWith('.json')).map((f) => f.replace(/\.json$/, '')).filter((id) => !filtro.length || filtro.includes(id));
  const browser = await abrirNavegador();
  let falhas = 0;
  for (const id of ids) {
    const dados = JSON.parse(readFileSync(join(pasta, `${id}.json`), 'utf8'));
    const { preenchidos, relatorio } = normalizar(dados);
    if (!preenchidos) { console.log(`- ${id}: sem números preenchidos, pulado`); falhas++; continue; }
    const destino = join(AQUI, 'saida', segunda, nomeArquivo(relatorio.marca, relatorio.periodo));
    const n = await renderizar(browser, relatorio, destino, { png });
    console.log(`✓ ${id}: ${n} páginas · ${destino}`);
  }
  await browser.close();
  if (falhas) process.exitCode = 2;
} else if (cmd === 'exemplo') {
  const dados = JSON.parse(readFileSync(join(AQUI, 'exemplo-ficticio.json'), 'utf8'));
  const { relatorio } = normalizar(dados);
  const browser = await abrirNavegador();
  const destino = join(AQUI, 'saida', 'exemplo-ficticio.pdf');
  const n = await renderizar(browser, relatorio, destino, { png, escala: png ? 2 : 1 });
  await browser.close();
  console.log(`✓ exemplo: ${n} páginas · ${destino}`);
} else {
  console.log(readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').slice(1, 10).map((l) => l.replace(/^\/\/ ?/, '')).join('\n'));
}
