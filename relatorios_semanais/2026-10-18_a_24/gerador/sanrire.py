"""Instituto Sanrire: relatório semanal reduzido (capa + 1 página), com ChatGPT Ads."""
import base64
import json
from pathlib import Path

from template import brl, n0, n1, pct, mil, esc, rich, delta, document, cover, topbar, footer, read_box, next_steps

D = Path(__file__).parent / "dados"
GA = json.load(open(D / "gads_week.json"))["sanrire"]
OT = json.load(open(D / "other_week.json"))
YT = OT["sanrire_yt"]
GPT = OT["sanrire_chatgpt"]
GM = OT["sanrire_gads_month_01_25"]

SHORT = {
    "[GO] - [DEMAND GEN] - INSTITUTO SANRIRE - IMPLANTES": ("Implantes", "Demand Gen"),
    "[GO] - [PMAX] - INSTITUTO SANRIRE - LEADS": ("Leads", "PMax"),
    "[GO] - [SEARCH] [TERMOS GERAIS] CLÍNICA ODONTO": ("Termos gerais", "Pesquisa"),
    "[GO] - [SEARCH] - IMPLANTE/ PRÓTESE - LP + LIGAÇÃO": ("Implante/prótese", "Pesquisa"),
    "[GO] - [SEARCH] - ENDODONTIA - LP e LIGAÇÃO": ("Endodontia", "Pesquisa"),
    "[GO] - [SEARCH] - LENTE DE CONTATO - LP + LIGAÇÃO": ("Lente de contato", "Pesquisa"),
    "[GO] - BM | Search | Instituto Sanrire": ("Marca (BM)", "Pesquisa"),
}


def img64(path):
    return "data:image/png;base64," + base64.b64encode(Path(path).read_bytes()).decode()


def build_sanrire(out_dir):
    c, p = GA["cur"], GA["prev"]
    w, m = GPT["week_18_24"], GPT["month_01_25"]
    tot_week = c["cost"] + w["spend"]
    search = [x for x in GA["camp"] if x[1] == "Pesquisa"]
    search_cpc = sum(x[3] for x in search) / sum(x[2] for x in search)
    zero_conv = sum(x[3] for x in GA["camp"] if x[1] == "Pesquisa" and x[5] == 0)
    b = dict(brand="Instituto Sanrire", brand_upper="Instituto Sanrire")
    b["cover"] = dict(
        h1=["Cliques <o>em dobro</o> no Google.", "ChatGPT Ads no ar."],
        intro="Resumo da semana de <b>18 a 24/10</b> no <b>Google Ads</b>, <b>YouTube</b> e <b>ChatGPT Ads</b> do Instituto Sanrire, comparado com a semana anterior (11 a 17/10), com o acumulado do ChatGPT Ads em outubro.",
        hl_num="7.441", hl_lab="CLIQUES", hl_size=46,
        hl_h="<o>7.441 cliques</o> no Google Ads, quase o <o>dobro</o> da semana anterior (3.772).",
        hl_p="O salto veio da nova campanha Demand Gen (4.438 cliques). A Performance Max segue como a principal fonte de contatos: 37 das 44 conversões, a R$ 8,88 cada.",
        extra=f'''<div class="cprints"><div class="k">PRINTS · CHATGPT ADS MANAGER</div>
  <figure><img src="{img64(D / "print_semana.png")}"><figcaption>Semana · 18 a 24/10/2026</figcaption></figure>
  <figure><img src="{img64(D / "print_mes.png")}"><figcaption>Mês · 01 a 25/10/2026</figcaption></figure></div>''',
        strip=[(brl(tot_week, 0), f"investidos na semana: Google {brl(c['cost'], 0)} + ChatGPT {brl(w['spend'], 0)}"),
               (n0(c["conv"]), "conversões no Google Ads (semana anterior: 55)"),
               (brl(m["spend"], 0), f"no ChatGPT Ads em outubro, com {n0(m['clicks'])} cliques (01 a 25/10)"),
               (mil(YT["cur"]["views"]), "visualizações no YouTube, 3,5× a semana anterior")],
    )

    # ---- tabela semana × semana
    def r(lab, pv, cv, pill, hi=False):
        return f'<tr><td>{lab}</td><td class="p">{pv}</td><td class="v"{" style=color:#e85d1b" if hi else ""}>{cv}</td><td>{pill}</td></tr>'
    hp, hc = YT["prev"]["mins"] / 60, YT["cur"]["mins"] / 60
    tbl = ('<table class="cmp3"><thead><tr><th>Métrica</th><th>11-17/10</th><th>18-24/10</th><th>Var.</th></tr></thead><tbody>'
           '<tr class="grp"><td colspan="4">Google Ads</td></tr>'
           + r("Investimento", brl(p["cost"], 0), brl(c["cost"], 0), delta(c["cost"], p["cost"], "neutral"))
           + r("Cliques", n0(p["clicks"]), n0(c["clicks"]), delta(c["clicks"], p["clicks"]), True)
           + r("Impressões", n0(p["impr"]), n0(c["impr"]), delta(c["impr"], p["impr"]))
           + r("Custo por clique", brl(p["cpc"]), brl(c["cpc"]), delta(c["cpc"], p["cpc"], "down"))
           + r("Conversões", n0(p["conv"]), n0(c["conv"]), delta(c["conv"], p["conv"]), True)
           + r("Custo por conversão", brl(p["cpconv"]), brl(c["cpconv"]), delta(c["cpconv"], p["cpconv"], "down"))
           + '<tr class="grp"><td colspan="4">YouTube · canal</td></tr>'
           + r("Visualizações", n0(YT["prev"]["views"]), n0(YT["cur"]["views"]), delta(YT["cur"]["views"], YT["prev"]["views"]))
           + r("Horas assistidas", n1(hp) + " h", n1(hc) + " h", delta(hc, hp))
           + '</tbody></table>')

    rows = []
    for x in sorted(GA["camp"], key=lambda x: -x[3]):
        nm, tp = SHORT[x[0]]
        conv = x[5]
        cc = brl(x[8]) if conv > 0 else '<span style="color:#a3acc2">—</span>'
        cls = ' class="best"' if nm == "Leads" else ""
        new = ' <span class="tg" style="background:#fdf0e9;color:#e85d1b">nova</span>' if tp == "Demand Gen" else ""
        rows.append(f'<tr><td style="white-space:nowrap"><span class="tg" style="margin:0 5px 0 0">{tp}</span><span class="nm">{nm}</span>{new}</td><td>{brl(x[3], 0)}</td><td>{n0(x[2])}</td>'
                    f'<td class="strong">{n1(conv) if conv and conv != int(conv) else n0(conv)}</td><td{cls}>{cc}</td></tr>')
    camp = ('<table class="ct"><thead><tr><th>Campanha</th><th>Invest.</th><th>Cliques</th><th>Conv.</th><th>Custo/conv.</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table>')

    def per(t, sub, d, on=False):
        cpm = d["spend"] / d["impr"] * 1000
        cells = [(brl(d["spend"]), "investimento"), (n0(d["impr"]), "impressões"), (n0(d["clicks"]), "cliques"),
                 (pct(d["ctr"], 2), "CTR"), (brl(d["cpc"]), "CPC médio"), (brl(cpm), "CPM")]
        g = "".join(f'<div><div class="v">{v}</div><div class="t">{tt}</div></div>' for v, tt in cells)
        return f'<div class="per{" on" if on else ""}"><div class="ph"><span class="a">{t}</span><span class="b">{sub}</span></div><div class="g">{g}</div></div>'

    gpt = f'''
<div class="gpt">
  <div class="top"><div><div class="k">02 · NOVO CANAL · CHATGPT ADS (OPENAI)</div>
    <div class="h">Campanha <span class="o">{esc(w["campaign"])}</span></div>
    <div class="cmp">Anúncios dentro do ChatGPT. A 2ª campanha (Instituto Sanrire Odontologia e Health) não teve entrega.</div></div>
    <span class="tag">Conversões ainda não configuradas</span></div>
  <div class="pair">{per("Semana", "18 A 24/10 · 7 DIAS", w, True)}{per("Mês", "01 A 25/10 · 25 DIAS", m)}</div>
  <p class="fn">Fonte: prints do OpenAI Ads Manager (beta) de 26/10/2026, reproduzidos na capa. A plataforma exibe o aviso “Insight metrics delayed”: métricas de investimento podem ser revisadas. CPM calculado (investimento ÷ impressões × 1.000).</p>
</div>'''

    page2 = f'''
<section class="page">
  {topbar(b["brand_upper"], "Relatório semanal · reduzido", "Semana de 18 a 24/10/2026")}
  <div class="content">
    <div class="sec"><span class="n">01</span><span>Semana × semana anterior</span></div>
    <h2>Google, YouTube e <span class="o">ChatGPT Ads</span></h2>
    <p class="lead">Os cliques no Google dobraram com a estreia da <b>Demand Gen</b>, e as visualizações do YouTube subiram 3,5× junto com ela. As conversões caíram 20% (55 → 44), puxadas pela Performance Max (50 → 37).</p>
    <div class="split" style="grid-template-columns:1fr 1.08fr">
      <div class="card"><div class="card-h"><span class="a">Semana a semana</span><span class="b">Google Ads · YouTube</span></div>{tbl}</div>
      <div class="card"><div class="card-h"><span class="a">Google Ads · campanhas</span><span class="b">{brl(c["cost"], 0)} · {n0(c["conv"])} conv.</span></div>{camp}
        <p class="note" style="margin-top:7px">Outubro (01 a 25/10): {brl(GM["cost"], 0)} investidos, {n0(GM["clicks"])} cliques e {n0(GM["conv"])} conversões no Google Ads ({brl(GM["cpconv"])} por conversão).</p></div>
    </div>
    {gpt}
    {read_box(f"O clique no ChatGPT Ads custou <b>{brl(w['cpc'])}</b> na semana (média do mês: {brl(m['cpc'])}), perto do CPC das campanhas de Pesquisa do Google ({brl(search_cpc)}) e bem acima de PMax e Demand Gen. "
              f"Sem conversão configurada, ainda não dá para saber quantos contatos o canal gera. No Google, quatro campanhas de Pesquisa somaram <b>{brl(zero_conv, 0)} sem conversões</b> na semana.")}
    {next_steps([
        ("Conversões no ChatGPT Ads", "Configurar o evento de conversão (WhatsApp, ligação ou formulário) no Ads Manager da OpenAI para medir o custo por contato."),
        ("Rever a Pesquisa", f"Termos gerais, Endodontia, Lente de contato e Marca somaram {brl(zero_conv, 0)} sem conversões: revisar termos, lances e página de destino."),
        ("PMax como base", "Manter a Performance Max (R$ 8,88 por conversão) como principal campanha e acompanhar a Demand Gen, que traz volume mas converte caro (R$ 99)."),
    ])}
    <p class="note">Fonte: Reportei (Google Ads e YouTube) e OpenAI Ads Manager. Conversões do Google Ads podem ter casas decimais (modelo de atribuição); totais arredondados. YouTube: 24/10 ainda não consolidado.</p>
  </div>
  {footer(b["brand"] + " · reduzido", 2)}
</section>'''

    html = document("Instituto Sanrire · Relatório semanal reduzido 18 a 24/10/2026", [cover(b), page2])
    path = Path(out_dir) / "Relatorio_Semanal_Reduzido_Instituto_Sanrire_18-24out2026.html"
    path.write_text(html, encoding="utf-8")
    return path
