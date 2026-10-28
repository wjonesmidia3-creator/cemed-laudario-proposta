// Gera os PDFs de roteiros (um por cliente) e o ROTEIROS.md a partir de conteudo.mjs.
// Uso: node build.mjs            (gera tudo)
//      node build.mjs EGO Trait  (só os clientes indicados)
import { createRequire } from 'node:module';
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { CALENDARIO, PRAZOS, CHECKLIST, WHATSAPP, CLIENTES } from './conteudo.mjs';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }

const AQUI = dirname(fileURLToPath(import.meta.url));
const SAIDA = join(AQUI, '..');
const HTML_DIR = join(AQUI, 'html');

const esc = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
// Trechos entre colchetes ([Resposta da paciente]) e entre parênteses no início ((equipe)) viram notas de direção.
const fala = (s) => esc(s)
  .replace(/\[([^\]]+)\]/g, '<span class="direcao">[$1]</span>')
  .replace(/^\(([^)]+)\)/gm, '<span class="direcao">($1)</span>')
  .replace(/\n/g, '<br>');
const multilinha = (s) => esc(s).replace(/\n/g, '<br>');
const num = (i) => String(i + 1).padStart(2, '0');

const CSS = `
@page { size: A4; margin: 0; }
:root {
  --black: #0b0c12; --black-2: #151722; --ink: #12141d; --muted: #5d6276; --line: #e4e6ee;
  --soft: #f4f5f9; --orange: #f06a1e; --orange-2: #f7a04b; --cream: #fdf1e8; --navy: #0b2878;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #fff; }
body { font-family: 'Inter', sans-serif; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; background: #fff; }
.page:last-child { page-break-after: auto; }
h1, h2, h3, .poppins { font-family: 'Poppins', sans-serif; }
.brand { font-family: 'Poppins', sans-serif; font-weight: 700; letter-spacing: -0.02em; }
.brand i { font-style: normal; color: var(--orange); }

/* capa */
.capa { background: radial-gradient(120% 70% at 92% 4%, rgba(240,106,30,.30) 0%, rgba(240,106,30,0) 46%),
        radial-gradient(90% 60% at 0% 100%, rgba(11,40,120,.55) 0%, rgba(11,40,120,0) 60%), var(--black); color: #fff; padding: 64px 58px; }
.capa .brand { font-size: 24px; }
.capa .eyebrow { margin-top: 150px; display: flex; align-items: center; gap: 14px; color: var(--orange-2);
  font-size: 11px; font-weight: 700; letter-spacing: .32em; text-transform: uppercase; }
.capa .eyebrow::before { content: ''; width: 34px; height: 3px; background: var(--orange-2); border-radius: 2px; }
.capa h1 { margin-top: 22px; font-size: 44px; line-height: 1.08; font-weight: 800; letter-spacing: -0.025em; max-width: 640px; }
.capa h1 span { color: var(--orange); display: block; }
.capa .sub { margin-top: 22px; font-size: 15px; line-height: 1.6; color: #c9ccd8; max-width: 560px; }
.chips { margin-top: 30px; display: flex; flex-wrap: wrap; gap: 10px; }
.chip { border: 1px solid rgba(255,255,255,.22); border-radius: 999px; padding: 9px 16px; font-size: 11.5px; font-weight: 600; color: #fff; }
.chip b { color: var(--orange-2); font-weight: 700; }
.chip.on { background: var(--orange); border-color: var(--orange); }
.chip.on b { color: #fff; }
.capa .conceito { position: absolute; left: 58px; right: 58px; bottom: 150px; border: 1px solid rgba(255,255,255,.14);
  background: rgba(255,255,255,.04); border-radius: 18px; padding: 26px 30px; }
.capa .conceito .lbl { font-size: 10px; letter-spacing: .3em; font-weight: 700; color: var(--orange-2); text-transform: uppercase; }
.capa .conceito .nome { margin-top: 8px; font-family: 'Poppins', sans-serif; font-size: 22px; font-weight: 700; }
.capa .conceito p { margin-top: 8px; font-size: 12.5px; line-height: 1.6; color: #c9ccd8; }
.capa .faixa { position: absolute; left: 0; right: 0; bottom: 0; height: 112px; display: grid; grid-template-columns: repeat(4, 1fr);
  border-top: 1px solid rgba(255,255,255,.12); }
.capa .faixa div { padding: 24px 26px; border-right: 1px solid rgba(255,255,255,.12); }
.capa .faixa div:last-child { border-right: 0; }
.capa .faixa b { display: block; font-family: 'Poppins', sans-serif; font-size: 25px; font-weight: 800; color: #fff; }
.capa .faixa b em { font-style: normal; color: var(--orange); }
.capa .faixa span { font-size: 11px; color: #aeb2c2; }

/* páginas internas */
.topo { height: 64px; background: var(--black); color: #fff; display: flex; align-items: center; justify-content: space-between; padding: 0 44px; }
.topo .brand { font-size: 17px; }
.topo .cli { font-size: 8.5px; letter-spacing: .3em; color: #9ea3b5; text-transform: uppercase; margin-top: 3px; font-weight: 600; }
.topo .dir { text-align: right; font-size: 11px; color: #aeb2c2; }
.topo .dir b { display: block; color: #fff; font-size: 12px; font-family: 'Poppins', sans-serif; }
.miolo { padding: 30px 44px 0; }
.rodape { position: absolute; left: 44px; right: 44px; bottom: 22px; border-top: 1px solid var(--line); padding-top: 12px;
  display: flex; justify-content: space-between; font-size: 10px; color: var(--muted); }
.rodape .brand { color: var(--ink); font-size: 10.5px; }
.secao { font-size: 10px; letter-spacing: .28em; font-weight: 700; color: var(--orange); text-transform: uppercase; }
.secao em { font-style: normal; color: var(--muted); margin-right: 8px; }
h2 { margin-top: 8px; font-size: 27px; line-height: 1.15; font-weight: 800; letter-spacing: -0.02em; }
h2 span { color: var(--orange); }
.intro { margin-top: 8px; font-size: 12.5px; line-height: 1.55; color: var(--muted); max-width: 640px; }

.stats { margin-top: 20px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.stat { border: 1px solid var(--line); border-radius: 14px; padding: 16px 16px 14px; position: relative; }
.stat::before { content: ''; position: absolute; top: -1px; left: 16px; width: 26px; height: 4px; background: var(--orange); border-radius: 0 0 3px 3px; }
.stat b { display: block; font-family: 'Poppins', sans-serif; font-size: 25px; font-weight: 800; letter-spacing: -0.02em; }
.stat span { display: block; margin-top: 4px; font-size: 11.5px; line-height: 1.4; }
.stat small { display: block; margin-top: 8px; font-size: 10px; line-height: 1.4; color: var(--muted); }
.leitura { margin-top: 14px; background: var(--cream); border-left: 4px solid var(--orange); border-radius: 0 12px 12px 0; padding: 14px 18px; font-size: 11.5px; line-height: 1.55; }
.leitura .lbl { font-size: 9.5px; letter-spacing: .26em; font-weight: 700; color: var(--orange); margin-bottom: 4px; }

.duas { margin-top: 18px; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.card { border: 1px solid var(--line); border-radius: 14px; padding: 16px 18px; }
.card h3 { font-size: 14px; font-weight: 700; }
.card p { margin-top: 6px; font-size: 11px; line-height: 1.55; color: #3a3e4f; }
.passos { margin-top: 10px; display: grid; gap: 8px; }
.passo { display: grid; grid-template-columns: 24px 1fr; gap: 10px; align-items: start; font-size: 11px; line-height: 1.45; }
.passo i { font-style: normal; width: 24px; height: 24px; border-radius: 50%; background: var(--black); color: #fff; font-weight: 700; font-size: 11px; display: grid; place-items: center; }
.passo b { display: block; font-size: 11.5px; }
.cal { margin-top: 10px; display: grid; gap: 7px; }
.cal .fase { display: grid; grid-template-columns: 98px 1fr; gap: 10px; padding: 9px 11px; border-radius: 10px; background: var(--soft); font-size: 10.5px; line-height: 1.4; }
.cal .fase.on { background: var(--black); color: #fff; }
.cal .fase b { display: block; font-size: 11px; }
.cal .fase small { color: var(--muted); font-size: 10px; }
.cal .fase.on small { color: #c9ccd8; }
.cal .fase .rots { font-weight: 700; color: var(--orange); }
.alerta { margin-top: 16px; display: grid; grid-template-columns: 1.1fr 1fr; gap: 16px; background: var(--black); color: #fff; border-radius: 14px; padding: 18px 20px; }
.alerta h3 { font-size: 14px; }
.alerta h3 span { color: var(--orange); }
.alerta p { margin-top: 6px; font-size: 10.8px; line-height: 1.55; color: #c9ccd8; }
.alerta .prazos { border-left: 1px solid rgba(255,255,255,.15); padding-left: 16px; display: grid; gap: 10px; align-content: center; }
.alerta .prazos div { font-size: 10.5px; color: #c9ccd8; line-height: 1.4; }
.alerta .prazos b { display: block; font-family: 'Poppins', sans-serif; font-size: 18px; color: var(--orange-2); }

/* roteiro */
.rot-cab { display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; }
.rot-num { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 54px; line-height: .9; color: var(--orange); letter-spacing: -0.04em; }
.meta { margin-top: 14px; display: grid; grid-template-columns: 1.05fr 1fr 1.25fr .7fr; border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
.meta div { padding: 9px 12px; border-right: 1px solid var(--line); font-size: 10.5px; line-height: 1.4; }
.meta div:last-child { border-right: 0; background: var(--cream); }
.meta small { display: block; font-size: 8.5px; letter-spacing: .2em; font-weight: 700; color: var(--muted); text-transform: uppercase; margin-bottom: 3px; }
.obj { margin-top: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.obj div { background: var(--soft); border-radius: 10px; padding: 10px 12px; font-size: 10.5px; line-height: 1.5; }
.obj small { display: block; font-size: 8.5px; letter-spacing: .2em; font-weight: 700; color: var(--orange); text-transform: uppercase; margin-bottom: 3px; }
.aviso { margin-top: 10px; border: 1px dashed var(--orange); border-radius: 10px; padding: 9px 12px; font-size: 10.3px; line-height: 1.5; background: #fffaf6; }
.aviso b { color: var(--orange); }
table { margin-top: 12px; width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
th { background: var(--black); color: #fff; font-size: 8.5px; letter-spacing: .2em; text-transform: uppercase; text-align: left; padding: 8px 10px; font-weight: 700; }
td { padding: 9px 10px; vertical-align: top; font-size: 10.4px; line-height: 1.45; border-top: 1px solid var(--line); }
tr:nth-child(even) td { background: #fafbfd; }
td.t { width: 58px; font-weight: 700; color: var(--orange); white-space: nowrap; font-size: 10px; }
td.img { width: 26%; color: #4a4f62; }
td.fala { font-weight: 500; color: var(--ink); }
td.tela { width: 21%; font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 9.5px; letter-spacing: .02em; color: var(--ink); }
.direcao { color: var(--muted); font-style: italic; font-weight: 400; }
.fim { margin-top: 12px; display: grid; grid-template-columns: 1.35fr 1fr; gap: 10px; }
.fim > div { border: 1px solid var(--line); border-radius: 12px; padding: 11px 13px; font-size: 10.2px; line-height: 1.5; }
.fim small { display: block; font-size: 8.5px; letter-spacing: .2em; font-weight: 700; color: var(--orange); text-transform: uppercase; margin-bottom: 4px; }
.fim .leg { white-space: normal; color: #2d3142; }
.fim .rt { margin-top: 6px; color: var(--muted); font-size: 9.5px; }

/* whatsapp e regras */
.wpp { margin-top: 18px; display: grid; gap: 10px; }
.msg { display: grid; grid-template-columns: 150px 1fr; gap: 14px; align-items: start; }
.msg .q b { display: block; font-size: 11.5px; font-family: 'Poppins', sans-serif; }
.msg .q small { font-size: 10px; color: var(--muted); }
.balao { background: #e7f8ee; border-radius: 4px 14px 14px 14px; padding: 11px 14px; font-size: 11px; line-height: 1.55; color: #12301e; border: 1px solid #cdeedb; }
.regras { margin-top: 18px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.regras .card ul { margin-top: 8px; padding-left: 16px; display: grid; gap: 6px; font-size: 10.8px; line-height: 1.45; }
.regras .pode h3 { color: #138a4a; }
.regras .nao h3 { color: #c2410c; }
.check { margin-top: 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px 16px; }
.check div { display: grid; grid-template-columns: 18px 1fr; gap: 8px; font-size: 10.8px; line-height: 1.45; }
.check div::before { content: ''; width: 14px; height: 14px; border: 1.6px solid var(--ink); border-radius: 4px; margin-top: 1px; }
.fonte { margin-top: 16px; font-size: 9.5px; line-height: 1.5; color: var(--muted); }
`;

function topo(c, direita) {
  return `<div class="topo"><div><div class="brand">Grupo Opera<i>.</i></div><div class="cli">${esc(c.nome)}</div></div>
    <div class="dir"><b>Roteiros Black Friday</b>${esc(direita)}</div></div>`;
}
function rodape(c, n) {
  return `<div class="rodape"><div><span class="brand">Grupo Opera<i>.</i></span> · Roteiros Black Friday ${esc(c.curto)}</div><div>${String(n).padStart(2, '0')}</div></div>`;
}

function capa(c) {
  const chips = CALENDARIO.map((f) =>
    `<div class="chip${f.fase === 'Black Friday' ? ' on' : ''}">${esc(f.fase)} · <b>${esc(f.janela)}</b></div>`).join('');
  return `<section class="page capa">
    <div class="brand">Grupo Opera<i>.</i></div>
    <div class="eyebrow">Roteiros Black Friday 2026 · ${esc(c.nome)}</div>
    <h1>${esc(c.capa.titulo)} <span>${esc(c.capa.destaque)}</span></h1>
    <p class="sub">${esc(c.capa.sub)}</p>
    <div class="chips">${chips}</div>
    <div class="conceito"><div class="lbl">Conceito da campanha</div><div class="nome">${esc(c.conceito)}</div>
      <p>Vídeos sem preço, sem "grátis" e sem forma de pagamento. A condição especial é apresentada no atendimento individual, e cada vídeo leva para a Lista VIP ou para o WhatsApp.</p></div>
    <div class="faixa">
      <div><b>${c.roteiros.length} <em>roteiros</em></b><span>prontos para gravar</span></div>
      <div><b>até ${PRAZOS.gravacao}</b><span>prazo para gravação</span></div>
      <div><b>27<em>/11</em></b><span>abertura da Black Friday</span></div>
      <div><b>30<em>/11</em></b><span>último dia da condição</span></div>
    </div>
  </section>`;
}

function estrategia(c, pg) {
  const stats = c.dados.map((d) => `<div class="stat"><b>${esc(d.valor)}</b><span>${esc(d.rotulo)}</span><small>${esc(d.nota)}</small></div>`).join('');
  const rotsPorFase = (fase) => c.roteiros.map((r, i) => (r.fase === fase ? num(i) : null)).filter(Boolean);
  const cal = CALENDARIO.map((f) => {
    const rs = rotsPorFase(f.fase);
    return `<div class="fase${f.fase === 'Black Friday' ? ' on' : ''}"><div><b>${esc(f.fase)}</b><small>${esc(f.janela)}</small></div>
      <div>${esc(f.texto)}${rs.length ? ` <span class="rots">Roteiro ${rs.join(' e ')}</span>` : ''}</div></div>`;
  }).join('');
  return `<section class="page">${topo(c, 'Estratégia')}
  <div class="miolo">
    <div class="secao"><em>01</em>Estratégia</div>
    <h2>O que os dados da ${esc(c.curto)} <span>mostram</span></h2>
    <p class="intro">Antes de escrever, olhamos as campanhas e os conteúdos de 2026. Os roteiros partem do que já trouxe conversa e engajamento para a clínica.</p>
    <div class="stats">${stats}</div>
    <div class="leitura"><div class="lbl">LEITURA</div>${esc(c.leitura)}${c.notaCanal ? `<br><b>Nota:</b> ${esc(c.notaCanal)}` : ''}</div>
    <div class="duas">
      <div class="card"><h3>Conceito: ${esc(c.conceito)}</h3><p>${esc(c.conceitoTexto)}</p>
        <div class="passos">
          <div class="passo"><i>1</i><div><b>Lista VIP</b>O vídeo pede para mandar BLACK no WhatsApp. Quem manda entra na lista e recebe a novidade primeiro.</div></div>
          <div class="passo"><i>2</i><div><b>Conversa individual</b>A recepção entende o caso e convida para a avaliação (roteiro de atendimento na pág. 08).</div></div>
          <div class="passo"><i>3</i><div><b>Avaliação até 30/11</b>A condição especial é apresentada na avaliação, para quem iniciar o tratamento até 30/11.</div></div>
        </div></div>
      <div class="card"><h3>Calendário de publicação</h3><div class="cal">${cal}</div></div>
    </div>
    <div class="alerta">
      <div><h3>Por que os vídeos <span>não falam de preço</span></h3>
        <p>O Código de Ética Odontológica proíbe anunciar preço, serviço gratuito e forma de pagamento. Desde 2025 (Res. CFO 271) o desconto em si deixou de ser infração, mas campanhas de Black Friday em massa ainda são discutidas na Justiça. Por isso, todos os roteiros falam em "condição especial" e deixam valores para a conversa individual. Regras completas na pág. 09.</p></div>
      <div class="prazos">
        <div><b>até ${PRAZOS.condicao}</b>A clínica define a condição (tratamentos, regra e prazo) para a recepção falar a mesma coisa.</div>
        <div><b>até ${PRAZOS.gravacao}</b>Gravação dos 5 vídeos, para editar e publicar a partir de 09/11.</div>
      </div>
    </div>
  </div>${rodape(c, pg)}</section>`;
}

function roteiro(c, r, i, pg) {
  const linhas = r.cenas.map((s) => `<tr><td class="t">${esc(s.t)}</td><td class="img">${multilinha(s.imagem)}</td><td class="fala">${fala(s.fala)}</td><td class="tela">${esc(s.tela)}</td></tr>`).join('');
  return `<section class="page">${topo(c, `Roteiro ${num(i)} de ${num(c.roteiros.length - 1)}`)}
  <div class="miolo">
    <div class="rot-cab"><div><div class="secao"><em>Roteiro ${num(i)}</em>${esc(r.fase)} · ${esc(r.janela)}</div><h2>${esc(r.titulo)}</h2></div><div class="rot-num">${num(i)}</div></div>
    <div class="meta">
      <div><small>Formato</small>${esc(r.formato)}</div>
      <div><small>Quem grava</small>${esc(r.quem)}</div>
      <div><small>Onde usar</small>${esc(r.onde)}</div>
      <div><small>Publicar</small><b>${esc(r.janela)}</b></div>
    </div>
    <div class="obj"><div><small>Objetivo</small>${esc(r.objetivo)}</div><div><small>Por que este roteiro</small>${esc(r.porque)}</div></div>
    ${r.aviso ? `<div class="aviso"><b>Atenção:</b> ${esc(r.aviso)}</div>` : ''}
    <table><thead><tr><th>Tempo</th><th>Cena</th><th>Fala</th><th>Texto na tela</th></tr></thead><tbody>${linhas}</tbody></table>
    <div class="fim">
      <div><small>Legenda sugerida</small><div class="leg">${multilinha(r.legenda)}</div><div class="rt">+ Responsável técnico: [nome] · CRO-[UF] [nº]</div></div>
      <div><small>Dica de gravação</small>${esc(r.dica)}</div>
    </div>
  </div>${rodape(c, pg)}</section>`;
}

function atendimento(c, pg) {
  const msgs = WHATSAPP.map((m) => `<div class="msg"><div class="q"><b>${esc(m.etapa)}</b><small>${esc(m.quando)}</small></div>
    <div class="balao">${esc(m.texto.replaceAll('{clinica}', c.curto))}</div></div>`).join('');
  return `<section class="page">${topo(c, 'Atendimento')}
  <div class="miolo">
    <div class="secao"><em>02</em>Atendimento</div>
    <h2>Quando a pessoa mandar <span>BLACK</span></h2>
    <p class="intro">Todos os vídeos levam para o WhatsApp. É aqui que a campanha vira avaliação agendada, então a recepção precisa falar a mesma língua dos vídeos. Mensagens-modelo para adaptar ao jeito da clínica:</p>
    <div class="wpp">${msgs}</div>
    <div class="leitura" style="margin-top:18px"><div class="lbl">REGRA DE OURO</div>Valores, percentuais e formas de pagamento só aparecem na conversa individual ou na consulta. Nunca em post, stories, anúncio, status do WhatsApp ou lista de transmissão.</div>
    <div class="duas">
      <div class="card"><h3>Mensagem automática das campanhas</h3><p>Nas campanhas de mensagem da Meta, troque a mensagem pré-preenchida por: <b>"Oi! Quero entrar na Lista VIP Black 🖤"</b>. Assim a recepção sabe de onde veio o contato.</p></div>
      <div class="card"><h3>Marcar quem chegou pela Black</h3><p>Use uma etiqueta "Black 2026" no WhatsApp Business. Em dezembro, ela mostra quantas conversas viraram avaliação e tratamento iniciado.</p></div>
    </div>
  </div>${rodape(c, pg)}</section>`;
}

function regras(c, pg) {
  const chk = CHECKLIST.map((t) => `<div>${esc(t)}</div>`).join('');
  return `<section class="page">${topo(c, 'Antes de publicar')}
  <div class="miolo">
    <div class="secao"><em>03</em>Regras</div>
    <h2>Black Friday <span>dentro do Código de Ética</span></h2>
    <p class="intro">Resumo prático para a clínica e para quem edita os vídeos. Na dúvida, o responsável técnico da clínica valida antes de publicar.</p>
    <div class="regras">
      <div class="card pode"><h3>Pode</h3><ul>
        <li>Falar em Black Friday, "condição especial" e prazo (até 30/11).</li>
        <li>Lista VIP e convite para a avaliação.</li>
        <li>Conteúdo educativo sobre tratamentos, sem promessa de resultado.</li>
        <li>Depoimento de paciente com autorização de imagem assinada.</li>
        <li>Desconto apresentado de forma individual, na conversa ou na consulta.</li>
      </ul></div>
      <div class="card nao"><h3>Não pode</h3><ul>
        <li>Preço, valor ou "a partir de R$" em qualquer conteúdo público.</li>
        <li>"Grátis", "gratuito" ou "cortesia", inclusive para a avaliação.</li>
        <li>Forma de pagamento (parcelas, Pix, cartão) em anúncio ou post.</li>
        <li>Percentual de desconto em conteúdo público (zona de risco: campanhas em massa ainda são discutidas na Justiça).</li>
        <li>Promessa de resultado: "sem dor", "garantido", "sorriso perfeito".</li>
      </ul></div>
    </div>
    <div class="leitura" style="margin-top:18px"><div class="lbl">CHECKLIST ANTES DE PUBLICAR</div>Passe por esta lista em cada vídeo, legenda e anúncio.</div>
    <div class="check">${chk}</div>
    <p class="fonte">Base: Código de Ética Odontológica (Res. CFO 118/2012), com as alterações das Res. CFO 196/2019 (imagens e selfies) e 271/2025 (descontos), e a discussão judicial sobre campanhas de Black Friday na odontologia (TRF5, MS 0805602-15.2025.4.05.8300). Este material não substitui orientação jurídica nem a consulta ao CRO do estado.<br>
    Dados de desempenho: Reportei (Meta Ads, Google Ads, Instagram e YouTube), agosto a outubro de 2026.</p>
  </div>${rodape(c, pg)}</section>`;
}

function documento(c) {
  let pg = 1;
  const paginas = [capa(c)];
  paginas.push(estrategia(c, ++pg));
  c.roteiros.forEach((r, i) => paginas.push(roteiro(c, r, i, ++pg)));
  paginas.push(atendimento(c, ++pg));
  paginas.push(regras(c, ++pg));
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Roteiros Black Friday ${esc(c.curto)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=block" rel="stylesheet">
<style>${CSS}</style></head><body>${paginas.join('\n')}</body></html>`;
}

function markdown() {
  const md = [`# Roteiros Black Friday 2026 · Clientes de odontologia`, ``,
    `> Gerado a partir de \`_fonte/conteudo.mjs\`. Os PDFs desta pasta têm o mesmo conteúdo, com layout para enviar ao cliente.`, ``,
    `**Calendário:** ${CALENDARIO.map((f) => `${f.fase} (${f.janela})`).join(' → ')}. Condição definida pela clínica até ${PRAZOS.condicao}; gravação até ${PRAZOS.gravacao}.`, ``];
  for (const c of CLIENTES) {
    md.push(`---`, ``, `## ${c.nome}`, ``, `**Conceito:** ${c.conceito}. ${c.conceitoTexto}`, ``);
    md.push(...c.dados.map((d) => `- **${d.valor}** ${d.rotulo}. ${d.nota}`), ``);
    c.roteiros.forEach((r, i) => {
      md.push(`### Roteiro ${num(i)} · ${r.titulo}`, ``,
        `**${r.fase} · ${r.janela}** · ${r.formato} · Quem grava: ${r.quem} · Onde usar: ${r.onde}`, ``,
        `**Objetivo:** ${r.objetivo}  `, `**Por quê:** ${r.porque}`, ``);
      if (r.aviso) md.push(`> **Atenção:** ${r.aviso}`, ``);
      md.push(`| Tempo | Cena | Fala | Texto na tela |`, `|---|---|---|---|`);
      md.push(...r.cenas.map((s) => `| ${s.t} | ${s.imagem} | ${s.fala.replace(/\n/g, '<br>')} | ${s.tela} |`), ``);
      md.push(`**Legenda sugerida:**`, ``, ...r.legenda.split('\n').map((l) => `> ${l}`), `> `, `> Responsável técnico: [nome] · CRO-[UF] [nº]`, ``, `**Dica de gravação:** ${r.dica}`, ``);
    });
  }
  return md.join('\n');
}

const filtro = process.argv.slice(2);
const alvos = filtro.length ? CLIENTES.filter((c) => filtro.includes(c.slug)) : CLIENTES;
mkdirSync(HTML_DIR, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage();
for (const c of alvos) {
  const htmlPath = join(HTML_DIR, `${c.slug}.html`);
  writeFileSync(htmlPath, documento(c));
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  // Falha se algum conteúdo passar da altura da página (texto cortado no PDF).
  const estouros = await page.$$eval('.page', (ps) => ps.map((p, i) => {
    const limite = p.getBoundingClientRect().bottom - 52;
    const fundo = Math.max(...[...p.querySelectorAll('.miolo > *')].map((e) => e.getBoundingClientRect().bottom), 0);
    return fundo > limite ? `pág. ${i + 1}: ${Math.round(fundo - limite)}px além do limite` : null;
  }).filter(Boolean));
  if (estouros.length) console.warn(`⚠ ${c.slug}: ${estouros.join('; ')}`);
  const fontes = await page.evaluate(() => [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family));
  if (!fontes.some((f) => f.includes('Poppins'))) console.warn(`⚠ ${c.slug}: Poppins não carregou`);
  const pdf = join(SAIDA, `Roteiros_BlackFriday_2026_${c.slug}.pdf`);
  await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
  console.log(`✓ ${pdf}`);
}
await browser.close();
if (!filtro.length) {
  writeFileSync(join(SAIDA, 'ROTEIROS.md'), markdown());
  console.log(`✓ ${join(SAIDA, 'ROTEIROS.md')}`);
}
