"""Gera os relatórios semanais (padrão Grupo Opera) em PDF, um por cliente.

Uso (na pasta _gerador):
    python3 gerar.py <pasta>                 # todos os clientes da semana
    python3 gerar.py <pasta> CEMED Fiorini   # só alguns (nome do arquivo JSON, sem .json)
    python3 gerar.py <pasta> --validar       # só confere os JSON, sem gerar PDF
    python3 gerar.py <pasta> --mensagens     # só exporta as mensagens de WhatsApp para downloads/

Entrada: dados/<pasta>/semana.json e dados/<pasta>/clientes/<arquivo>.json
Saída:   ../<pasta>/<arquivo>_Semanal_<sufixo>.pdf

Marcação aceita nos textos dos JSON:
    {{texto}}  -> destaque laranja (no titulo_p3 vira o trecho laranja do título)
    **texto**  -> negrito
    quebra de linha (\n) nos rótulos dos KPIs -> <br>

Código de saída: 0 ok · 2 JSON inválido · 3 conteúdo encostando no rodapé (encurtar textos/linhas)
"""
import glob
import html
import json
import math
import os
import re
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


# ---------------------------------------------------------------- JSON -> estrutura de render
def md(s, em=False):
    """Escapa HTML e converte {{destaque}} e **negrito**."""
    s = html.escape(str(s), quote=False)
    s = re.sub(r"\{\{(.+?)\}\}", (r"<em>\1</em>" if em else r'<span class="hl">\1</span>'), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s.replace("\n", "<br>")


def validar(c, sem):
    erros = []

    def exige(cond, msg):
        if not cond:
            erros.append(msg)

    for k in ("arquivo", "nome", "titulo", "lead", "destaque", "faixa", "intro_p2", "kpis", "grupos",
              "grafico", "fonte", "titulo_p3", "intro_p3", "insights", "leitura", "proximos"):
        exige(k in c, f"falta o campo '{k}'")
    if erros:
        return erros
    exige(isinstance(c["titulo"], list) and len(c["titulo"]) == 2, "titulo deve ter 2 linhas")
    for k in ("num", "rotulo", "titulo", "texto"):
        exige(k in c["destaque"], f"destaque sem '{k}'")
    exige(len(c["faixa"]) == 4, "faixa deve ter 4 itens")
    exige(len(c["kpis"]) == 4, "kpis deve ter 4 itens")
    for i, k in enumerate(c["kpis"]):
        for campo in ("valor", "rotulo", "cur", "prev", "melhor"):
            exige(campo in k, f"kpis[{i}] sem '{campo}'")
        exige(k.get("melhor") in ("up", "down", None), f"kpis[{i}].melhor deve ser 'up', 'down' ou null")
    for g in c["grupos"]:
        exige(g.get("linhas"), f"grupo '{g.get('titulo')}' sem linhas")
        for l in g.get("linhas", []):
            exige(l.get("fmt") in FMT, f"linha '{l.get('rotulo')}': fmt deve ser um de {sorted(FMT)}")
            exige(l.get("melhor") in ("up", "down", None), f"linha '{l.get('rotulo')}': melhor inválido")
            for campo in ("prev", "cur"):
                v = l.get(campo)
                exige(v is None or isinstance(v, (int, float)), f"linha '{l.get('rotulo')}': {campo} deve ser número ou null")
    ch = c["grafico"]
    exige(len(ch.get("prev", [])) == 7 and len(ch.get("cur", [])) == 7, "grafico.prev e grafico.cur devem ter 7 valores cada")
    exige(all(isinstance(v, (int, float)) for v in ch.get("prev", []) + ch.get("cur", [])), "grafico: valores devem ser números")
    exige(any(v > 0 for v in ch.get("prev", []) + ch.get("cur", [])), "grafico: todos os valores são zero")
    exige(2 <= len(c["insights"]) <= 4, "insights deve ter de 2 a 4 itens")
    for i in c["insights"]:
        exige(i.get("tipo") in ("bom", "ruim", "neu"), f"insight '{i.get('titulo')}': tipo deve ser bom, ruim ou neu")
    exige(len(c["proximos"]) == 3, "proximos deve ter 3 itens")
    for p in c.get("posts") or []:
        exige(re.fullmatch(r"\d{2}/[A-Z]{3}", p.get("data", "")) is not None, f"post '{p.get('titulo')}': data no formato '05/NOV'")
    exige(len(c.get("posts") or []) <= 4, "no máximo 4 posts")
    if "whatsapp" in c:
        exige(isinstance(c["whatsapp"], str) and c["whatsapp"].strip(), "whatsapp deve ser um texto")
        exige(len(c.get("whatsapp") or "") <= 1200, f"whatsapp com {len(c.get('whatsapp') or '')} caracteres (máximo 1200)")
    return erros


def normalizar(c):
    """Converte o JSON (marcação simples) para a estrutura usada pelas funções de render."""
    r = dict(c)
    r["nome"] = c["nome"]
    r["titulo"] = [md(t) for t in c["titulo"]]
    r["lead"] = md(c["lead"])
    r["destaque"] = {k: md(v) for k, v in c["destaque"].items()}
    r["faixa"] = [(md(f["valor"]), md(f["legenda"])) for f in c["faixa"]]
    r["intro_p2"] = md(c["intro_p2"])
    r["kpis"] = [{"valor": md(k["valor"]) + (f"<small>{md(k['ref'])}</small>" if k.get("ref") else ""),
                  "rotulo": md(k["rotulo"]),
                  "delta": delta_linha(k["cur"], k["prev"], k["melhor"])} for k in c["kpis"]]
    r["grupos"] = [{"titulo": md(g["titulo"]),
                    "linhas": [(md(l["rotulo"]), l["prev"], l["cur"], l["fmt"], l["melhor"], bool(l.get("destaque")))
                               for l in g["linhas"]]} for g in c["grupos"]]
    r["grafico"] = dict(c["grafico"], titulo=md(c["grafico"]["titulo"]), sub=md(c["grafico"]["sub"]))
    r["fonte"] = md(c["fonte"])
    r["titulo_p3"] = md(c["titulo_p3"], em=True)
    r["intro_p3"] = md(c["intro_p3"])
    if c.get("posts"):
        r["posts"] = [{"data": p["data"], "tag": md(p["tag"]), "titulo": md(p["titulo"]),
                       "metricas": [(md(v), md(l)) for v, l in p["metricas"]]} for p in c["posts"]]
    r["insights"] = [(i["tipo"], md(i["titulo"]), md(i["texto"])) for i in c["insights"]]
    r["leitura"] = md(c["leitura"])
    r["proximos"] = [(md(p["titulo"]), md(p["texto"])) for p in c["proximos"]]
    if c.get("nota_p3"):
        r["nota_p3"] = md(c["nota_p3"])
    return r


def documento(c, sem):
    css = open(os.path.join(AQUI, "estilo.css"), encoding="utf-8").read()
    fontes = open(os.path.join(AQUI, "fonts", "local.css"), encoding="utf-8").read()
    # tabela longa (linhas + títulos de grupo > LIMITE) -> gráfico vai para a página 3
    if c.get("grafico_p3") is None:
        unidades = sum(len(g["linhas"]) + 1 for g in c["grupos"])
        # sem posts, a página 3 tem espaço: o gráfico vai para lá (exceto tabelas curtas)
        c["grafico_p3"] = unidades > LIMITE_TABELA_COM_GRAFICO or (not c.get("posts") and unidades > 9)
    corpo = pagina_capa(c, sem) + pagina_numeros(c, sem, 2) + pagina_leitura(c, sem, 3)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Relatório semanal · {html.escape(c['nome'])}</title>
<style>{fontes}</style><style>{css}</style></head><body>{corpo}</body></html>"""


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    pasta, resto = args[0], args[1:]
    so_validar = "--validar" in resto
    so = {a for a in resto if not a.startswith("--")}
    base = os.path.join(AQUI, "dados", pasta)
    sem = json.load(open(os.path.join(base, "semana.json"), encoding="utf-8"))
    arquivos = sorted(glob.glob(os.path.join(base, "clientes", "*.json")))
    clientes = []
    falhou = False
    for a in arquivos:
        nome = os.path.basename(a)[:-5]
        if so and nome not in so:
            continue
        try:
            c = json.load(open(a, encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"ERRO {nome}: JSON inválido ({e})")
            falhou = True
            continue
        erros = validar(c, sem)
        if erros:
            falhou = True
            for e in erros:
                print(f"ERRO {nome}: {e}")
            continue
        clientes.append(c)
    if so - {os.path.basename(a)[:-5] for a in arquivos}:
        print("ERRO arquivo(s) não encontrado(s):", ", ".join(sorted(so - {os.path.basename(a)[:-5] for a in arquivos})))
        falhou = True
    if falhou:
        sys.exit(2)
    if so_validar:
        print(f"ok {len(clientes)} JSON válido(s)")
        return
    if "--mensagens" in resto:  # só exporta as mensagens de WhatsApp, sem gerar PDF
        exportar_mensagens(sem, clientes)
        return
    saida = os.path.join(AQUI, "..", sem["pasta"])
    os.makedirs(saida, exist_ok=True)
    previa = os.environ.get("PREVIA")  # pasta para salvar PNGs de conferência
    tag = f"{os.getpid()}"  # nomes únicos: várias execuções podem rodar em paralelo
    pares, temporarios = [], []
    for c in clientes:
        # o HTML fica na pasta fonts/ para resolver os arquivos de fonte por caminho relativo
        html_path = os.path.join(AQUI, "fonts", f"_tmp_{tag}_{c['arquivo']}.html")
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(documento(normalizar(c), sem))
        destino = os.path.abspath(os.path.join(saida, f"{c['arquivo']}_Semanal_{sem['sufixo']}.pdf"))
        par = [html_path, destino]
        if previa:
            par.append(os.path.join(previa, f"{c['arquivo']}.png"))
        pares.append(par)
        temporarios.append(html_path)
    lista = os.path.join(AQUI, "fonts", f"_tmp_{tag}_lista.json")
    with open(lista, "w", encoding="utf-8") as fh:
        json.dump(pares, fh)
    temporarios.append(lista)
    rc = subprocess.run(["node", os.path.join(AQUI, "pdf.js"), lista]).returncode
    if os.environ.get("MANTER_HTML") != "1":
        for t in temporarios:
            os.remove(t)
    # semana completa gerada sem erro -> atualiza a pasta downloads/ (PDFs soltos + .zip com todos)
    if rc == 0 and not so and not sem["pasta"].startswith("_"):
        empacotar(sem, [p[1] for p in pares])
        exportar_mensagens(sem, clientes)
    sys.exit(rc)


def exportar_mensagens(sem, clientes):
    """downloads/mensagens_<sufixo>/: um .txt por cliente (pronto para o WhatsApp) + um arquivo com todas + .zip."""
    import zipfile
    raiz = os.path.abspath(os.path.join(AQUI, "..", ".."))
    pasta = os.path.join(raiz, "downloads", f"mensagens_{sem['sufixo']}")
    os.makedirs(pasta, exist_ok=True)
    for antigo in glob.glob(os.path.join(pasta, "*.txt")):
        os.remove(antigo)
    com_msg = [c for c in clientes if c.get("whatsapp")]
    sem_msg = [c["arquivo"] for c in clientes if not c.get("whatsapp")]
    arquivos = []
    for c in com_msg:
        caminho = os.path.join(pasta, f"{c['arquivo']}.txt")
        with open(caminho, "w", encoding="utf-8") as fh:
            fh.write(c["whatsapp"].strip() + "\n")
        arquivos.append(caminho)
    todas = os.path.join(pasta, "_TODAS_AS_MENSAGENS.txt")
    sep = "\n\n" + "=" * 40 + "\n\n"
    with open(todas, "w", encoding="utf-8") as fh:
        fh.write(sep.join(f"[{c['nome']}]\n\n{c['whatsapp'].strip()}" for c in com_msg) + "\n")
    arquivos.append(todas)
    zip_path = os.path.join(raiz, "downloads", f"Mensagens_WhatsApp_{sem['sufixo']}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for a in sorted(arquivos):
            z.write(a, os.path.basename(a))
    print(f"mensagens: {len(com_msg)} em", os.path.relpath(pasta, raiz) + "/", "e", os.path.relpath(zip_path, raiz))
    if sem_msg:
        print("AVISO sem mensagem de WhatsApp:", ", ".join(sem_msg))


def empacotar(sem, pdfs):
    import shutil
    import zipfile
    raiz = os.path.abspath(os.path.join(AQUI, "..", ".."))
    destino = os.path.join(raiz, "downloads", sem["sufixo"])
    os.makedirs(destino, exist_ok=True)
    for antigo in glob.glob(os.path.join(destino, "*.pdf")):
        os.remove(antigo)
    for p in pdfs:
        shutil.copy2(p, destino)
    zip_path = os.path.join(raiz, "downloads", f"Relatorios_Semanais_{sem['sufixo']}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(pdfs):
            z.write(p, os.path.basename(p))
    print("downloads:", os.path.relpath(zip_path, raiz), "e", os.path.relpath(destino, raiz) + "/")


if __name__ == "__main__":
    main()
