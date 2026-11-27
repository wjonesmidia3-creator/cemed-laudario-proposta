// Gera o "Caderno de Placar — Dominó da Família" em PDF (A4, pronto para imprimir e encadernar).
// Uso: node build.js   →  gera caderno-domino.pdf e caderno-domino.html nesta pasta.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT_DIR = __dirname;
const PLAYERS = ['Eneas C', 'Dene J', 'WJ', 'Anderson C', 'Ruxa', 'Caiu o P'];
const DIAS = 27;       // dias de jogo: frente = marcação do dia, verso = fechamento do dia
const MARK_ROWS = 15;  // linhas na página de marcação (um X por jogador em cada linha)
const ROW_H = 14.6;    // altura de cada linha (mm)
const OBS_LINES = 6;   // linhas de observação no verso

// ---------- Cores ----------
const C = {
  ink: '#1f2522', muted: '#5f6d66', green: '#1e5a46', green2: '#2f7a5e',
  tint: '#e6efea', tint2: '#f3f7f5', line: '#a7bab1', soft: '#d3ded8',
  gold: '#b07d24', cream: '#f7f2e6', pen: '#2b4a9a', xline: '#7f9f92',
};
const LVL_COLORS = ['#d9e8df', '#bcd7c8', '#9cc4ae', '#79ad92', '#569476', '#3b7a5d', '#276148', '#164634'];

// ---------- Dominó (SVG) ----------
const PIPS = {
  0: [], 1: [[1, 1]], 2: [[0, 0], [2, 2]], 3: [[0, 0], [1, 1], [2, 2]],
  4: [[0, 0], [0, 2], [2, 0], [2, 2]], 5: [[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]],
  6: [[0, 0], [1, 0], [2, 0], [0, 2], [1, 2], [2, 2]],
  7: [[0, 0], [1, 0], [2, 0], [0, 2], [1, 2], [2, 2], [1, 1]],
  8: [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]],
  9: [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]],
};
const GRID = [0.24, 0.5, 0.76];
function pips(x, y, s, n, color) {
  return PIPS[n].map(([r, c]) =>
    `<circle cx="${(x + GRID[c] * s).toFixed(2)}" cy="${(y + GRID[r] * s).toFixed(2)}" r="${(s * 0.088).toFixed(2)}" fill="${color}"/>`
  ).join('');
}
function tile(x, y, s, a, b, vertical = false, opt = {}) {
  const w = vertical ? s : 2 * s, h = vertical ? 2 * s : s;
  const sw = opt.stroke || s * 0.045;
  const pip = opt.pip || C.ink;
  const shadow = opt.shadow === false ? '' :
    `<rect x="${x + s * 0.06}" y="${y + s * 0.08}" width="${w}" height="${h}" rx="${s * 0.14}" fill="${opt.shadowColor || C.tint}"/>`;
  const divider = vertical
    ? `<line x1="${x + s * 0.12}" y1="${y + s}" x2="${x + s * 0.88}" y2="${y + s}" stroke="${C.ink}" stroke-width="${sw * 0.8}"/>`
    : `<line x1="${x + s}" y1="${y + s * 0.12}" x2="${x + s}" y2="${y + s * 0.88}" stroke="${C.ink}" stroke-width="${sw * 0.8}"/>`;
  const spinner = opt.spinner === false ? '' :
    `<circle cx="${vertical ? x + s / 2 : x + s}" cy="${vertical ? y + s : y + s / 2}" r="${s * 0.055}" fill="${C.gold}"/>`;
  const second = vertical ? pips(x, y + s, s, b, pip) : pips(x + s, y, s, b, pip);
  return `${shadow}<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${s * 0.14}" fill="#fff" stroke="${C.ink}" stroke-width="${sw}"/>${divider}${pips(x, y, s, a, pip)}${second}${spinner}`;
}
function tileSvg(a, b, s, vertical = false, opt = {}) {
  const pad = s * 0.12;
  const w = (vertical ? s : 2 * s) + pad * 2, h = (vertical ? 2 * s : s) + pad * 2;
  return `<svg class="${opt.cls || ''}" viewBox="0 0 ${w} ${h}" width="${w}mm" height="${h}mm">${tile(pad, pad, s, a, b, vertical, opt)}</svg>`;
}
// Meia-pedra quadrada com N pontos (usada como selo de nível 1–8)
function badge(n, size = 12, fill, pipColor) {
  const s = 10;
  return `<svg class="badge" viewBox="0 0 ${s} ${s}" width="${size}mm" height="${size}mm">
    <rect x="0.3" y="0.3" width="${s - 0.6}" height="${s - 0.6}" rx="1.6" fill="${fill}" stroke="${C.ink}" stroke-width="0.35"/>
    ${pips(0, 0, s, n, pipColor)}</svg>`;
}
const lvlBadge = (n, size) => badge(n, size, LVL_COLORS[n - 1], n <= 3 ? C.ink : '#fff');

// "X" feito à mão (exemplos)
let seed = 7;
const rnd = () => ((seed = (seed * 9301 + 49297) % 233280) / 233280);
function handX(w = 9, h = 8) {
  const j = () => (rnd() - 0.5) * 1.1;
  const m = 1.8;
  return `<svg class="hx" viewBox="0 0 ${w} ${h}" width="${w}mm" height="${h}mm"><g stroke="${C.pen}" stroke-width="0.55" stroke-linecap="round" fill="none">
    <path d="M${m + j()} ${m + j()} Q ${w / 2 + j()} ${h / 2 + j()} ${w - m + j()} ${h - m + j()}"/>
    <path d="M${w - m + j()} ${m + j()} Q ${w / 2 + j()} ${h / 2 + j()} ${m + j()} ${h - m + j()}"/></g></svg>`;
}

// ---------- Ícones ----------
const ICON = {
  eye: `<svg viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3.2"/></svg>`,
  ahead: `<svg viewBox="0 0 24 24"><path d="M4 6l6 6-6 6"/><path d="M12 6l6 6-6 6"/></svg>`,
  fork: `<svg viewBox="0 0 24 24"><path d="M12 21v-7"/><path d="M12 14L6 6"/><path d="M12 14l6-8"/><circle cx="18" cy="5" r="1.6"/><path d="M4.5 4.5l3 3M7.5 4.5l-3 3"/></svg>`,
  adapt: `<svg viewBox="0 0 24 24"><path d="M20 11a8 8 0 0 0-14.3-4.9L4 8"/><path d="M4 3v5h5"/><path d="M4 13a8 8 0 0 0 14.3 4.9L20 16"/><path d="M20 21v-5h-5"/></svg>`,
  trophy: `<svg viewBox="0 0 24 24"><path d="M7 4h10v5a5 5 0 0 1-10 0V4z"/><path d="M7 6H4v1a3 3 0 0 0 3 3M17 6h3v1a3 3 0 0 1-3 3"/><path d="M12 14v4M8 21h8M9 18h6"/></svg>`,
};

// ---------- Peças comuns ----------
const ALL_TILES = [];
for (let a = 0; a <= 6; a++) for (let b = a; b <= 6; b++) ALL_TILES.push([a, b]);
let pageNo = 0;
function footer(label = 'Caderno de Placar') {
  pageNo++;
  const [a, b] = ALL_TILES[(pageNo * 5) % ALL_TILES.length];
  return `<footer class="foot"><span>Dominó da Família · ${label}</span>${tileSvg(a, b, 2.6, false, { shadow: false, stroke: 0.14 })}<span class="pg">${pageNo}</span></footer>`;
}
const blank = (w) => `<span class="blank" style="width:${w}mm"></span>`;

// ---------- Páginas ----------
function cover() {
  const chain = [
    [2, 5, false], [5, 5, true], [5, 3, false], [3, 6, false], [6, 6, true], [6, 1, false],
  ];
  const s = 14.5, gap = 1.6;
  let x = 1.5, parts = '';
  for (const [a, b, v] of chain) {
    const y = v ? 2 : 2 + s / 2;
    parts += tile(x, y, s, a, b, v, { stroke: 0.55 });
    x += (v ? s : 2 * s) + gap;
  }
  const chainW = x + 1.5, chainH = 2 * s + 5;
  pageNo++;
  return `<div class="page cover">
    <div class="frame"><div class="frame-in">
      <div class="cv-kicker"><i></i>Caderno de Placar<i></i></div>
      <h1 class="cv-title">Dominó</h1>
      <div class="cv-sub">da Família</div>
      <p class="cv-tag">Partidas, vitórias e a evolução da leitura de jogo</p>
      <svg class="cv-chain" viewBox="0 0 ${chainW} ${chainH}" width="${chainW}mm" height="${chainH}mm">${parts}</svg>
      <div class="cv-fields">
        <div>Caderno nº ${blank(16)}</div>
        <div>Início ${blank(9)}/${blank(9)}/${blank(14)}</div>
        <div>Fim ${blank(9)}/${blank(9)}/${blank(14)}</div>
      </div>
    </div></div>
  </div>`;
}

const LEVELS = [
  ['Iniciante', '0–10%', 'A pessoa acompanha o que está acontecendo, mas não consegue interpretar muito além da ação imediata.',
    ['Reage em vez de antecipar.', 'Tem dificuldade de identificar padrões.', 'Decide principalmente por instinto.']],
  ['Consciente', '10–25%', 'Começa a entender por que as jogadas acontecem.',
    ['Identifica erros e oportunidades.', 'Percebe movimentos dos adversários.', 'Entende situações básicas de jogo.']],
  ['Intermediário', '25–40%', 'Já consegue enxergar possibilidades antes de elas acontecerem.',
    ['Antecipa algumas jogadas.', 'Reconhece padrões recorrentes.', 'Entende melhor posicionamento e espaço.']],
  ['Avançado', '40–55%', 'Começa a pensar vários movimentos à frente.',
    ['Prevê comportamentos.', 'Calcula riscos rapidamente.', 'Identifica intenções dos adversários.']],
  ['Competitivo', '55–70%', 'Tem leitura superior à maioria dos praticantes.',
    ['Processa várias informações simultaneamente.', 'Ajusta estratégias durante a partida.', 'Antecipa situações complexas.']],
  ['Elite', '70–85%', 'A leitura começa a parecer intuitiva.',
    ['Reconhece situações antes dos demais.', 'Identifica padrões quase automaticamente.', 'Toma decisões muito rápidas sob pressão.']],
  ['Excepcional', '85–95%', 'Capacidade encontrada em atletas de referência mundial.',
    ['Antecipa sequências de acontecimentos.', 'Manipula o comportamento do adversário.', 'Enxerga oportunidades que outros não percebem.']],
  ['Extraordinário', '95–100%', 'O limite teórico da leitura de jogo humano.',
    ['Combina antecipação, estratégia e adaptação.', 'Parece estar sempre um passo à frente.', 'Consegue mudar o rumo de uma partida pela inteligência de jogo.']],
];
const SCALE = [0, 10, 25, 40, 55, 70, 85, 95, 100];

function levelsPage1() {
  const segs = LEVELS.map((_, i) =>
    `<div class="seg" style="flex:${SCALE[i + 1] - SCALE[i]};background:${LVL_COLORS[i]};color:${i <= 2 ? C.ink : '#fff'}">${i + 1}</div>`).join('');
  const ticks = SCALE.slice(0, -1).map((v) => `<span style="left:${v}%">${v}%</span>`).join('');
  const cards = LEVELS.map(([name, pct, desc, bullets], i) => `
    <article class="lvl" style="--c:${LVL_COLORS[i]}">
      <header>${lvlBadge(i + 1, 11)}
        <div class="lvl-id"><span class="lvl-n">Nível ${i + 1}</span><span class="lvl-name">${name}</span></div>
        <span class="lvl-pct">${pct}</span></header>
      <p class="lvl-desc">${desc}</p>
      <ul>${bullets.map((b) => `<li>${b}</li>`).join('')}</ul>
    </article>`).join('');
  return `<div class="page levels">
    <div class="kicker">Escala de desenvolvimento · inteligência de jogo</div>
    <h1 class="h1">Ranking de domínio da <em>leitura de jogo</em></h1>
    <p class="lead">Vou criar uma escala de desenvolvimento da inteligência de jogo, desde uma pessoa que apenas reage ao que acontece até um atleta de elite que consegue antecipar cenários, ler adversários e tomar decisões quase intuitivamente.</p>
    <div class="scale"><div class="bar">${segs}</div><div class="ticks">${ticks}</div></div>
    <div class="lvl-grid">${cards}</div>
    <p class="note"><b>Importante:</b> os percentuais são uma escala ilustrativa de desenvolvimento, não medidas científicas ou percentis de atletas.</p>
    ${footer('Leitura de jogo')}
  </div>`;
}

function staircase() {
  const bw = 15, gap = 4.6, base = 50, unit = 4.9;
  const top = (i) => base - (unit * (i + 1) + 4);
  let bars = '';
  for (let i = 0; i < 8; i++) {
    const x = i * (bw + gap), h = base - top(i);
    const on = i >= 2 && i <= 6;
    bars += `<rect x="${x}" y="${top(i)}" width="${bw}" height="${h}" rx="1.4" fill="${on ? LVL_COLORS[i] : '#fff'}" stroke="${on ? C.ink : C.line}" stroke-width="${on ? 0.35 : 0.3}" ${on ? '' : 'stroke-dasharray="1 0.8"'}/>`;
    bars += `<text x="${x + bw / 2}" y="${base + 5.2}" text-anchor="middle" class="st-n" fill="${on ? C.ink : C.muted}">Nível ${i + 1}</text>`;
    bars += `<text x="${x + bw / 2}" y="${base + 9.2}" text-anchor="middle" class="st-s" fill="${C.muted}">${LEVELS[i][0]}</text>`;
  }
  const x3 = 2 * (bw + gap) + bw / 2, x7 = 6 * (bw + gap) + bw / 2;
  const y3 = top(2) - 2.5, y7 = top(6) - 2.5;
  const arrow = `<path d="M${x3} ${y3} C ${x3 + 6} ${y7 - 2}, ${x7 - 30} ${y7 - 9}, ${x7 - 2} ${y7 - 1}" fill="none" stroke="${C.gold}" stroke-width="0.75" stroke-linecap="round"/>
    <path d="M${x7 - 5.6} ${y7 - 3.6} L${x7 - 1.6} ${y7 - 0.9} L${x7 - 5.8} ${y7 + 1.4}" fill="none" stroke="${C.gold}" stroke-width="0.75" stroke-linecap="round" stroke-linejoin="round"/>`;
  const W = 8 * bw + 7 * gap;
  const lx = (x3 + x7) / 2 - 6;
  return `<svg class="stairs" viewBox="-1 -6 ${W + 2} ${base + 17}" width="${W + 2}mm" height="${base + 17}mm">${bars}${arrow}
    <text x="${lx}" y="${y7 - 9.5}" text-anchor="middle" class="st-l" fill="${C.gold}">o caminho proposto</text></svg>`;
}

function levelsPage2() {
  const caps = [
    ['eye', 'Percepção', 'enxergar o que está acontecendo.'],
    ['ahead', 'Antecipação', 'prever o que vai acontecer.'],
    ['fork', 'Decisão', 'escolher a melhor resposta.'],
    ['adapt', 'Adaptação', 'mudar a estratégia conforme o jogo evolui.'],
  ];
  return `<div class="page levels2">
    <div class="kicker">Leitura de jogo</div>
    <h2 class="h2">Até onde uma pessoa consegue chegar?</h2>
    <div class="two">
      <p class="big">Uma pessoa comum, com treinamento deliberado, experiência e análise de partidas, pode desenvolver uma leitura muito acima da média.</p>
      <p class="big">O nível de elite exige algo a mais: milhares de situações vividas, memória de padrões, conhecimento específico da modalidade e capacidade de executar decisões sob pressão.</p>
    </div>

    <div class="rule"></div>
    <h2 class="h2">Uma distinção importante</h2>
    <p class="body">Existem quatro capacidades diferentes que formam essa inteligência:</p>
    <div class="caps">${caps.map(([ic, t, d], i) => `
      <div class="cap"><div class="cap-ic">${ICON[ic]}</div><div class="cap-n">0${i + 1}</div>
        <div class="cap-t">${t}</div><div class="cap-d">${d}</div></div>`).join('')}
    </div>
    <p class="body">Uma pessoa pode ser excelente em antecipação, mas ruim na execução. Por isso, leitura de jogo não é sinônimo de habilidade física ou técnica.</p>

    <div class="proposal">
      <div class="prop-text">
        <div class="kicker gold">Minha proposta</div>
        <p>Podemos desenvolver um método de treinamento para levar alguém do <b>nível 3</b> ao <b>nível 7</b>, usando exercícios de percepção, previsão, tomada de decisão e análise de padrões.</p>
        <div class="chips"><span>Percepção</span><span>Previsão</span><span>Tomada de decisão</span><span>Análise de padrões</span></div>
      </div>
      <div class="prop-viz">${staircase()}</div>
    </div>
    ${footer('Leitura de jogo')}
  </div>`;
}

// X impresso em cada quadradinho (fundo SVG vetorial)
const dot = (r = 1.15) => `<svg class="dot" viewBox="0 0 4 4" width="${r * 2}mm" height="${r * 2}mm"><circle cx="2" cy="2" r="1.75" fill="${C.pen}"/></svg>`;

// Um X por jogador em cada linha (desenhado na proporção da célula)
function xCell(w, h, xw, xh, dots = 0, wFull = false) {
  const x0 = (w - xw) / 2, y0 = (h - xh) / 2, x1 = x0 + xw, y1 = y0 + xh;
  const tips = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
  const d = tips.slice(0, dots).map(([x, y]) => `<circle cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="1.2" fill="${C.pen}"/>`).join('');
  return `<svg viewBox="0 0 ${w} ${h}" width="${wFull ? '100%' : w + 'mm'}" height="${h}mm"><path d="M${x0.toFixed(2)} ${y0.toFixed(2)}L${x1.toFixed(2)} ${y1.toFixed(2)}M${x1.toFixed(2)} ${y0.toFixed(2)}L${x0.toFixed(2)} ${y1.toFixed(2)}" stroke="${C.xline}" stroke-width="0.5" stroke-linecap="round" fill="none"/>${d}</svg>`;
}

// Grade de marcação: nomes fixos + "outro:" no cabeçalho, linhas com um X por jogador
function markGrid(o) {
  const names = o.names || PLAYERS;
  const th = names.map((p, i) => `<th class="name">${o.struck === i ? `<span class="struck">${p}${o.strikeSvg}</span>` : p}</th>`).join('');
  const subs = names.map((_, i) => `<th class="sub"><div><span>outro:</span><i>${o.sub && o.sub[i] ? `<b class="hand">${o.sub[i]}</b>` : ''}</i></div></th>`).join('');
  let body = '';
  for (let r = 0; r < o.rows; r++) {
    body += `<tr><td class="rn">${r + 1}</td>${names.map((_, p) => `<td class="x">${xCell(o.colW, o.rowH, o.xw, o.xh, o.dots ? (o.dots[p][r] || 0) : 0, true)}</td>`).join('')}</tr>`;
  }
  return `<div class="gridwrap${o.cls ? ' ' + o.cls : ''}"><table class="grid mk">
    <colgroup><col style="width:${o.rnW}mm">${names.map(() => '<col>').join('')}</colgroup>
    <thead><tr class="names"><th class="corner" rowspan="2"><span>linha</span></th>${th}</tr><tr class="subs">${subs}</tr></thead>
    <tbody>${body}</tbody></table></div>`;
}

function howToPage() {
  const strike = `<svg class="strike" viewBox="0 0 30 6" preserveAspectRatio="none"><path d="M1 3.6 Q 10 2.2 18 3.2 T 29 2.6" stroke="${C.pen}" stroke-width="0.9" fill="none" stroke-linecap="round"/></svg>`;
  const example = `<div class="ex">${markGrid({
    names: ['Fulano', 'Beltrano', 'Sicrano'], rows: 3, rnW: 7, colW: 25, rowH: 11, xw: 11, xh: 7.6,
    dots: [[4, 2], [4, 4, 1], [3]], struck: 1, strikeSvg: strike, sub: [null, 'Visita', null],
  })}</div>`;
  const steps = [
    ['Um X por jogador em cada linha', 'Cada jogador tem a sua coluna, separada por uma linha. Quando alguém fizer um ponto, coloque uma bolinha no X dessa pessoa. Quando o X encher, passe para o X da linha de baixo.'],
    ['Entrou outra pessoa?', 'Risque o nome de quem não jogou e escreva o novo jogador na linha “outro:”, logo abaixo. Os nomes da família continuam impressos em todas as páginas.'],
    ['Feche o dia no verso', 'No verso fica o fechamento do dia: conte as bolinhas de cada um, preencha o placar e monte o pódio e o ranking. O 1º lugar é o campeão(ã) do dia. Os dias de jogo são numerados em ordem (1, 2, 3…) e a data vai no campo Data. No fim do caderno vem o fechamento do mês.'],
  ];
  const lvlHead = [1, 2, 3, 4, 5, 6, 7, 8].map((n) => `<th>${lvlBadge(n, 6.2)}</th>`).join('');
  const lvlRows = PLAYERS.map((p, i) => `<tr><td class="pl"><div class="plc">${badge(i + 1, 5, '#fff', C.green)}<span>${p}</span></div></td>${'<td></td>'.repeat(8)}<td></td></tr>`).join('')
    + [1, 2].map(() => `<tr><td class="pl other"><div class="plc"><span>outro:</span><i></i></div></td>${'<td></td>'.repeat(8)}<td></td></tr>`).join('');
  return `<div class="page howto">
    <div class="kicker">Antes de começar</div>
    <h2 class="h2">Como marcar os pontos</h2>
    <div class="howto-top">
      <ol class="steps">${steps.map(([t, d], i) => `<li>${badge(i + 1, 7.5, C.tint, C.green)}<div><b>${t}</b><p>${d}</p></div></li>`).join('')}</ol>
      <div class="ex-col"><div class="ex-label">Exemplo</div>${example}
        <p class="ex-cap">Fulano fez 6 pontos, a Visita fez 9 e Sicrano fez 3. Beltrano não jogou e foi riscado; a Visita entrou no lugar dele.</p></div>
    </div>
    <div class="rule"></div>
    <div class="kicker">Leitura de jogo</div>
    <h2 class="h2">Onde cada um está hoje</h2>
    <p class="body">Consulte o ranking das páginas anteriores e marque com um X o nível de leitura de jogo de cada jogador. De tempos em tempos, reavalie com todos e anote a data.</p>
    <table class="lvltable"><thead><tr><th class="pl">Jogador</th>${lvlHead}<th class="dt">Data</th></tr></thead><tbody>${lvlRows}</tbody></table>
    ${footer()}
  </div>`;
}

function sheetHead(n, side, title) {
  return `<div class="sheet-head">
      <div class="sh-left">${tileSvg(n % 7, (n * 3) % 7, 3.6, true, { shadow: false, stroke: 0.18, cls: 'dh-tile' })}
        <div><div class="kicker">${side}</div><h2 class="h2 sm">${title}</h2></div></div>
      <div class="sh-no"><span>Dia de<br>jogo</span><b>${n}</b></div>
    </div>`;
}
const WEEK = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB', 'DOM'].map((d) => `<span>${d}</span>`).join('');
const dateFields = (local = true) => `<div class="sheet-fields">
      <div class="fld">Data ${blank(8)}/${blank(8)}/${blank(13)}</div>
      <div class="wk">${WEEK}</div>
      ${local ? '<div class="fld grow">Local <span class="blank flex"></span></div>' : ''}
    </div>`;

// Pódio 2º · 1º · 3º (o 1º lugar é o campeão)
function podium(champLabel, heights = [24, 33, 17]) {
  const order = [[2, heights[0]], [1, heights[1]], [3, heights[2]]];
  return `<div class="podium">${order.map(([n, h]) => `
    <div class="pod p${n}">
      <div class="pod-name">${n === 1 ? `<span class="pod-crown">${ICON.trophy}${champLabel}</span>` : ''}<span class="pod-line"></span><small>pontos ${blank(9)}</small></div>
      <div class="pod-step" style="height:${h}mm"><span>${n}º</span></div>
    </div>`).join('')}</div>`;
}
const rankRows = (from, to) => Array.from({ length: to - from + 1 }, (_, i) =>
  `<div class="rk-row"><span class="rk-pos">${from + i}º</span><span class="rk-name"></span><span class="rk-pts">pts</span></div>`).join('');

// Frente do dia: página inteira de marcação, um X por jogador em cada linha
function markPage(n) {
  return `<div class="page mark">
    ${sheetHead(n, 'Frente · marcação', 'Marcação do dia')}
    ${dateFields(true)}
    ${markGrid({ rows: MARK_ROWS, rnW: 8, colW: 28.2, rowH: ROW_H, xw: 15, xh: 10.4 })}
    <div class="mark-foot">
      <span class="legend">${xCell(9, 7, 6, 4.2, 1)}Ponto feito: uma bolinha no X de quem fez o ponto</span>
      <span class="turn">No verso: fechamento do dia ${n} →</span>
    </div>
    ${footer('Dia ' + n + ' · marcação')}
  </div>`;
}

// Verso do dia: fechamento do dia (placar + pódio + ranking do campeão)
function dayClosePage(n) {
  const row = (label) => `<tr>${label}<td class="pf"></td><td></td><td class="tt"></td><td class="pos"><span>º</span></td></tr>`;
  const rows = PLAYERS.map((p, i) => row(`<td class="pl"><div class="plc">${badge(i + 1, 5, '#fff', C.green)}<span>${p}</span></div></td>`)).join('')
    + [1, 2].map(() => row(`<td class="pl other"><div class="plc"><span>outro:</span><i></i></div></td>`)).join('');
  return `<div class="page dayclose">
    ${sheetHead(n, 'Verso · fechamento', 'Fechamento do dia')}
    ${dateFields(false)}
    <div class="sub-h">Placar do dia</div>
    <table class="mtable ptable"><thead><tr><th class="pl">Jogador</th><th class="pf">Pontos<br>do dia</th><th>Vem do<br>dia anterior</th><th class="tt">Total<br>no mês</th><th class="pos">Posição<br>do dia</th></tr></thead><tbody>${rows}</tbody></table>
    <p class="hint">Pontos do dia = bolinhas da frente. Total no mês = pontos do dia + o que vem do dia anterior.</p>
    <div class="close-mid">
      <div><div class="sub-h">Pódio do dia</div>${podium('Campeão(ã) do dia')}</div>
      <div><div class="sub-h">Ranking do dia</div>${rankRows(4, 8)}
        <div class="hl dest1"><span>Destaque do dia</span><span class="blank flex"></span></div></div>
    </div>
    <div class="sub-h">Anotações</div>
    <div class="lines">${'<i></i>'.repeat(OBS_LINES)}</div>
    ${footer('Dia ' + n + ' · fechamento')}
  </div>`;
}

// Fechamento do mês: uma linha por dia
function monthClosePage() {
  const head = PLAYERS.map((p) => `<th class="op">${p}</th>`).join('') + '<th class="op oo"><span>outro:</span><i></i></th>';
  const cols = PLAYERS.length + 1;
  let rows = '';
  for (let d = 1; d <= DIAS; d++) rows += `<tr><td class="of">${d}</td>${'<td class="op"></td>'.repeat(cols)}<td class="oc"></td></tr>`;
  return `<div class="page overview">
    <div class="kicker">Fim do caderno</div>
    <h2 class="h2">Fechamento do mês</h2>
    <div class="mfields"><div class="fld">Mês ${blank(40)}</div><div class="fld">Ano ${blank(18)}</div></div>
    <p class="body">Copie os pontos de cada dia de jogo (coluna “Pontos do dia” no verso) e o nome do campeão(ã) do dia. Quem jogou no lugar de alguém entra na coluna “outro”. No fim, some as colunas.</p>
    <table class="otable"><thead><tr><th class="of">Dia</th>${head}<th class="oc">Campeão(ã) do dia</th></tr></thead>
      <tbody>${rows}</tbody>
      <tfoot><tr class="sum"><td class="of">Total</td>${'<td class="op"></td>'.repeat(cols)}<td class="oc ghost"></td></tr>
      <tr class="psn"><td class="of">Posição</td>${'<td class="op"><span>º</span></td>'.repeat(cols)}<td class="oc ghost"></td></tr></tfoot>
    </table>
    ${footer('Fechamento do mês')}
  </div>`;
}

// Ranking do mês: pódio, destaques e assinaturas
function finalPage() {
  const row = (label) => `<tr>${label}<td class="tt"></td><td></td><td class="pos"><span>º</span></td><td class="lv"></td></tr>`;
  const rows = PLAYERS.map((p, i) => row(`<td class="pl"><div class="plc">${badge(i + 1, 5, '#fff', C.green)}<span>${p}</span></div></td>`)).join('')
    + [1, 2].map(() => row(`<td class="pl other"><div class="plc"><span>outro:</span><i></i></div></td>`)).join('');
  const records = [
    'Mais pontos em um único dia', 'Maior sequência de pontos', 'Mais dias como campeão(ã)',
    'Dia mais disputado', 'Maior evolução de nível', 'Partida inesquecível',
  ].map((t) => `<div class="hl"><span>${t}</span><span class="blank flex"></span></div>`).join('');
  const sigs = PLAYERS.map((p) => `<div class="sig"><i></i><span>${p}</span></div>`).join('');
  return `<div class="page final">
    <div class="kicker">Fechamento do mês</div>
    <h2 class="h2">Ranking do mês</h2>
    <table class="mtable"><thead><tr><th class="pl">Jogador</th><th class="tt">Total de pontos</th><th>Dias como campeão(ã)</th><th class="pos">Posição</th><th class="lv">Nível de leitura</th></tr></thead><tbody>${rows}</tbody></table>
    <div class="final-mid">
      <div><div class="sub-h">Pódio do mês</div>${podium('Campeão(ã) do mês', [30, 40, 21])}</div>
      <div><div class="sub-h">Destaques do mês</div>${records}</div>
    </div>
    <div class="sub-h">Assinaturas da mesa</div>
    <div class="sigs">${sigs}</div>
    ${footer('Fechamento do mês')}
  </div>`;
}

// ---------- CSS ----------
const font = (fam, file, weight, style = 'normal') =>
  `@font-face{font-family:'${fam}';src:url('fonts/${file}') format('woff2');font-weight:${weight};font-style:${style};}`;
const CSS = `
${font('Fraunces', 'fraunces-latin-400-normal.woff2', 400)}
${font('Fraunces', 'fraunces-latin-600-normal.woff2', 600)}
${font('Fraunces', 'fraunces-latin-700-normal.woff2', 700)}
${font('Fraunces', 'fraunces-latin-900-normal.woff2', 900)}
${font('Fraunces', 'fraunces-latin-400-italic.woff2', 400, 'italic')}
${font('Fraunces', 'fraunces-latin-600-italic.woff2', 600, 'italic')}
${font('Caveat', 'caveat-latin-600-normal.woff2', 600)}
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:Inter,'DejaVu Sans',sans-serif;color:${C.ink};font-size:9pt;line-height:1.4;background:#fff}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;break-after:page;padding:12mm 16mm 14mm}
.page:last-child{page-break-after:auto;break-after:auto}
svg{display:block}
.foot{position:absolute;left:16mm;right:16mm;bottom:6mm;display:flex;align-items:center;justify-content:space-between;font-size:6.5pt;color:${C.muted};letter-spacing:.02em}
.foot svg{position:absolute;left:50%;transform:translateX(-50%)}
.foot .pg{font-variant-numeric:tabular-nums;font-weight:600;color:${C.green}}
.blank{display:inline-block;border-bottom:.25mm solid ${C.ink};height:1em;vertical-align:baseline;margin:0 .6mm}
.blank.flex{flex:1;min-width:10mm}
.fld{display:flex;align-items:baseline;white-space:nowrap;font-size:8pt;color:${C.muted};font-weight:500}
.fld .blank{border-color:${C.line}}
.fld.grow{flex:1}
.kicker{font-size:7pt;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:${C.green};margin-bottom:1.5mm}
.kicker.gold{color:${C.gold}}
.h1{font-family:Fraunces,serif;font-weight:700;font-size:25pt;line-height:1.05;letter-spacing:-.01em;margin-bottom:3mm}
.h1 em{font-style:italic;font-weight:600;color:${C.green}}
.h2{font-family:Fraunces,serif;font-weight:700;font-size:19pt;line-height:1.1;margin-bottom:3mm}
.body{font-size:9pt;color:#36403b;max-width:165mm;margin-bottom:3mm}
.rule{height:0;border-top:.25mm solid ${C.soft};margin:6mm 0 5mm}
.sub-h{font-family:Fraunces,serif;font-weight:600;font-size:12pt;margin:0 0 2.5mm}

/* ---- Capa ---- */
.cover{padding:10mm}
.frame{height:100%;border:.7mm solid ${C.green};border-radius:5mm;padding:1.6mm}
.frame-in{height:100%;border:.25mm solid ${C.green};border-radius:3.6mm;display:flex;flex-direction:column;align-items:center;padding:24mm 14mm 14mm;text-align:center;
  background:radial-gradient(ellipse at 50% 38%, ${C.tint2} 0%, #fff 62%)}
.cv-kicker{display:flex;align-items:center;gap:4mm;font-size:9pt;font-weight:700;letter-spacing:.32em;text-transform:uppercase;color:${C.green}}
.cv-kicker i{display:block;width:16mm;border-top:.3mm solid ${C.gold}}
.cv-title{font-family:Fraunces,serif;font-weight:900;font-size:92pt;line-height:.95;letter-spacing:-.02em;margin-top:8mm;color:${C.ink}}
.cv-sub{font-family:Fraunces,serif;font-style:italic;font-weight:400;font-size:38pt;line-height:1;color:${C.green};margin-top:1mm}
.cv-tag{margin-top:6mm;font-size:10.5pt;color:${C.muted};letter-spacing:.02em}
.cv-chain{margin:auto 0}
.cv-fields{margin-top:20mm;display:flex;gap:9mm;font-size:9pt;color:${C.muted}}
.cv-fields>div{display:flex;align-items:baseline}
.cv-fields .blank{border-color:${C.line}}

/* ---- Níveis ---- */
.lead{font-family:Fraunces,serif;font-size:11pt;line-height:1.45;color:#3a4540;max-width:168mm;margin-bottom:5mm}
.scale{margin-bottom:7mm}
.scale .bar{display:flex;height:6mm;border-radius:1.5mm;overflow:hidden;border:.25mm solid ${C.ink}}
.scale .seg{display:flex;align-items:center;justify-content:center;font-weight:700;font-size:7.5pt;border-right:.25mm solid rgba(0,0,0,.35)}
.scale .seg:last-child{border-right:0}
.scale .ticks{position:relative;height:4mm;margin-top:1mm}
.scale .ticks span{position:absolute;transform:translateX(-50%);font-size:6pt;color:${C.muted};font-variant-numeric:tabular-nums}
.scale .ticks span:first-child{transform:none}
.lvl-grid{display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:44.5mm;gap:3.6mm 4mm}
.lvl{border:.25mm solid ${C.soft};border-left:1.6mm solid var(--c);border-radius:2mm;padding:3mm 3.5mm 2.5mm 3.2mm;background:#fff}
.lvl header{display:flex;align-items:center;gap:2.8mm;margin-bottom:2mm}
.lvl-id{display:flex;flex-direction:column;flex:1}
.lvl-n{font-size:6.5pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:${C.muted}}
.lvl-name{font-family:Fraunces,serif;font-weight:700;font-size:14pt;line-height:1.1}
.lvl-pct{font-size:7.5pt;font-weight:700;color:${C.green};background:${C.tint};border-radius:5mm;padding:.8mm 2.4mm;font-variant-numeric:tabular-nums;align-self:flex-start}
.lvl-desc{font-family:Fraunces,serif;font-style:italic;font-size:9pt;line-height:1.35;color:#36403b;margin-bottom:1.6mm}
.lvl ul{list-style:none}
.lvl li{position:relative;padding-left:3.6mm;font-size:8pt;line-height:1.38;color:#2b332f}
.lvl li::before{content:'';position:absolute;left:.4mm;top:1.45mm;width:1.4mm;height:1.4mm;border-radius:50%;background:${C.green2}}
.note{margin-top:4.5mm;font-size:7.5pt;color:${C.muted};border-top:.25mm solid ${C.soft};padding-top:2.5mm}
.note b{color:${C.ink}}

.two{display:grid;grid-template-columns:1fr 1fr;gap:7mm}
.big{font-family:Fraunces,serif;font-size:13pt;line-height:1.45;color:#2f3834;border-left:.6mm solid ${C.gold};padding-left:4mm}
.caps{display:grid;grid-template-columns:repeat(4,1fr);gap:3.5mm;margin:2mm 0 5mm}
.cap{border:.25mm solid ${C.soft};border-radius:2.4mm;padding:5mm 4mm 5.5mm;position:relative;background:${C.tint2}}
.cap-ic{width:10mm;height:10mm;border-radius:50%;background:#fff;border:.3mm solid ${C.green};display:flex;align-items:center;justify-content:center;margin-bottom:3mm}
.cap-ic svg{width:6mm;height:6mm;fill:none;stroke:${C.green};stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.cap-n{position:absolute;top:3.5mm;right:3.5mm;font-family:Fraunces,serif;font-size:10pt;color:${C.line};font-weight:600}
.cap-t{font-family:Fraunces,serif;font-weight:700;font-size:12.5pt;margin-bottom:1mm}
.cap-d{font-size:9pt;color:#36403b;line-height:1.35}
.proposal{margin-top:7mm;border:.35mm solid ${C.gold};border-radius:3mm;padding:6.5mm 7mm 5mm;background:${C.cream}}
.prop-text{margin-bottom:5mm}
.prop-text p{font-family:Fraunces,serif;font-size:13pt;line-height:1.45;margin-bottom:4mm;max-width:150mm}
.prop-text b{color:${C.green}}
.chips{display:flex;flex-wrap:wrap;gap:1.6mm}
.chips span{font-size:7.5pt;font-weight:600;color:${C.green};border:.25mm solid ${C.green};border-radius:5mm;padding:.7mm 2.4mm;background:#fff}
.prop-viz{display:flex;justify-content:center}
.st-n{font-family:Inter,sans-serif;font-size:2.7px;font-weight:700}
.st-s{font-family:Fraunces,serif;font-style:italic;font-size:2.6px}
.st-l{font-family:Fraunces,serif;font-style:italic;font-weight:600;font-size:4.4px}

/* ---- Como usar ---- */
.howto-top{display:grid;grid-template-columns:1fr 83mm;gap:7mm;align-items:start}
.steps{list-style:none;display:flex;flex-direction:column;gap:4mm}
.steps li{display:flex;gap:3mm;align-items:flex-start}
.steps li svg{flex:none}
.steps b{font-family:Fraunces,serif;font-size:11pt;font-weight:700;display:block;margin-bottom:.5mm}
.steps p{font-size:8.5pt;color:#36403b;line-height:1.4}
.ex-label{font-size:6.5pt;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:${C.pen};margin-bottom:1.5mm}
.ex-cap{font-size:7.5pt;color:${C.muted};margin-top:2mm;font-style:italic}
.hand{font-family:Caveat,cursive;font-weight:600;color:${C.pen};font-size:12pt;line-height:1}
.hand.lg{font-size:17pt}
.struck{position:relative;display:inline-block}
.strike{position:absolute;left:-1mm;right:-1mm;top:30%;width:calc(100% + 2mm);height:2.4mm}
.lvltable{width:100%;border-collapse:collapse;margin-top:1mm}
.lvltable th{font-size:6.5pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:${C.muted};padding:1.5mm 0;border-bottom:.4mm solid ${C.green}}
.lvltable th svg{margin:0 auto}
.lvltable th.pl{text-align:left;width:46mm}
.lvltable th.dt{width:26mm}
.lvltable td{height:12mm;border-bottom:.25mm solid ${C.soft};border-left:.25mm dotted ${C.line}}
.lvltable td.pl{border-left:0}

/* tabelas de jogadores (comum) */
td.pl .plc{display:flex;align-items:center;gap:2mm}
td.pl span{font-family:Fraunces,serif;font-weight:600;font-size:11pt}
td.pl.other span{font-family:Inter,sans-serif;font-size:6.5pt;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:${C.muted}}
td.pl.other i{flex:1;border-bottom:.25mm solid ${C.line};height:4mm;margin-right:3mm}

/* ---- Grade de marcação ---- */
.gridwrap{border:.45mm solid ${C.green};border-radius:2.4mm;overflow:hidden}
.grid{width:100%;border-collapse:collapse;table-layout:fixed}
.grid th,.grid td{padding:0}
.grid .names th{height:9mm;background:${C.tint};font-family:Fraunces,serif;font-weight:600;font-size:11.5pt;text-align:center;vertical-align:middle;border-left:.4mm solid ${C.green};white-space:nowrap;overflow:hidden}
.grid .subs th{height:7mm;border-left:.4mm solid ${C.green};border-bottom:.35mm solid ${C.green};font-weight:400;vertical-align:middle}
.grid .sub div{display:flex;align-items:flex-end;gap:1mm;padding:0 1.6mm 1.4mm}
.grid .sub span{font-size:5.5pt;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:${C.muted};line-height:1}
.grid .sub i{flex:1;border-bottom:.22mm solid ${C.line};height:3.6mm;font-style:normal;text-align:center;position:relative}
.grid .sub i .hand{position:absolute;left:0;right:0;bottom:-.4mm;font-size:12.5pt}
.grid .corner{background:${C.tint2};border-left:0;border-bottom:.35mm solid ${C.green};vertical-align:middle}
.grid .corner span{display:block;transform:rotate(-90deg);font-size:5pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:${C.green};white-space:nowrap;width:8mm;font-family:Inter,sans-serif}
.grid td{height:10.2mm;border-top:.2mm solid ${C.soft};text-align:center;vertical-align:middle}
.grid tbody tr:first-child td{border-top:0}
.grid td.ps{border-left:.4mm solid ${C.green}}
.grid td.rn{font-size:6pt;color:${C.muted};font-weight:600;font-variant-numeric:tabular-nums;background:${C.tint2}}
.grid td .dot{margin:0 auto}
.ex .grid .names th{font-size:10pt;height:8mm}
.ex .grid .subs th{height:6.5mm}
.grid.mk td{height:auto;border-top:.25mm solid ${C.line}}
.grid.mk td.x{border-left:.4mm solid ${C.green}}
.grid.mk td.x svg{display:block}
.grid.mk td.rn{font-size:7.5pt;color:${C.muted};font-family:Fraunces,serif;font-weight:600}
.legend svg{flex:none}

/* ---- Folha: frente ---- */
.mark,.placar{padding-top:11mm}
.sheet-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:3mm}
.sh-left{display:flex;align-items:center;gap:3mm}
.sh-left .kicker{margin-bottom:.6mm}
.h2.sm{font-size:17pt;margin:0}
.sh-no{display:flex;align-items:center;gap:2.2mm;border:.4mm solid ${C.green};border-radius:2.4mm;padding:1.4mm 3.6mm 1.4mm 3.2mm}
.sh-no span{font-size:6.5pt;line-height:1.15;text-align:right;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:${C.muted}}
.sh-no b{font-family:Fraunces,serif;font-weight:900;font-size:20pt;line-height:1;color:${C.green};font-variant-numeric:tabular-nums}
.sheet-fields{display:flex;gap:6mm;margin-bottom:3mm;align-items:baseline}
.mark-foot{display:flex;justify-content:space-between;align-items:center;margin-top:2.6mm;font-size:7.5pt;color:${C.muted}}
.legend{display:flex;align-items:center;gap:1.8mm}
.turn{font-weight:600;color:${C.green}}

/* ---- Dia: verso (fechamento) ---- */
.dayclose{padding-top:11mm}
.wk{display:flex;gap:1mm}
.wk span{font-size:6pt;font-weight:700;letter-spacing:.04em;color:${C.green};border:.25mm solid ${C.line};border-radius:1.2mm;padding:.6mm 1.1mm}
.mtable.ptable{margin:0 0 2mm}
.mtable.ptable th{line-height:1.25;vertical-align:bottom}
.mtable.ptable th.pl{width:52mm}
.mtable.ptable td{height:11.2mm}
.mtable.ptable td.pf,.mtable.ptable th.pf{background:${C.tint2}}
.hint{font-size:7pt;color:${C.muted};line-height:1.4;margin-bottom:5mm}
.close-mid{display:grid;grid-template-columns:1fr 70mm;gap:9mm;margin-bottom:5mm;align-items:start}
.podium{display:flex;align-items:flex-end;gap:2.5mm}
.pod{flex:1;display:flex;flex-direction:column;justify-content:flex-end}
.pod-name{display:flex;flex-direction:column;gap:1mm;margin-bottom:2mm}
.pod-crown{display:flex;align-items:center;gap:1mm;font-size:6pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:${C.gold};white-space:nowrap}
.pod-crown svg{width:4mm;height:4mm;fill:none;stroke:${C.gold};stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.pod-line{display:block;height:7mm;border-bottom:.3mm solid ${C.ink}}
.pod-name small{font-size:6pt;color:${C.muted};display:flex;align-items:baseline}
.pod-name small .blank{border-color:${C.line}}
.pod-step{border:.35mm solid ${C.green};border-bottom-width:.7mm;border-radius:1.6mm 1.6mm 0 0;display:flex;align-items:flex-start;justify-content:center;padding-top:2mm;background:${C.tint2}}
.pod.p1 .pod-step{background:${C.cream};border-color:${C.gold}}
.pod-step span{font-family:Fraunces,serif;font-weight:900;font-size:17pt;color:${C.green}}
.pod.p1 .pod-step span{color:${C.gold};font-size:21pt}
.rk-row{display:flex;align-items:flex-end;gap:2mm;height:9.6mm;padding-bottom:1mm;border-bottom:.25mm solid ${C.soft}}
.rk-pos{font-family:Fraunces,serif;font-weight:700;font-size:12pt;color:${C.green};width:8mm;line-height:1}
.rk-name{flex:1}
.rk-pts{width:15mm;text-align:right;font-size:6pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:${C.muted};border-left:.25mm dotted ${C.line};height:6mm;display:flex;align-items:flex-end;justify-content:flex-end}
.dest1{margin:4mm 0 0}
.final-mid{display:grid;grid-template-columns:1fr 1fr;gap:9mm;margin-bottom:9mm;align-items:start}
.mfields{display:flex;gap:9mm;margin:1mm 0 3mm}
.mfields .fld{font-size:9pt}

/* ---- Tabelas de resumo ---- */
.mtable{width:100%;border-collapse:collapse;margin:1mm 0 6mm}
.mtable th{font-size:6.5pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:${C.muted};padding:1.6mm 0;border-bottom:.4mm solid ${C.green};text-align:center}
.mtable th.pl{text-align:left;width:50mm}
.mtable td{height:11mm;border-bottom:.25mm solid ${C.soft};border-left:.25mm dotted ${C.line}}
.mtable td.pl{border-left:0}
.mtable td.tt,.mtable th.tt{background:${C.cream};border-left:.35mm solid ${C.gold}}
.mtable th.tt{color:${C.gold}}
.mtable td.pos{text-align:right;padding-right:3mm;color:${C.muted};font-size:9pt}
.mtable td.pos,.mtable th.pos{width:22mm}
.mtable td.lv,.mtable th.lv{width:24mm}
.otable{width:100%;border-collapse:collapse;table-layout:fixed;margin-top:1mm}
.otable th{font-size:6.5pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:${C.muted};padding:1.8mm 0;border-bottom:.4mm solid ${C.green};text-align:center;vertical-align:bottom}
.otable th.op{font-family:Fraunces,serif;font-size:8.5pt;font-weight:600;letter-spacing:0;text-transform:none;color:${C.ink}}
.otable th.of,.otable td.of{width:15mm}
.otable th.oc,.otable td.oc{width:34mm}
.otable th.oo{vertical-align:bottom;padding-bottom:1.4mm}
.otable th.oo span{display:block;font-family:Inter,sans-serif;font-size:5.5pt;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:${C.muted};text-align:left;padding-left:1.2mm}
.otable th.oo i{display:block;height:4mm;margin:0 1.2mm;border-bottom:.25mm solid ${C.line}}
.otable td{height:7.1mm;border-bottom:.25mm solid ${C.soft};border-left:.25mm dotted ${C.line}}
.otable td.of{border-left:0;text-align:center;font-family:Fraunces,serif;font-weight:600;font-size:9pt;color:${C.green};font-variant-numeric:tabular-nums}
.otable tbody tr:nth-child(even) td{background:${C.tint2}}
.otable tfoot td{height:9mm;border-top:.4mm solid ${C.green}}
.otable tfoot td.of{font-family:Inter,sans-serif;font-size:6.5pt;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
.otable tr.sum td.op{background:${C.cream}}
.otable tr.psn td.op{text-align:right;padding-right:2mm;color:${C.muted}}
.otable td.ghost{border:0;background:transparent}
.hl{display:flex;flex-direction:column;gap:.6mm;margin-bottom:3.4mm}
.hl span:first-child{font-size:7.5pt;font-weight:600;color:${C.muted}}
.hl .blank{width:100%;margin:0;height:5mm;border-color:${C.line}}
.lines i{display:block;height:8mm;border-bottom:.25mm solid ${C.soft}}
.champion{display:flex;align-items:center;gap:7mm;border:.35mm solid ${C.gold};border-radius:3mm;padding:5mm 7mm;background:${C.cream};margin-bottom:7mm}
.champ-body{flex:1}
.champ-line{height:13mm;border-bottom:.35mm solid ${C.ink};margin-bottom:3mm}
.champ-meta{display:flex;gap:8mm}
.records{display:grid;grid-template-columns:1fr 1fr;gap:0 8mm;margin-bottom:5mm}
.sigs{display:grid;grid-template-columns:repeat(3,1fr);gap:12mm 8mm;margin-top:6mm}
.sig i{display:block;height:9mm;border-bottom:.3mm solid ${C.ink}}
.sig span{display:block;text-align:center;font-family:Fraunces,serif;font-weight:600;font-size:10pt;margin-top:1.2mm}
`;

// ---------- Montagem ----------
function build() {
  pageNo = 0;
  const pages = [cover(), levelsPage1(), levelsPage2(), howToPage()];
  for (let d = 1; d <= DIAS; d++) pages.push(markPage(d), dayClosePage(d));
  pages.push(monthClosePage(), finalPage());
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Dominó da Família — Caderno de Placar</title><style>${CSS}</style></head><body>${pages.join('\n')}</body></html>`;
}

(async () => {
  const html = build();
  const htmlPath = path.join(OUT_DIR, 'caderno-domino.html');
  fs.writeFileSync(htmlPath, html);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(OUT_DIR, 'caderno-domino.pdf'), preferCSSPageSize: true, printBackground: true });
  await browser.close();
  console.log(`OK: ${pageNo} páginas`);
})();
