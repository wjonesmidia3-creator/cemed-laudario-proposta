"""Gera os relatórios semanais (padrão Grupo Opera) em PDF, um por cliente.

Uso:
    python3 gerar.py semana_2026_11_02 [arquivo ...]

O argumento é o nome de um módulo nesta pasta que define:
    SEMANA  -> dict com rótulos dos períodos e pasta de saída
    CLIENTES -> lista de dicts com os dados e textos de cada cliente
"""
import html
import importlib
import json
import math
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LIMITE_TABELA_COM_GRAFICO = 14


# ---------------------------------------------------------------- formatação
def _milhar(s):
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def f_int(v):
    return "—" if v is None else _milhar(f"{round(v):,.0f}")


def f_brl(v, dec=2):
    return "—" if v is None else "R$ " + _milhar(f"{v:,.{dec}f}")


def f_num(v, dec=1):
    return "—" if v is None else _milhar(f"{v:,.{dec}f}")


def f_mil(v):
    """12345 -> '12,3 mil'"""
    if v >= 1000:
        return f_num(v / 1000, 1) + " mil"
    return f_int(v)


FMT = {"int": f_int, "brl": f_brl, "brl0": lambda v: f_brl(v, 0)}


def variacao(cur, prev):
    if cur is None or prev in (None, 0):
        return None
    return (cur - prev) / prev * 100


def txt_pct(p):
    a = abs(p)
    s = f_num(a, 1) if a < 10 else f_int(a)
    return s + "%"


def estado(p, melhor):
    if p is None or melhor is None or abs(p) < 0.05:
        return "neu"
    bom = (p > 0) == (melhor == "up")
    return "bom" if bom else "ruim"


def badge(cur, prev, melhor):
    p = variacao(cur, prev)
    if p is None:
        return ""
    seta = "▲" if p > 0 else "▼"
    if abs(p) < 0.05:
        seta, p = "=", 0.0
    return f'<span class="badge {estado(p, melhor)}">{seta} {txt_pct(p)}</span>'


def delta_linha(cur, prev, melhor, sufixo="vs. sem. anterior"):
    p = variacao(cur, prev)
    if p is None:
        return '<div class="kdelta neu">sem base de comparação</div>'
    seta = "▲" if p > 0 else "▼"
    return f'<div class="kdelta {estado(p, melhor)}">{seta} {txt_pct(p)} {sufixo}</div>'


# ---------------------------------------------------------------- gráfico
def grafico(ch, sem):
    prev, cur = ch["prev"], ch["cur"]
    serie = prev + cur
    labels = sem["dias"]
    W, H = 700, 170
    L, R, T, B = 38, 8, 26, 24
    pw, ph = W - L - R, H - T - B
    vmax = max(serie) or 1
    # escala com passos "redondos" (1, 2, 2,5, 5 x 10^k), 3 a 4 divisões
    bruto = vmax / 3.5
    mag = 10 ** math.floor(math.log10(bruto))
    passo = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= bruto)
    ndiv = math.ceil(vmax / passo)
    teto = passo * ndiv
    n = len(serie)
    slot = pw / n
    bw = slot * 0.62

    def fmtv(v):
        if ch.get("unidade") == "brl":
            return f_brl(v, 0)
        if v >= 1000:
            return f_num(v / 1000, 0 if v % 1000 == 0 else 1) + "k"
        return f_int(v)

    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for i in range(ndiv + 1):
        v = passo * i
        y = T + ph - ph * i / ndiv
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#E6EAF2" stroke-width="1"/>')
        out.append(f'<text x="{L-6}" y="{y+3:.1f}" text-anchor="end" class="ax">{fmtv(v)}</text>')
    ipk = serie.index(max(serie))
    for i, v in enumerate(serie):
        x = L + slot * i + (slot - bw) / 2
        h = ph * v / teto
        cor = "#0B2C7A" if i < len(prev) else "#E8601C"
        out.append(f'<rect x="{x:.1f}" y="{T+ph-h:.1f}" width="{bw:.1f}" height="{max(h,0.8):.1f}" rx="2" fill="{cor}"/>')
        out.append(f'<text x="{x+bw/2:.1f}" y="{H-8}" text-anchor="middle" class="ax">{labels[i]}</text>')
    # pico
    xp = L + slot * ipk + slot / 2
    pv = serie[ipk]
    yp = T + ph - ph * pv / teto
    out.append(f'<line x1="{xp:.1f}" x2="{xp:.1f}" y1="{T-12}" y2="{yp-3:.1f}" stroke="#E8601C" stroke-dasharray="3 3" stroke-width="1.2"/>')
    anc = "end" if ipk > n * 0.7 else ("start" if ipk < n * 0.3 else "middle")
    dx = -4 if anc == "end" else (4 if anc == "start" else 0)
    pico_txt = f_brl(pv) if ch.get("unidade") == "brl" else f_int(pv)
    out.append(f'<text x="{xp+dx:.1f}" y="{T-15}" text-anchor="{anc}" class="pk">pico {pico_txt} em {labels[ipk]}</text>')
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------- blocos
def cabecalho(c, titulo, sub):
    return f"""
    <div class="hdr">
      <div><div class="logo">Grupo Opera<span>.</span></div><div class="hdr-cli">{html.escape(c['nome'].upper())}</div></div>
      <div class="hdr-r"><b>{titulo}</b><span>{sub}</span></div>
    </div>"""


def rodape(c, n):
    return f"""<div class="ftr"><div><b>Grupo Opera<span>.</span></b> · Relatório semanal {html.escape(c['nome'])}</div><div>{n:02d}</div></div>"""


def tabela(c, sem, lado):
    atual = lado == "cur"
    head = (f'<div class="th cur"><b>Esta semana</b><span>{sem["cur_curto"].upper()} · 7 DIAS</span></div>' if atual
            else f'<div class="th prev"><b>Semana anterior</b><span>{sem["prev_curto"].upper()} · 7 DIAS</span></div>')
    linhas = []
    for g in c["grupos"]:
        linhas.append(f'<div class="gt">{g["titulo"]}</div>')
        for r in g["linhas"]:
            rot, prev, cur, fmt, melhor = r[:5]
            hl = len(r) > 5 and r[5]
            v = cur if atual else prev
            val = FMT[fmt](v)
            if atual:
                b = badge(cur, prev, melhor) if hl else ""
                cls = "v hl" if hl else "v"
                linhas.append(f'<div class="tr"><span>{rot}</span><span class="{cls}">{val}{b}</span></div>')
            else:
                linhas.append(f'<div class="tr"><span>{rot}</span><span class="v">{val}</span></div>')
    return f'<div class="tbl {"tcur" if atual else "tprev"}">{head}<div class="tb">{"".join(linhas)}</div></div>'


def bloco_grafico(c, sem):
    ch = c["grafico"]
    return f"""
    <div class="card chart">
      <div class="ct">{ch['titulo']}</div>
      <div class="cs">{ch['sub']}</div>
      {grafico(ch, sem)}
      <div class="lg"><span><i style="background:#0B2C7A"></i>Semana anterior</span><span><i style="background:#E8601C"></i>Esta semana</span></div>
    </div>"""


def pagina_capa(c, sem):
    strip = "".join(f'<div class="st"><div class="sv">{v}</div><div class="sl">{l}</div></div>' for v, l in c["faixa"])
    d = c["destaque"]
    return f"""
<section class="page capa">
  <div class="glow"></div>
  <div class="logo big">Grupo Opera<span>.</span></div>
  <div class="eyebrow"><i></i>RELATÓRIO SEMANAL · {html.escape(c['nome'].upper())}</div>
  <h1><span class="l1">{c['titulo'][0]}</span><span class="l2">{c['titulo'][1]}</span></h1>
  <p class="lead">{c['lead']}</p>
  <div class="pills"><span class="pill o">Semana anterior · {sem['prev_curto']}</span><span class="pill f">Esta semana · {sem['cur_curto']}</span></div>
  <div class="dest">
    <div class="dn"><div class="dnum">{d['num']}</div><div class="dlab">{d['rotulo']}</div></div>
    <div class="dt"><div class="dey">DESTAQUE DA SEMANA</div><div class="dh">{d['titulo']}</div><div class="dd">{d['texto']}</div></div>
  </div>
  <div class="strip">{strip}</div>
</section>"""


def pagina_numeros(c, sem, n):
    kp = "".join(f"""<div class="kpi"><i></i><div class="kv">{k['valor']}</div><div class="kl">{k['rotulo']}</div>{k['delta']}</div>"""
                 for k in c["kpis"])
    graf = bloco_grafico(c, sem) if not c.get("grafico_p3") else ""
    return f"""
<section class="page">
  {cabecalho(c, 'Relatório semanal', sem['cur_longo'])}
  <div class="body">
    <div class="sec"><b>01</b> SEMANA × SEMANA</div>
    <h2>Os números, <em>semana a semana</em></h2>
    <p class="intro">{c['intro_p2']}</p>
    <div class="kpis">{kp}</div>
    <div class="cols {'dense' if c.get('denso') else ''}">{tabela(c, sem, 'prev')}{tabela(c, sem, 'cur')}</div>
    {graf}
    <p class="src">{c['fonte']}</p>
  </div>
  {rodape(c, n)}
</section>"""


def pagina_leitura(c, sem, n):
    partes = []
    if c.get("posts"):
        cards = []
        for p in c["posts"]:
            dia, mes = p["data"].split("/")
            mets = " ".join(f'<b>{v}</b> {l}' for v, l in p["metricas"])
            cards.append(f"""<div class="post"><div class="pd"><div class="pl">▶</div><div class="pdd">{dia}</div><div class="pm">{mes}</div></div>
              <div class="pc"><span class="tag">{p['tag']}</span><div class="ptit">{p['titulo']}</div><div class="pmet">{mets}</div></div></div>""")
        partes.append(f'<div class="sub">Publicações da semana</div><div class="posts">{"".join(cards)}</div>')
    if c.get("grafico_p3"):
        partes.append(bloco_grafico(c, sem))
    ins = "".join(f'<div class="ins {i[0]}"><div class="it">{i[1]}</div><div class="ix">{i[2]}</div></div>' for i in c["insights"])
    partes.append(f'<div class="sub">O que a semana mostrou</div><div class="insights n{len(c["insights"])}">{ins}</div>')
    partes.append(f'<div class="leitura"><div class="ley">LEITURA</div><p>{c["leitura"]}</p></div>')
    nx = "".join(f'<div class="nx"><div class="nxe">PRÓXIMO {i+1:02d}</div><div class="nxt">{t}</div><div class="nxx">{x}</div></div>'
                 for i, (t, x) in enumerate(c["proximos"]))
    partes.append(f'<div class="next">{nx}</div>')
    nota = f'<p class="src">{c["nota_p3"]}</p>' if c.get("nota_p3") else ""
    return f"""
<section class="page">
  {cabecalho(c, 'Leitura da semana', 'Destaques e próximos passos')}
  <div class="body">
    <div class="sec"><b>02</b> LEITURA DA SEMANA</div>
    <h2>{c['titulo_p3']}</h2>
    <p class="intro">{c['intro_p3']}</p>
    {''.join(partes)}
    {nota}
  </div>
  {rodape(c, n)}
</section>"""


def documento(c, sem):
    css = open(os.path.join(AQUI, "estilo.css"), encoding="utf-8").read()
    fontes = open(os.path.join(AQUI, "fonts", "local.css"), encoding="utf-8").read()
    # tabela longa (linhas + títulos de grupo > LIMITE) -> gráfico vai para a página 3
    if "grafico_p3" not in c:
        unidades = sum(len(g["linhas"]) + 1 for g in c["grupos"])
        # sem posts, a página 3 tem espaço: o gráfico vai para lá (exceto tabelas curtas)
        c["grafico_p3"] = unidades > LIMITE_TABELA_COM_GRAFICO or (not c.get("posts") and unidades > 9)
    corpo =pagina_capa(c, sem) + pagina_numeros(c, sem, 2) + pagina_leitura(c, sem, 3)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Relatório semanal · {html.escape(c['nome'])}</title>
<style>{fontes}</style><style>{css}</style></head><body>{corpo}</body></html>"""


def main():
    mod = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "semana_2026_11_02")
    sem, clientes = mod.SEMANA, mod.CLIENTES
    saida = os.path.join(AQUI, "..", sem["pasta"])
    os.makedirs(saida, exist_ok=True)
    so = set(sys.argv[2:])
    previa = os.environ.get("PREVIA")  # pasta para salvar PNGs de conferência
    pares, temporarios = [], []
    for c in clientes:
        if so and c["arquivo"] not in so:
            continue
        # o HTML fica na pasta fonts/ para resolver os arquivos de fonte por caminho relativo
        html_path = os.path.join(AQUI, "fonts", f"_tmp_{c['arquivo']}.html")
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(documento(c, sem))
        destino = os.path.abspath(os.path.join(saida, f"{c['arquivo']}_Semanal_{sem['sufixo']}.pdf"))
        par = [html_path, destino]
        if previa:
            par.append(os.path.join(previa, f"{c['arquivo']}.png"))
        pares.append(par)
        temporarios.append(html_path)
    lista = os.path.join(AQUI, "fonts", "_tmp_lista.json")
    with open(lista, "w", encoding="utf-8") as fh:
        json.dump(pares, fh)
    temporarios.append(lista)
    subprocess.run(["node", os.path.join(AQUI, "pdf.js"), lista], check=True)
    if os.environ.get("MANTER_HTML") != "1":
        for t in temporarios:
            os.remove(t)


if __name__ == "__main__":
    main()
