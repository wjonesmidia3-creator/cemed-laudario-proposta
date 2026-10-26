"""Gera os relatórios semanais (18 a 24/10/2026) no modelo Grupo Opera."""
import json
import sys
from pathlib import Path

from template import (brl, n0, n1, pct, mil, esc, rich, delta, delta_txt, document, cover, page_numbers,
                      topbar, footer, svg_daily_pair, svg_daily_single, meta_table, gads_table, posts_list,
                      read_box, next_steps, platform_split)

D = Path(__file__).parent / "dados"
FB = json.load(open(D / "fbads_week.json"))
GA = json.load(open(D / "gads_week.json"))
IG = json.load(open(D / "ig_week.json"))
OT = json.load(open(D / "other_week.json"))
MO = json.load(open(D / "month.json"))
FIO = json.load(open(D / "fiorini_daily.json"))
PL = json.load(open(D / "platform.json"))


def plat(k, note=""):
    c = FB[k]["cur"]
    rows = [("Facebook", *PL[k]["facebook"]), ("Instagram", *PL[k]["instagram"])]
    return platform_split(rows, c["spend"], c["conv"], note)

DIAS14 = [f"{d:02d}/10" for d in range(11, 25)]
NOTE_BASE = "Fonte: Reportei ({fontes}). Semana atual: 18 a 24/10/2026; semana anterior: 11 a 17/10/2026; acumulado de outubro: 01 a 25/10/2026."


def meta_rows(k, extra=()):
    c, p = FB[k]["cur"], FB[k]["prev"]
    rows = [
        ("Conversas iniciadas", n0(p["conv"]), n0(c["conv"]), delta(c["conv"], p["conv"], "up"), True),
        ("Custo por conversa", brl(p["cpconv"]), brl(c["cpconv"]), delta(c["cpconv"], p["cpconv"], "down"), True),
        ("Investimento", brl(p["spend"], 0), brl(c["spend"], 0), delta(c["spend"], p["spend"], "neutral"), False),
        ("Alcance", n0(p["reach"]), n0(c["reach"]), delta(c["reach"], p["reach"], "up"), False),
        ("Impressões", n0(p["impr"]), n0(c["impr"]), delta(c["impr"], p["impr"], "up"), False),
        ("Cliques no link", n0(p["lclicks"]), n0(c["lclicks"]), delta(c["lclicks"], p["lclicks"], "up"), False),
    ]
    return rows + list(extra)


def ig_rows(k, posts_prev=None, posts_cur=None, followers=True):
    c, p = IG[k]["cur"], IG[k]["prev"]
    rows = [
        ("Alcance (soma diária)", n0(p["reach"]), n0(c["reach"]), delta(c["reach"], p["reach"], "up"), False),
        ("Visualizações", n0(p["views"]), n0(c["views"]), delta(c["views"], p["views"], "up"), False),
        ("Visitas ao perfil", n0(p["pv"]), n0(c["pv"]), delta(c["pv"], p["pv"], "up"), False),
    ]
    if followers:
        dif = c["fol"] - p["fol"]
        cls = "pos" if dif > 0 else ("neg" if dif < 0 else "neu")
        sign = "+" if dif > 0 else ""
        rows.append(("Seguidores (fim da semana)", n0(p["fol"]), n0(c["fol"]), f'<span class="pill {cls}">{sign}{n0(dif)}</span>', False))
    if posts_cur is not None:
        rows.append(("Publicações no feed", n0(posts_prev), n0(posts_cur), delta(posts_cur, posts_prev, "up") if posts_prev else "", False))
    return rows


def gads_rows(k, conv=True, ctr=False):
    c, p = GA[k]["cur"], GA[k]["prev"]
    dash = "—"
    pv = lambda v, f: dash if not p["cost"] else f(v)
    rows = [
        ("Investimento", pv(p["cost"], lambda v: brl(v, 0) if v >= 100 else brl(v)), brl(c["cost"], 0) if c["cost"] >= 100 else brl(c["cost"]), delta(c["cost"], p["cost"], "neutral"), False),
        ("Cliques", pv(p["clicks"], n0), n0(c["clicks"]), delta(c["clicks"], p["clicks"], "up"), False),
    ]
    if ctr:
        rows.append(("CTR", pv(p["ctr"], lambda v: pct(v * 100)), pct(c["ctr"] * 100), delta(c["ctr"], p["ctr"], "up"), False))
    rows.append(("Custo por clique", pv(p["cpc"], brl), brl(c["cpc"]), delta(c["cpc"], p["cpc"], "down"), False))
    if conv:
        rows.append(("Conversões", pv(p["conv"], n0), n0(c["conv"]), delta(c["conv"], p["conv"], "up"), True))
        rows.append(("Custo por conversão", pv(p["cpconv"], brl), brl(c["cpconv"]) if c["conv"] else "—", delta(c["cpconv"], p["cpconv"], "down") if c["conv"] else "", True))
    return rows


def page_campaigns(b, blocks, n=3, sec="Campanhas e conteúdo"):
    return f'''
<section class="page">
  {topbar(b["brand_upper"], "Campanhas e conteúdo", "Semana de 18 a 24/10/2026")}
  <div class="content">
    <div class="sec"><span class="n">02</span><span>{esc(sec)}</span></div>
    {"".join(blocks)}
  </div>
  {footer(b["brand"], n)}
</section>'''


def h2lead(h2, lead):
    return f'<h2>{rich(h2)}</h2><p class="lead">{rich(lead)}</p>'


def card(title, sub, body, style=""):
    return f'<div class="card" style="{style}"><div class="card-h"><span class="a">{rich(title)}</span><span class="b">{rich(sub)}</span></div>{body}</div>'


def ig_block(k, posts_html, sub_posts, title_posts="Publicações da semana"):
    prev = MO["ig_reach_daily_prev_11_17"][k]
    cur = IG[k]["reach_daily_cur"]
    chart = svg_daily_pair(prev, cur, DIAS14, w=318, h=150)
    left = (f'<div class="card"><div class="card-h"><span class="a">Alcance diário no Instagram</span><span class="b">11 a 24/10</span></div>'
            f'{chart}<div class="legend"><span><i style="background:#00247d"></i>Semana anterior</span><span><i style="background:#e85d1b"></i>Semana atual</span></div></div>')
    right = f'<div class="card"><div class="card-h"><span class="a">{title_posts}</span><span class="b">{sub_posts}</span></div>{posts_html}</div>'
    return f'<div class="split">{left}{right}</div>'


# ====================================================================== EGO
def ego():
    k = "ego"
    c, p = FB[k]["cur"], FB[k]["prev"]
    b = dict(brand="EGO Odontologia", brand_upper="EGO Odontologia", slug="EGO_Odontologia")
    b["cover"] = dict(
        h1=["Conversas <o>em dobro</o>.", "Custo pela metade."],
        intro="Resumo da semana de <b>18 a 24/10</b> nos <b>anúncios Meta</b>, <b>Google Ads</b>, <b>Instagram</b> e <b>Facebook</b> da EGO Odontologia, comparado com a semana anterior (11 a 17/10).",
        hl_num="82", hl_lab="CONVERSAS",
        hl_h="<o>82 conversas</o> na semana, contra <o>42</o> na anterior, com menos investimento.",
        hl_p="Pessoas que chamaram a clínica por mensagem (WhatsApp, Direct ou Messenger) a partir dos anúncios. O investimento no Meta foi R$ 259 menor que na semana anterior.",
        strip=[(brl(c["cpconv"]), f"custo por conversa (semana anterior: {brl(p['cpconv'])})"),
               (brl(c["cpc"]), "custo por clique, 40% menor que na semana anterior"),
               (n0(c["lclicks"]), "cliques no link dos anúncios, 48% a mais"),
               ("203", "conversas iniciadas em outubro (01 a 25/10)")],
    )
    m = MO["fbads"][k]
    b["numbers"] = dict(
        h2="Os números, <o>semana a semana</o>",
        lead="Com <b>14% menos verba</b> no Meta, a conta entregou quase o <b>dobro de conversas</b> e cliques bem mais baratos. O Google Ads estreou no sábado (24/10).",
        kpis=[
            dict(v="82", small="/42", t="Conversas iniciadas<br>semana atual / anterior", d=delta_txt(c["conv"], p["conv"], "up")),
            dict(v=brl(c["cpconv"]), t="Custo por conversa<br>nos anúncios Meta", d=delta_txt(c["cpconv"], p["cpconv"], "down")),
            dict(v=brl(c["cpc"]), t="Custo por clique<br>nos anúncios Meta", d=delta_txt(c["cpc"], p["cpc"], "down")),
            dict(v=pct(c["ctr"]), t="Taxa de cliques (CTR)<br>dos anúncios", d=("pos", f"▲ era {pct(p['ctr'])} na semana anterior")),
        ],
        groups=[
            ("Anúncios · Meta Ads", meta_rows(k)),
            ("Google Ads · estreia em 24/10", [
                ("Investimento", "—", brl(GA[k]["cur"]["cost"]), '<span class="pill neu">novo</span>', False),
                ("Cliques / impressões", "—", f'{n0(GA[k]["cur"]["clicks"])} / {n0(GA[k]["cur"]["impr"])}', "", False)]),
            ("Instagram", ig_rows(k)),
            ("Facebook · página", [
                ("Alcance da página", n0(IG[k]["fb_page"]["prev"]["reach"]), n0(IG[k]["fb_page"]["cur"]["reach"]), delta(IG[k]["fb_page"]["cur"]["reach"], IG[k]["fb_page"]["prev"]["reach"]), False),
                ("Visualizações", n0(IG[k]["fb_page"]["prev"]["views"]), n0(IG[k]["fb_page"]["cur"]["views"]), delta(IG[k]["fb_page"]["cur"]["views"], IG[k]["fb_page"]["prev"]["views"]), False)]),
        ],
        mtd=("Meta Ads · 01 a 25/10", f"O custo por conversa da semana ficou <b style='color:#fff'>38% abaixo</b> da média do mês.",
             [(brl(m["spend"], 0), "investidos no Meta"), (n0(m["conv"]), "conversas iniciadas"),
              (brl(m["cpconv"]), "custo médio por conversa"), (n0(m["lclicks"]), "cliques no link")]),
        note=NOTE_BASE.format(fontes="Meta Ads, Google Ads, Instagram Business e Página do Facebook") + " Alcance do Instagram = soma do alcance diário (orgânico + pago).",
    )
    camps = FB[k]["camp"]
    blocks = [
        h2lead("Onde a verba <o>trabalhou</o>",
               "A <b>GO_OLDADS_TESTEA</b> ficou com 93% do investimento: trouxe 3.520 cliques no link a R$ 0,42 e respondeu por cerca de 75 das 82 conversas da conta."),
        card("Meta Ads · campanhas", f"Total {brl(c['spend'])} · {n0(c['conv'])} conversas na conta", meta_table(camps, c["spend"])
             + '<p class="note" style="margin-top:6px">O resultado de cada campanha segue o objetivo configurado. A GO_OLDADS_TESTEA otimiza para clique no link; as outras três somaram 7 conversas; as 75 restantes da conta são atribuídas a ela.</p>'),
        ig_block(k, posts_list(IG[k]["posts"], 2), "2 posts · 20 e 22/10"),
        read_box("A queda de alcance no Instagram (−75%) acompanha a entrega dos anúncios, que se concentrou no Facebook: o alcance pago no Instagram caiu 34%, enquanto as impressões no Facebook subiram 4%. "
                 "O conteúdo segue respondendo: o Reels sobre falta de osso para implante somou <b>238 visualizações e 18 interações</b>, o melhor post da semana. "
                 "No Meta, a GO_IMPLANTES teve a conversa mais barata (R$ 9,84), mas com só R$ 39 investidos."),
        next_steps([
            ("Testar mais verba em Implantes", "A GO_IMPLANTES teve o menor custo por conversa (R$ 9,84). Vale subir o orçamento para confirmar com mais volume."),
            ("Instagram de volta à entrega", "Reforçar os posicionamentos de Reels e Stories nos anúncios e impulsionar o Reels de implante para recuperar o alcance no perfil."),
            ("Acompanhar o Google Ads", "A campanha de pesquisa estreou em 24/10. Na próxima semana: revisar termos de busca e conferir o registro de conversões."),
        ]),
        '<p class="note">Campanha GO_PROTOCOLO: 1 conversa a R$ 35,27 (amostra pequena). Google Ads: campanha GO_Generico_Long_Tail (Pesquisa), R$ 4,66, 2 cliques e 37 impressões em 24/10. Posts: números acumulados desde a publicação até 24/10.</p>',
    ]
    return b, blocks


# ====================================================================== CEMED
def cemed():
    k = "cemed"
    c, p = FB[k]["cur"], FB[k]["prev"]
    g = GA[k]["cur"]
    b = dict(brand="CEMED", brand_upper="CEMED · Mirassol", slug="CEMED")
    tot = c["spend"] + g["cost"]
    b["cover"] = dict(
        h1=["Contatos <o>multiplicados</o>.", "Google Ads de volta ao ar."],
        intro="Resumo da semana de <b>18 a 24/10</b> nos <b>anúncios Meta</b> e no <b>Google Ads</b> do CEMED (Centro de Especialidades Médicas de Mirassol), comparado com a semana anterior (11 a 17/10).",
        hl_num="60", hl_lab="CONTATOS",
        hl_h="<o>60 contatos</o> na semana: <o>27 conversas</o> pelo Meta e <o>33 conversões</o> no Google.",
        hl_p="Na semana anterior foram 7 conversas, sem veiculação no Google Ads. As campanhas de pesquisa voltaram a rodar em 19/10.",
        strip=[(brl(c["cpconv"]), f"custo por conversa no Meta (semana anterior: {brl(p['cpconv'])})"),
               (brl(g["cpconv"]), "custo por conversão no Google Ads"),
               (brl(tot, 0), "investimento total da semana (Meta + Google)"),
               ("141", "contatos em outubro: 85 conversas + 56 conversões (01 a 25/10)")],
    )
    mf, mg = MO["fbads"][k], MO["gads"][k]
    b["numbers"] = dict(
        h2="Os números, <o>semana a semana</o>",
        lead="As conversas pelo Meta quase <b>quadruplicaram</b> (7 → 27) e o custo por conversa caiu 64%. Com o Google Ads de volta desde 19/10, a semana fechou com <b>60 contatos</b>.",
        kpis=[
            dict(v="27", small="/7", t="Conversas pelo Meta<br>semana atual / anterior", d=delta_txt(c["conv"], p["conv"], "up")),
            dict(v=brl(c["cpconv"]), t="Custo por conversa<br>nos anúncios Meta", d=delta_txt(c["cpconv"], p["cpconv"], "down")),
            dict(v="33", t="Conversões no Google Ads<br>em 5 dias de veiculação", d=("pos", f"▲ {brl(g['cpconv'])} por conversão")),
            dict(v=brl(tot, 0), t="Investimento total<br>Meta + Google", d=("neu", f"Meta {brl(c['spend'],0)} · Google {brl(g['cost'],0)}")),
        ],
        groups=[
            ("Anúncios · Meta Ads", meta_rows(k)),
            ("Google Ads · voltou em 19/10", gads_rows(k, conv=True, ctr=True)),
        ],
        mtd=("Meta + Google · 01 a 25/10", "O Google Ads ficou sem veiculação de 07 a 18/10.",
             [(brl(mf["spend"] + mg["cost"], 0), "investidos (Meta + Google)"), ("141", "contatos: 85 conversas + 56 conversões"),
              (brl(mf["cpconv"]), "custo médio por conversa no Meta"), (brl(mg["cost"] / mg["conv"]), "custo médio por conversão no Google")]),
        note=NOTE_BASE.format(fontes="Meta Ads e Google Ads") + " Conversões do Google Ads conforme as ações configuradas na conta.",
    )
    dc = MO["gads"][k]["daily_cost"]
    days = [f"{d:02d}/10" for d in range(1, 26)]
    vals = [dc.get(f"2026-10-{d:02d}", 0) for d in range(1, 26)]
    chart = svg_daily_single(days, vals, w=318, h=132, color=lambda i: "#e85d1b" if i >= 18 else "#00247d", mark=(6, 17, "sem veiculação"))
    gc = GA[k]["camp"]
    blocks = [
        h2lead("Onde a verba <o>trabalhou</o>",
               "No Google, a campanha de <b>ultrassonografia (USG)</b> trouxe 2 de cada 3 conversões, com custo menor que a de especialidades. No Meta, uma campanha única de mensagens entregou o contato mais barato da conta."),
        card("Meta Ads · campanhas", f"Total {brl(c['spend'])} · {n0(c['conv'])} conversas", meta_table(FB[k]["camp"], c["spend"])),
        plat("cemed", "No Facebook, cada conversa custou R$ 11,66; no Instagram, R$ 15,03."),
        card("Google Ads · campanhas", f"Total {brl(g['cost'])} · {n0(g['conv'])} conversões", gads_table(gc)),
        f'''<div class="split"><div class="card"><div class="card-h"><span class="a">Investimento diário no Google Ads</span><span class="b">01 a 25/10</span></div>{chart}
        <div class="legend"><span><i style="background:#00247d"></i>Início de outubro</span><span><i style="background:#e85d1b"></i>Retomada (19/10)</span></div></div>
        <div class="card"><div class="card-h"><span class="a">Custo por contato</span><span class="b">semana atual</span></div>
        <div class="fmt" style="border:0;padding:4px 0 0"><div class="g" style="grid-template-columns:1fr 1fr">
          <div><div class="v">{brl(c["cpconv"])}</div><div class="t">por conversa no Meta<br>(27 conversas)</div></div>
          <div><div class="v">{brl(gc[0][8])}</div><div class="t">por conversão em USG<br>(22 conversões)</div></div>
          <div style="margin-top:10px"><div class="v">{brl(gc[1][8])}</div><div class="t">por conversão em<br>especialidades (11)</div></div>
          <div style="margin-top:10px"><div class="v">{brl(tot/60)}</div><div class="t">custo médio por contato<br>(60 no total)</div></div>
        </div></div></div></div>''',
        read_box("A retomada do Google Ads mudou o patamar da semana: 33 conversões em 5 dias, a R$ 24,10 cada. A pausa de 07 a 18/10 deixou o CEMED só com o Meta nesse período. "
                 "No Meta, o custo por conversa caiu de R$ 36,00 para <b>R$ 12,91</b> com 38% a mais de investimento, na mesma campanha única de mensagens."),
        next_steps([
            ("Google Ads sem pausas", "Manter orçamento contínuo nas campanhas de pesquisa: a pausa de 12 dias zerou os contatos vindos do Google."),
            ("Especialidades no Meta", "Testar conjuntos de anúncios para USG e para as especialidades da campanha de pesquisa do Google."),
            ("Contato → agendamento", "Cruzar os 60 contatos com os agendamentos da recepção para chegar ao custo por paciente agendado."),
        ]),
    ]
    return b, blocks


# ====================================================================== DREISSON
def dreisson():
    k = "dreisson"
    c, p = FB[k]["cur"], FB[k]["prev"]
    b = dict(brand="Dreisson Vivo Imóveis", brand_upper="Dreisson · Vivo Imóveis", slug="Dreisson_Vivo_Imoveis")
    m = MO["fbads"][k]
    camps = FB[k]["camp"]
    car, reel, seg = camps[0], camps[1], camps[2]
    b["cover"] = dict(
        h1=["Mais verba, <o>mais conversas</o>.", "27 contatos na semana."],
        intro="Resumo da semana de <b>18 a 24/10</b> nos <b>anúncios Meta</b> (Facebook e Instagram) de Dreisson · Vivo Imóveis, comparado com a semana anterior (11 a 17/10).",
        hl_num="27", hl_lab="CONVERSAS",
        hl_h="<o>27 conversas</o> no WhatsApp, <o>50% a mais</o> que na semana anterior (18).",
        hl_p="Pessoas que chamaram por mensagem a partir dos anúncios. O carrossel foi o formato mais eficiente, com conversa a R$ 13,06.",
        strip=[(brl(c["cpconv"]), f"custo por conversa (semana anterior: {brl(p['cpconv'])})"),
               (mil(c["reach"]), "pessoas alcançadas pelos anúncios, 22% a mais"),
               ("319", "visitas ao perfil pela campanha de seguidores, a R$ 0,22"),
               (n0(m["conv"]), "conversas iniciadas em outubro (01 a 25/10)")],
    )
    b["numbers"] = dict(
        h2="Os números, <o>semana a semana</o>",
        lead="O investimento subiu <b>68%</b> e as conversas cresceram <b>50%</b>. O custo por conversa subiu 12%, para R$ 17,99, em linha com a média do mês (R$ 18,02).",
        kpis=[
            dict(v="27", small="/18", t="Conversas iniciadas<br>semana atual / anterior", d=delta_txt(c["conv"], p["conv"], "up")),
            dict(v=brl(c["cpconv"]), t="Custo por conversa<br>nos anúncios Meta", d=delta_txt(c["cpconv"], p["cpconv"], "down")),
            dict(v=mil(c["reach"]), t="Pessoas alcançadas<br>pelos anúncios", d=delta_txt(c["reach"], p["reach"], "up")),
            dict(v=brl(c["spend"], 0), t="Investimento<br>na semana", d=delta_txt(c["spend"], p["spend"], "neutral")),
        ],
        groups=[("Anúncios · Meta Ads", meta_rows(k, extra=[
            ("Custo por clique", brl(p["cpc"]), brl(c["cpc"]), delta(c["cpc"], p["cpc"], "down"), False),
            ("CTR", pct(p["ctr"]), pct(c["ctr"]), delta(c["ctr"], p["ctr"], "up"), False)]))],
        mtd=("Meta Ads · 01 a 25/10", "A semana respondeu por quase 1/3 das conversas do mês.",
             [(brl(m["spend"], 0), "investidos no Meta"), (n0(m["conv"]), "conversas iniciadas"),
              (brl(m["cpconv"]), "custo médio por conversa"), (n0(m["lclicks"]), "cliques no link")]),
        extra=plat("dreisson", "No Facebook, cada conversa custou <b>R$ 9,65</b>; no Instagram, R$ 34,66, mesmo ficando com 64% da verba."),
        note=NOTE_BASE.format(fontes="Meta Ads"),
    )

    def fmt_card(c_, title, kick, win=False):
        return (f'<div class="fmt{" win" if win else ""}"><div class="k">{kick}</div><div class="h">{title}</div><div class="g">'
                f'<div><div class="v">{n0(c_[1])}</div><div class="t">conversas</div></div>'
                f'<div><div class="v">{brl(c_[3])}</div><div class="t">por conversa</div></div>'
                f'<div><div class="v">{pct(c_[7])}</div><div class="t">CTR</div></div>'
                f'<div><div class="v">{brl(c_[9])}</div><div class="t">CPM</div></div></div></div>')
    blocks = [
        h2lead("Carrossel × Reels: <o>quem converte</o>",
               "As duas campanhas de WhatsApp receberam a mesma verba (cerca de R$ 207 cada). O <b>carrossel</b> trouxe 16 conversas; o Reels, 11, mesmo com quase o dobro de taxa de cliques."),
        f'<div class="duo">{fmt_card(car, "[OZ] [WHATS] CARROSSEL", "MELHOR CUSTO POR CONVERSA", True)}{fmt_card(reel, "[OZ] [WHATS] | REELS", "MAIS CLIQUES, MENOS CONVERSAS")}</div>',
        card("Meta Ads · campanhas", f"Total {brl(c['spend'])} · {n0(c['conv'])} conversas", meta_table(camps, c["spend"])),
        card("Do anúncio à conversa", "semana atual · semana anterior entre parênteses",
             f'''<div class="funnel">
               <div class="fs"><div class="k">Pessoas alcançadas</div><div class="v">{n0(c["reach"])}</div><div class="p">({n0(p["reach"])})</div></div>
               <div class="fs"><div class="k">Cliques no link</div><div class="v">{n0(c["lclicks"])}</div><div class="p">({n0(p["lclicks"])})</div></div>
               <div class="fs"><div class="k">Conversas no WhatsApp</div><div class="v">{n0(c["conv"])}</div><div class="p">({n0(p["conv"])})</div></div></div>
             <div class="frate"><div>Clique no link a cada 100 alcançados: <b>{n1(c["lclicks"]/c["reach"]*100)}</b> ({n1(p["lclicks"]/p["reach"]*100)})</div>
             <div>Conversa a cada 100 cliques no link: <b>{n1(c["conv"]/c["lclicks"]*100)}</b> ({n1(p["conv"]/p["lclicks"]*100)})</div></div>'''),
        read_box("O carrossel converte melhor: cada conversa custou <b>R$ 13,06</b>, contra R$ 18,81 no Reels. O Reels atrai mais cliques (CTR de 6,2% contra 3,4%), mas gera menos conversas por real investido. "
                 "A campanha de seguidores levou <b>319 pessoas ao perfil</b> a R$ 0,22 cada, e esse público pode ser reaproveitado em remarketing."),
        next_steps([
            ("Priorizar o carrossel", "Mover parte da verba do Reels para o carrossel e testar novos imóveis no mesmo formato. No Reels, chamada para o WhatsApp logo no início."),
            ("Mais entrega no Facebook", "No Facebook a conversa custou R$ 9,65, contra R$ 34,66 no Instagram. Testar mais verba nos posicionamentos do Facebook."),
            ("Remarketing", "Criar campanha de mensagem para quem visitou o perfil ou interagiu com os anúncios nos últimos 30 dias."),
        ]),
    ]
    return b, blocks


# ====================================================================== D'PLACIDO
def dplacido():
    k = "dplacido"
    c, p = FB[k]["cur"], FB[k]["prev"]
    b = dict(brand="D’Placido Odontologia", brand_upper="D’Placido Odontologia", slug="DPlacido_Odontologia")
    m = MO["fbads"][k]
    b["cover"] = dict(
        h1=["<o>100 conversas</o> na semana.", "Protocolo puxou 55 delas."],
        intro="Resumo da semana de <b>18 a 24/10</b> nos <b>anúncios Meta</b> e no <b>Instagram</b> (@dralucianadeplacido) da D’Placido Odontologia, comparado com a semana anterior (11 a 17/10).",
        hl_num="100", hl_lab="CONVERSAS",
        hl_h="<o>55 das 100 conversas</o> vieram da campanha de <o>Protocolo</o>, a R$ 2,54 cada.",
        hl_p="Volume abaixo da semana anterior (132), com o mesmo investimento. O custo médio por conversa segue baixo: R$ 7,34.",
        strip=[(brl(c["cpconv"]), f"custo por conversa (semana anterior: {brl(p['cpconv'])})"),
               ("R$ 2,54", "por conversa na campanha de Protocolo"),
               (mil(c["reach"]), "pessoas alcançadas pelos anúncios"),
               (n0(m["conv"]), "conversas iniciadas em outubro (01 a 25/10)")],
    )
    b["numbers"] = dict(
        h2="Os números, <o>semana a semana</o>",
        lead="Com investimento estável (R$ 734), as conversas caíram <b>24%</b> e o custo por conversa subiu para <b>R$ 7,34</b>, ainda perto da média do mês (R$ 7,46). No Instagram, a semana ficou sem publicações.",
        kpis=[
            dict(v="100", small="/132", t="Conversas iniciadas<br>semana atual / anterior", d=delta_txt(c["conv"], p["conv"], "up")),
            dict(v=brl(c["cpconv"]), t="Custo por conversa<br>nos anúncios Meta", d=delta_txt(c["cpconv"], p["cpconv"], "down")),
            dict(v="55", t="Conversas na campanha<br>de Protocolo", d=("pos", "▼ R$ 2,54 por conversa")),
            dict(v=n0(IG[k]["cur"]["views"]), t="Visualizações<br>no Instagram", d=delta_txt(IG[k]["cur"]["views"], IG[k]["prev"]["views"], "up")),
        ],
        groups=[("Anúncios · Meta Ads", meta_rows(k)),
                ("Instagram · @dralucianadeplacido", ig_rows(k, posts_prev=2, posts_cur=0))],
        mtd=("Meta Ads · 01 a 25/10", "Custo por conversa da semana próximo da média do mês.",
             [(brl(m["spend"], 0), "investidos no Meta"), (n0(m["conv"]), "conversas iniciadas"),
              (brl(m["cpconv"]), "custo médio por conversa"), (n0(m["lclicks"]), "cliques no link")]),
        extra=plat("dplacido", "O Facebook trouxe 54% das conversas com 40% da verba: R$ 5,43 por conversa, contra R$ 9,57 no Instagram."),
        note=NOTE_BASE.format(fontes="Meta Ads e Instagram Business") + " Publicações no feed: posts e Reels publicados na semana (11 a 17/10: 12/10 e 17/10).",
    )
    rp = MO["dplacido_recent_posts"]
    inv = rp[2]
    side = (f'<div class="post"><div class="dt" style="background:#e85d1b"><div class="d1">0</div><div class="d2" style="color:#fff">POSTS</div></div>'
            f'<div><div class="tp">Semana sem publicações</div><div class="cap">Último post em 17/10. O feed ficou parado de 18 a 24/10.</div>'
            f'<div class="ms">Alcance −14% · visitas ao perfil +22% · −3 seguidores</div></div></div>'
            f'<div class="post"><div class="dt"><div class="d1">10</div><div class="d2">OUT</div></div>'
            f'<div><div class="tp">Destaque do mês · Carrossel</div><div class="cap">“Quer usar aparelho, mas não quer que ele apareça?” (Invisalign)</div>'
            f'<div class="ms"><b>{n0(inv[3])}</b> alcance · <b>{n0(inv[4])}</b> views · <b>{n0(inv[5])}</b> interações</div></div></div>'
            f'<div class="post"><div class="dt"><div class="d1">17</div><div class="d2">OUT</div></div>'
            f'<div><div class="tp">Mais interações do mês · Imagem</div><div class="cap">“My family” (post pessoal)</div>'
            f'<div class="ms"><b>{n0(rp[0][3])}</b> alcance · <b>{n0(rp[0][4])}</b> views · <b>{n0(rp[0][5])}</b> interações</div></div></div>')
    blocks = [
        h2lead("Onde a verba <o>trabalhou</o>",
               "<b>Protocolo</b> segue como a campanha mais eficiente da conta: 55 conversas a R$ 2,54, com 19% da verba. Depoimentos recebeu a maior fatia (33%) e entregou 15 conversas a R$ 16,33."),
        card("Meta Ads · campanhas", f"Total {brl(c['spend'])} · {n0(c['conv'])} conversas", meta_table(FB[k]["camp"], c["spend"])),
        ig_block(k, side, "18 a 24/10", title_posts="Conteúdo"),
        read_box("Em Protocolo, a conversa custa <b>menos de um sexto</b> do que em Depoimentos e Base Antiga – Top Leads (R$ 16,33 e R$ 17,50). "
                 "Sem posts na semana, o Instagram perdeu alcance (−14%) e 3 seguidores. Conteúdo de tratamento funciona no perfil: o carrossel de Invisalign alcançou 838 contas, o maior alcance entre os posts de outubro."),
        next_steps([
            ("Mais verba em Protocolo", "Mover parte do orçamento de Base Antiga e Depoimentos para Protocolo, acompanhando se o custo se mantém."),
            ("Voltar a publicar", "Retomar pelo menos 3 posts por semana, alternando tratamento (como o carrossel de Invisalign) e bastidores da Dra. Luciana."),
            ("Novos depoimentos", "Testar novos vídeos de depoimento para baixar o custo por conversa dessa campanha, hoje em R$ 16,33."),
        ]),
    ]
    return b, blocks


# ====================================================================== TRAIT
def trait():
    k = "trait"
    c, p = FB[k]["cur"], FB[k]["prev"]
    gm = OT["trait_gmb"]
    b = dict(brand="Trait Odontologia", brand_upper="Trait Odontologia", slug="Trait_Odontologia")
    m = MO["fbads"][k]
    mg = MO["gads"][k]
    b["cover"] = dict(
        h1=["Conversas <o>dobraram</o>.", "Com o mesmo investimento."],
        intro="Resumo da semana de <b>18 a 24/10</b> nos <b>anúncios Meta</b>, <b>Google Ads</b>, <b>Instagram</b> e <b>Perfil da Empresa no Google</b> da Trait Odontologia, comparado com a semana anterior (11 a 17/10).",
        hl_num="75", hl_lab="CONVERSAS",
        hl_h="<o>75 conversas</o> pelos anúncios, contra <o>36</o> na semana anterior.",
        hl_p="Com o mesmo investimento no Meta (R$ 801), o custo por conversa caiu de R$ 22,25 para R$ 10,69. Implantes foi a campanha campeã: 31 conversas a R$ 5,60.",
        strip=[(brl(c["cpconv"]), "custo por conversa, 52% menor que na semana anterior"),
               ("R$ 5,60", "por conversa na campanha de Implantes"),
               ("27", "ações no Perfil do Google (rotas, ligações e site), contra 12"),
               (n0(IG[k]["cur"]["pv"]), "visitas ao perfil do Instagram, 55% a mais")],
    )
    b["numbers"] = dict(
        h2="Os números, <o>semana a semana</o>",
        lead="Mesmo investimento no Meta, o <b>dobro de conversas</b>. No orgânico, o Instagram ganhou visitas ao perfil e o Perfil da Empresa no Google mais que dobrou as ações.",
        kpis=[
            dict(v="75", small="/36", t="Conversas iniciadas<br>semana atual / anterior", d=delta_txt(c["conv"], p["conv"], "up")),
            dict(v=brl(c["cpconv"]), t="Custo por conversa<br>nos anúncios Meta", d=delta_txt(c["cpconv"], p["cpconv"], "down")),
            dict(v="27", small="/12", t="Ações no Perfil<br>da Empresa no Google", d=delta_txt(gm["cur"]["actions"], gm["prev"]["actions"], "up")),
            dict(v=n0(IG[k]["cur"]["pv"]), t="Visitas ao perfil<br>no Instagram", d=delta_txt(IG[k]["cur"]["pv"], IG[k]["prev"]["pv"], "up")),
        ],
        groups=[
            ("Anúncios · Meta Ads", [r for r in meta_rows(k) if r[0] != "Impressões"]),
            ("Google Ads · Performance Max", gads_rows(k, conv=False)),
            ("Instagram · @traitodontologia", ig_rows(k)),
            ("Perfil da Empresa no Google", [
                ("Visualizações (Busca + Maps)", n0(gm["prev"]["views"]), n0(gm["cur"]["views"]), delta(gm["cur"]["views"], gm["prev"]["views"]), False),
                ("Ações: rotas, ligações e site", n0(gm["prev"]["actions"]), n0(gm["cur"]["actions"]), delta(gm["cur"]["actions"], gm["prev"]["actions"]), True)]),
        ],
        mtd=("Meta + Google · 01 a 25/10", "Google Ads ainda sem conversões registradas no mês.",
             [(brl(m["spend"] + mg["cost"], 0), "investidos (Meta + Google)"), (n0(m["conv"]), "conversas pelo Meta"),
              (brl(m["cpconv"]), "custo médio por conversa no Meta"), (n0(mg["clicks"]), "cliques no Google Ads")]),
        note=NOTE_BASE.format(fontes="Meta Ads, Google Ads, Instagram Business e Perfil da Empresa no Google") + " Alcance do Instagram = soma do alcance diário (orgânico + pago).",
    )
    gc = GA[k]["camp"]
    blocks = [
        h2lead("Onde a verba <o>trabalhou</o>",
               "<b>Implantes</b> (31 conversas a R$ 5,60) e <b>Protocolo</b> (25 a R$ 11,16) responderam por 75% das conversas. Alinhadores teve o maior custo: R$ 34,79."),
        card("Meta Ads · campanhas", f"Total {brl(c['spend'])} · {n0(c['conv'])} conversas", meta_table(FB[k]["camp"], c["spend"])),
        card("Google Ads · campanha", f"Total {brl(GA[k]['cur']['cost'])} · sem conversões registradas", gads_table(gc)),
        ig_block(k, posts_list(IG[k]["posts"], 3), "5 posts · top 3"),
        read_box("No Google Ads, a Performance Max gerou 562 cliques (−46%), mas segue <b>sem conversões registradas</b>: sem esse rastreio a campanha otimiza só por clique e não dá para comparar com o Meta. "
                 "No Perfil da Empresa no Google, foram <b>20 pedidos de rota</b>, 4 ligações, 3 cliques no site e 1 nova avaliação 5 estrelas."),
        next_steps([
            ("Reforçar Implantes e Protocolo", "Realocar parte da verba de Alinhadores (R$ 34,79 por conversa) e Institucional (R$ 20,95) para as duas campeãs."),
            ("Conversões no Google Ads", "Configurar WhatsApp, ligação e formulário como conversão para a PMax otimizar por contato, não só por clique."),
            ("Avaliações no Google", "Pedir avaliação aos pacientes atendidos: o perfil está gerando rotas e ligações, e avaliações recentes ajudam no Maps."),
        ]),
    ]
    return b, blocks


# ====================================================================== FIORINI
def fiorini():
    k = "fiorini"
    c, p = FB[k]["cur"], FB[k]["prev"]
    b = dict(brand="Fiorini Odonto & Estética", brand_upper="Fiorini Odonto & Estética", slug="Fiorini_Odonto")
    m = MO["fbads"][k]
    mg = MO["gads"][k]
    share_prot = 839.36 / c["spend"] * 100
    b["cover"] = dict(
        h1=["<o>59% mais</o> conversas.", "Com a mesma verba."],
        intro="Resumo da semana de <b>18 a 24/10</b> nos <b>anúncios Meta</b> e no <b>Google Ads</b> da Fiorini Odonto & Estética, comparado com a semana anterior (11 a 17/10).",
        hl_num="62", hl_lab="CONVERSAS",
        hl_h="<o>62 conversas</o> na semana, contra <o>39</o> na anterior, com o mesmo investimento.",
        hl_p=f"Protocolo concentrou {n0(share_prot)}% da verba e trouxe 38 conversas. Lentes teve o menor custo: R$ 13,04 por conversa.",
        strip=[(brl(c["cpconv"]), f"custo por conversa (semana anterior: {brl(p['cpconv'])})"),
               (brl(c["spend"], 0), "investidos no Meta, praticamente igual à semana anterior"),
               (mil(c["reach"]), "pessoas alcançadas pelos anúncios"),
               (n0(m["conv"]), "conversas iniciadas em outubro (01 a 25/10)")],
    )
    b["numbers"] = dict(
        h2="Os números, <o>semana a semana</o>",
        lead="Investimento estável no Meta e <b>23 conversas a mais</b>. O alcance caiu 13%, mas o custo por conversa ficou 37% menor. O Google Ads está praticamente <b>sem veiculação desde 11/10</b>.",
        kpis=[
            dict(v="62", small="/39", t="Conversas iniciadas<br>semana atual / anterior", d=delta_txt(c["conv"], p["conv"], "up")),
            dict(v=brl(c["cpconv"]), t="Custo por conversa<br>nos anúncios Meta", d=delta_txt(c["cpconv"], p["cpconv"], "down")),
            dict(v=brl(c["spend"], 0), t="Investimento<br>no Meta", d=("neu", "= estável (+0,7%)")),
            dict(v=brl(GA[k]["cur"]["cost"]), t="Investimento no Google Ads<br>na semana", d=("neg", "▼ praticamente parado desde 11/10")),
        ],
        groups=[("Anúncios · Meta Ads", meta_rows(k)),
                ("Google Ads · Performance Max", gads_rows(k, conv=False))],
        mtd=("Meta + Google · 01 a 25/10", "R$ 745 do Google Ads foram investidos de 01 a 10/10.",
             [(brl(m["spend"] + mg["cost"], 0), "investidos (Meta + Google)"), (n0(m["conv"]), "conversas pelo Meta"),
              (brl(m["cpconv"]), "custo médio por conversa no Meta"), (n0(mg["clicks"]), "cliques no Google Ads")]),
        extra=plat("fiorini", "Custo por conversa parecido entre Facebook e Instagram. “Outros” reúne Messenger e Audience Network."),
        note=NOTE_BASE.format(fontes="Meta Ads e Google Ads") + " A integração da Página do Facebook está inativa no Reportei e não entrou no relatório.",
    )
    dc = FIO["fiorini_gads_daily_cost"]
    days = [f"{d:02d}/10" for d in range(1, 26)]
    vals = [dc.get(f"{d:02d}", 0) for d in range(1, 26)]
    chart = svg_daily_single(days, vals, w=318, h=150, color="#00247d", mark=(10, 24, "≈ R$ 0 por dia"))
    blocks = [
        h2lead("Onde a verba <o>trabalhou</o>",
               f"<b>Protocolo</b> ficou com {n0(share_prot)}% da verba e trouxe 38 das 62 conversas. <b>Lentes</b> teve o melhor custo (R$ 13,04) com só R$ 104 investidos."),
        card("Meta Ads · campanhas", f"Total {brl(c['spend'])} · {n0(c['conv'])} conversas", meta_table(FB[k]["camp"], c["spend"])),
        f'''<div class="split"><div class="card"><div class="card-h"><span class="a">Investimento diário no Google Ads</span><span class="b">01 a 25/10</span></div>{chart}</div>
        <div class="card"><div class="card-h"><span class="a">Google Ads · alerta</span><span class="b">GO_PMAX_GERAL</span></div>
        <div class="post"><div class="dt" style="background:#b42318"><div class="d1">!</div><div class="d2" style="color:#fff">ALERTA</div></div>
        <div><div class="tp">Sem veiculação desde 11/10</div><div class="cap">A campanha investiu R$ 745 entre 01 e 10/10 e, desde então, gasta centavos por dia.</div>
        <div class="ms">Semana: <b>{brl(GA[k]["cur"]["cost"])}</b> · <b>{n0(GA[k]["cur"]["clicks"])}</b> cliques · <b>{n0(GA[k]["cur"]["impr"])}</b> impressões</div></div></div>
        <div class="post"><div class="dt"><div class="d1">1k</div><div class="d2">CLIQUES</div></div>
        <div><div class="tp">Outubro até agora</div><div class="cap">1.025 cliques e nenhuma conversão registrada na Performance Max.</div>
        <div class="ms">Conferir orçamento, forma de pagamento e status da campanha.</div></div></div></div></div>''',
        read_box("O Meta melhorou a eficiência com a mesma verba: o custo por conversa caiu de R$ 34,66 para <b>R$ 21,97</b>. Implantes e Invisalign seguem os mais caros (R$ 27,93 e R$ 27,88), "
                 "enquanto Lentes entrega conversa pela metade do preço. No Google Ads, a queda brusca a partir de 11/10 sugere problema de orçamento, pagamento ou status da campanha."),
        next_steps([
            ("Reativar o Google Ads", "Verificar orçamento, pagamento e status da GO_PMAX_GERAL, e configurar conversões de WhatsApp e ligação."),
            ("Testar mais verba em Lentes", "Lentes teve o menor custo por conversa (R$ 13,04). Subir o orçamento para validar com mais volume."),
            ("Criativos para Implantes e Invisalign", "Renovar os anúncios das duas campanhas mais caras (R$ 27,9 por conversa) com depoimentos e antes/depois."),
        ]),
    ]
    return b, blocks


BUILDERS = {"ego": ego, "cemed": cemed, "dreisson": dreisson, "dplacido": dplacido, "trait": trait, "fiorini": fiorini}


def build_full(key, out_dir):
    b, blocks = BUILDERS[key]()
    pages = [cover(b), page_numbers(b), page_campaigns(b, blocks)]
    name = f"Relatorio_Semanal_{b['slug']}_18-24out2026"
    path = Path(out_dir) / f"{name}.html"
    path.write_text(document(f"{b['brand']} · Relatório semanal 18 a 24/10/2026", pages), encoding="utf-8")
    return path


if __name__ == "__main__":
    out = sys.argv[1]
    keys = sys.argv[2:] or list(BUILDERS)
    for k in keys:
        if k == "sanrire":
            from sanrire import build_sanrire
            print(build_sanrire(out))
        else:
            print(build_full(k, out))
