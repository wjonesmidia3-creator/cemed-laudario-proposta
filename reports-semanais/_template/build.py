#!/usr/bin/env python3
"""Gera os reports semanais no padrão Grupo Opera (HTML -> PDF).

Uso:
    python3 build.py <pasta-da-semana> [slug ...]

A pasta da semana precisa ter:
    data/<slug>.json        dados coletados no Reportei
    narrativas/<slug>.json  textos (título, destaque, leitura, próximos passos)
Saída:
    html/<slug>.html  e  pdf/Report_Semanal_<Cliente>_<periodo>.pdf
"""
import json
import math
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).resolve().parent
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
MESES_UP = [m.upper() for m in MESES]

NAVY = "#0B2A84"
ORANGE = "#E8601C"

# --------------------------------------------------------------------------- formatação


def fmt_num(v, dec=0):
    if v is None:
        return "—"
    s = f"{v:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_brl(v, dec=2):
    if v is None:
        return "—"
    return "R$ " + fmt_num(v, dec)


def fmt_pct(v, dec=1):
    if v is None:
        return "—"
    return fmt_num(v * 100, dec) + "%"


def fmt_compact(v):
    """90.626 -> '90,6 mil'."""
    if v is None:
        return "—"
    if abs(v) >= 10000:
        return fmt_num(v / 1000, 1) + " mil"
    return fmt_num(v)


def d(s):
    return date.fromisoformat(s)


def ddmm(s):
    x = d(s)
    return f"{x.day:02d}/{x.month:02d}"


def period_label(p):
    a, b = d(p[0]), d(p[1])
    if a.month == b.month:
        return f"{a.day:02d} a {b.day:02d}/{b.month:02d}"
    return f"{a.day:02d}/{a.month:02d} a {b.day:02d}/{b.month:02d}"


def markup(s):
    """**negrito** e *destaque laranja*."""
    if not s:
        return ""
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r'<span class="accent">\1</span>', s)
    return s


def ratio(a, b):
    if not b:
        return None
    return a / b


def change(cur, prev):
    if cur is None or prev in (None, 0):
        return None
    return (cur - prev) / prev


# --------------------------------------------------------------------------- métricas


class Metric:
    def __init__(self, label, cur, prev, fmt="num", good="up", group=None):
        self.label, self.cur, self.prev, self.fmt, self.good, self.group = label, cur, prev, fmt, good, group

    def f(self, v):
        if v is None:
            return "—"
        return {
            "num": lambda x: fmt_num(x),
            "brl": lambda x: fmt_brl(x),
            "brl0": lambda x: fmt_brl(x, 0),
            "pct": lambda x: fmt_pct(x),
            "dec": lambda x: fmt_num(x, 1),
        }[self.fmt](v)

    @property
    def cur_s(self):
        return self.f(self.cur)

    @property
    def prev_s(self):
        return self.f(self.prev)

    @property
    def delta(self):
        return change(self.cur, self.prev)

    @property
    def tone(self):
        dl = self.delta
        if dl is None or abs(dl) < 0.005 or self.good == "neutral":
            return "neutral"
        better = dl > 0 if self.good == "up" else dl < 0
        return "good" if better else "bad"

    @property
    def delta_s(self):
        dl = self.delta
        if dl is None:
            return ""
        arrow = "▲" if dl > 0 else ("▼" if dl < 0 else "=")
        if abs(dl) < 0.005:
            return "= estável"
        return f"{arrow} {fmt_num(abs(dl) * 100, 1 if abs(dl) < 0.1 else 0)}%"


def sum_accounts(accounts, key, which):
    vals = [a[which].get(key) for a in accounts]
    vals = [v for v in vals if v is not None]
    return sum(vals) if vals else None


MIN_SPEND = 20  # contas com menos que isso nas duas semanas somadas ficam fora da tabela


def active_meta(data):
    return [a for a in data.get("meta_ads", []) if (a["cur"].get("spend") or 0) + (a["prev"].get("spend") or 0) >= MIN_SPEND]


def build_metrics(data):
    """Monta o dicionário de métricas (chave -> Metric) e os grupos da tabela."""
    M = {}
    groups = []

    # ---------------- Meta Ads
    meta = [a for a in data.get("meta_ads", [])]
    meta_active = active_meta(data)
    if meta_active:
        g = []
        multi = len(meta_active) > 1
        S = lambda k, w: sum_accounts(meta_active, k, w)
        spend_c, spend_p = S("spend", "cur"), S("spend", "prev")
        conv_c, conv_p = S("conversations", "cur"), S("conversations", "prev")
        lead_c, lead_p = S("leads", "cur"), S("leads", "prev")
        clk_c, clk_p = S("link_clicks", "cur"), S("link_clicks", "prev")
        imp_c, imp_p = S("impressions", "cur"), S("impressions", "prev")
        M["meta.spend"] = Metric("Investimento", spend_c, spend_p, "brl", "neutral")
        g.append("meta.spend")
        if (conv_c or 0) + (conv_p or 0) > 0:
            M["meta.conversations"] = Metric("Conversas iniciadas", conv_c, conv_p, "num", "up")
            M["meta.cpconv"] = Metric("Custo por conversa", ratio(spend_c, conv_c), ratio(spend_p, conv_p), "brl", "down")
            g += ["meta.conversations", "meta.cpconv"]
        M["meta.leads_raw"] = Metric("Leads (cadastros)", lead_c, lead_p, "num", "up")
        leads_t, conv_t = (lead_c or 0) + (lead_p or 0), (conv_c or 0) + (conv_p or 0)
        if leads_t > 0 and (conv_t == 0 or leads_t >= 0.2 * conv_t):
            M["meta.leads"] = Metric("Leads (cadastros)", lead_c, lead_p, "num", "up")
            M["meta.cpl"] = Metric("Custo por lead", ratio(spend_c, lead_c), ratio(spend_p, lead_p), "brl", "down")
            if conv_t > 0:
                res_c, res_p = (conv_c or 0) + (lead_c or 0), (conv_p or 0) + (lead_p or 0)
                M["meta.results"] = Metric("Resultados (conversas + leads)", res_c, res_p, "num", "up")
                M["meta.cpr"] = Metric("Custo por resultado", ratio(spend_c, res_c), ratio(spend_p, res_p), "brl", "down")
                g = [k for k in g if k != "meta.cpconv"] + ["meta.leads", "meta.cpr"]
            else:
                g += ["meta.leads", "meta.cpl"]
        M["meta.link_clicks"] = Metric("Cliques no link", clk_c, clk_p, "num", "up")
        M["meta.cpc"] = Metric("Custo por clique", ratio(spend_c, clk_c), ratio(spend_p, clk_p), "brl", "down")
        g += ["meta.link_clicks", "meta.cpc"]
        if not multi:
            M["meta.reach"] = Metric("Alcance", S("reach", "cur"), S("reach", "prev"), "num", "up")
            g.append("meta.reach")
        M["meta.impressions"] = Metric("Impressões", imp_c, imp_p, "num", "up")
        g.append("meta.impressions")
        title = "Anúncios · Meta Ads" + (f" ({len(meta_active)} contas)" if multi else "")
        groups.append((title, g))

    # ---------------- Google Ads
    gads = [a for a in data.get("google_ads", []) if (a["cur"].get("cost") or 0) + (a["prev"].get("cost") or 0) + (a["cur"].get("impressions") or 0) > 0]
    if gads:
        S = lambda k, w: sum_accounts(gads, k, w)
        cost_c, cost_p = S("cost", "cur"), S("cost", "prev")
        clk_c, clk_p = S("clicks", "cur"), S("clicks", "prev")
        M["google.cost"] = Metric("Investimento", cost_c, cost_p, "brl", "neutral")
        M["google.clicks"] = Metric("Cliques", clk_c, clk_p, "num", "up")
        M["google.cpc"] = Metric("Custo por clique", ratio(cost_c, clk_c), ratio(cost_p, clk_p), "brl", "down")
        M["google.impressions"] = Metric("Impressões", S("impressions", "cur"), S("impressions", "prev"), "num", "up")
        g = ["google.cost", "google.clicks", "google.cpc"]
        conv_c, conv_p = S("conversions", "cur"), S("conversions", "prev")
        if (conv_c or 0) + (conv_p or 0) > 0:
            M["google.conversions"] = Metric("Conversões", conv_c, conv_p, "dec" if (conv_c or 0) % 1 or (conv_p or 0) % 1 else "num", "up")
            M["google.cpa"] = Metric("Custo por conversão", ratio(cost_c, conv_c), ratio(cost_p, conv_p), "brl", "down")
            g += ["google.conversions", "google.cpa"]
        groups.append(("Google Ads" + (f" ({len(gads)} contas)" if len(gads) > 1 else ""), g))

    # ---------------- Instagram
    for i, ig in enumerate(data.get("instagram", [])):
        p = f"ig{i or ''}"
        g = []
        if ig.get("cur", {}).get("reach") is not None:
            M[f"{p}.reach"] = Metric("Alcance", ig["cur"].get("reach"), ig["prev"].get("reach"), "num", "up")
            M[f"{p}.views"] = Metric("Visualizações", ig["cur"].get("views"), ig["prev"].get("views"), "num", "up")
            g += [f"{p}.reach", f"{p}.views"]
        content = (ig.get("reels") or []) + (ig.get("posts") or [])
        M[f"{p}.published"] = Metric("Publicações no feed/Reels", len(content), None, "num", "up")
        if ig.get("followers_current") is not None:
            M[f"{p}.followers"] = Metric("Seguidores (total)", ig.get("followers_current"), None, "num", "up")
        if ig.get("followers_delta") is not None:
            M[f"{p}.followers_delta"] = Metric("Novos seguidores (saldo)", ig.get("followers_delta"), None, "num", "up")
        if g:
            name = "Instagram" + (f" · @{ig['account_name']}" if len(data.get("instagram", [])) > 1 else "")
            groups.append((name, g))

    # ---------------- Facebook (página)
    pages = [fb for fb in data.get("facebook_page", []) if fb.get("cur", {}).get("page_reach") is not None
             and any((fb[w].get(k) or 0) for w in ("cur", "prev") for k in ("page_reach", "media_views", "posts"))]
    for i, fb in enumerate(pages):
        p = f"fb{i or ''}"
        M[f"{p}.page_reach"] = Metric("Alcance da página", fb["cur"].get("page_reach"), fb["prev"].get("page_reach"), "num", "up")
        M[f"{p}.media_views"] = Metric("Visualizações", fb["cur"].get("media_views"), fb["prev"].get("media_views"), "num", "up")
        M[f"{p}.posts"] = Metric("Publicações", fb["cur"].get("posts"), fb["prev"].get("posts"), "num", "up")
        name = "Facebook" + (f" · {fb['account_name']}" if len(pages) > 1 else "")
        groups.append((name, [f"{p}.page_reach", f"{p}.media_views", f"{p}.posts"]))

    # ---------------- Outras plataformas
    names = {"google_my_business": "Perfil da empresa no Google", "youtube": "YouTube", "chatgpt_ads": "Anúncios no ChatGPT"}
    for i, o in enumerate(data.get("other", [])):
        g = []
        for j, m in enumerate(o.get("metrics", [])):
            if not (m.get("cur") or 0) and not (m.get("prev") or 0):
                continue
            k = f"other{i}.{j}"
            lab = m.get("label_pt", "")
            is_cost = any(w in lab.lower() for w in ("custo", "cpc", "cpm"))
            is_money = is_cost or "invest" in lab.lower() or "gasto" in lab.lower()
            M[k] = Metric(lab, m.get("cur"), m.get("prev"), "brl" if is_money else "num", "down" if is_cost else ("neutral" if is_money else "up"))
            g.append(k)
        if g:
            groups.append((names.get(o.get("platform"), o.get("platform", "")), g))

    return M, groups


# --------------------------------------------------------------------------- gráfico


def nice_max(v):
    if v <= 0:
        return 1
    exp = 10 ** math.floor(math.log10(v))
    for m in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if m * exp >= v:
            return m * exp
    return 10 * exp


def nice_step(x, integer=False):
    if x <= 0:
        return 1
    exp = 10 ** math.floor(math.log10(x))
    for m in (1, 2, 2.5, 5, 10):
        st = m * exp
        if integer and st != int(st):
            continue
        if st >= x:
            return st
    return 10 * exp


def build_chart(data, chart_spec):
    """Barras diárias (14 dias): semana anterior em azul, semana atual em laranja."""
    spec = chart_spec or {}
    days = {}
    if spec.get("source") == "google":
        idx = {"clicks": 1, "conversions": 2}
        for a in data.get("google_ads", []):
            for row in a.get("daily") or []:
                days.setdefault(row[0], [0, 0])
                for k in range(2):
                    days[row[0]][k] += float(row[k + 1] or 0)
        order = ("conversions", "clicks")
    else:
        idx = {"spend": 1, "conversations": 2, "leads": 3, "link_clicks": 4}
        for a in [a for a in active_meta(data) if a.get("daily")]:
            for row in a["daily"]:
                days.setdefault(row[0], [0, 0, 0, 0])
                for k in range(4):
                    days[row[0]][k] += float(row[k + 1] or 0)
        order = ("conversations", "leads", "link_clicks", "spend")
    if not days:
        return None
    labels = sorted(days)
    metric = spec.get("metric")
    if not metric:
        tot = lambda k: sum(days[x][idx[k] - 1] for x in labels)
        metric = next((m for m in order if tot(m) > 0), None)
        if metric is None:
            return None
    vals = [days[x][idx[metric] - 1] for x in labels]
    cur0 = data["period"]["cur"][0]
    is_cur = [x >= cur0 for x in labels]

    W, H = 640, 180
    left, bottom, top = 34, 24, 26
    plot_w, plot_h = W - left - 6, H - bottom - top
    raw = max(vals) if max(vals) > 0 else 1
    step = nice_step(raw / 4, integer=(metric != "spend"))
    ticks = max(1, math.ceil(raw / step))
    vmax = step * ticks
    n = len(vals)
    slot = plot_w / n
    bw = slot * 0.56
    parts = []
    for t in range(ticks + 1):
        v = vmax * t / ticks
        y = top + plot_h - plot_h * t / ticks
        lab = fmt_brl(v, 0).replace("R$ ", "R$") if metric == "spend" else (fmt_num(v / 1000, 1) + "k" if vmax >= 2000 else fmt_num(v))
        parts.append(f'<line x1="{left}" x2="{W - 4}" y1="{y:.1f}" y2="{y:.1f}" stroke="#EDF0F5" stroke-width="1"/>')
        parts.append(f'<text x="{left - 8}" y="{y + 3.5:.1f}" text-anchor="end" class="ax">{lab}</text>')
    peak_i = max((i for i in range(n) if is_cur[i]), key=lambda i: vals[i], default=None)
    for i, v in enumerate(vals):
        x = left + slot * i + (slot - bw) / 2
        h = plot_h * v / vmax
        y = top + plot_h - h
        color = ORANGE if is_cur[i] else NAVY
        if h < 1.5 and v > 0:
            h, y = 1.5, top + plot_h - 1.5
        if v == 0:
            parts.append(f'<rect x="{x:.1f}" y="{top + plot_h - 1.2:.1f}" width="{bw:.1f}" height="1.2" fill="#C9D1E3"/>')
        else:
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{x + bw / 2:.1f}" y="{H - 6}" text-anchor="middle" class="ax">{ddmm(labels[i])}</text>')
    # divisor entre semanas
    xdiv = left + slot * is_cur.index(True) - 1 if True in is_cur else None
    if xdiv:
        parts.append(f'<line x1="{xdiv:.1f}" x2="{xdiv:.1f}" y1="{top - 6}" y2="{top + plot_h}" stroke="#C9D1E3" stroke-width="1" stroke-dasharray="3 3"/>')
    peak = None
    if peak_i is not None and vals[peak_i] > 0:
        x = left + slot * peak_i + slot / 2
        y = top + plot_h - plot_h * vals[peak_i] / vmax
        pv = fmt_brl(vals[peak_i], 0) if metric == "spend" else fmt_num(round(vals[peak_i]))
        txt = f"pico {pv} em {ddmm(labels[peak_i])}"
        anchor = "end" if x > W * 0.75 else "middle"
        parts.append(f'<text x="{x:.1f}" y="{max(y - 8, 11):.1f}" text-anchor="{anchor}" class="peak">{txt}</text>')
        peak = (labels[peak_i], vals[peak_i])
    svg = f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'
    titles = {
        "conversations": ("Conversas iniciadas por dia", "Conversas no WhatsApp, Direct ou Messenger vindas dos anúncios"),
        "leads": ("Leads por dia", "Cadastros gerados pelos anúncios da Meta"),
        "link_clicks": ("Cliques no link por dia", "Cliques dos anúncios da Meta que levaram ao destino"),
        "spend": ("Investimento por dia", "Valor investido nos anúncios da Meta"),
        "conversions": ("Conversões no Google Ads por dia", "Conversões registradas pelo Google Ads"),
        "clicks": ("Cliques no Google Ads por dia", "Cliques nos anúncios do Google"),
    }
    t, sub = titles[metric]
    p, c = data["period"]["prev"], data["period"]["cur"]
    return {
        "svg": svg,
        "metric": metric,
        "title": (chart_spec or {}).get("title") or t,
        "subtitle": (chart_spec or {}).get("subtitle") or f"{sub}, de {ddmm(p[0])} a {ddmm(c[1])}",
        "peak": peak,
    }


# --------------------------------------------------------------------------- conteúdo


def build_content(data, n=8):
    items = []
    for ig in data.get("instagram", []):
        for kind, lst in (("REELS", ig.get("reels") or []), ("POST", ig.get("posts") or [])):
            for it in lst:
                items.append(dict(it, kind=kind))
    if not items:
        return None
    total = {
        "count": len(items),
        "views": sum(i.get("views") or 0 for i in items),
        "reach": sum(i.get("reach") or 0 for i in items),
        "interactions": sum(i.get("interactions") or 0 for i in items),
        "n_reels": sum(1 for i in items if i["kind"] == "REELS"),
    }
    total["views_s"] = fmt_compact(total["views"])
    total["reach_s"] = fmt_compact(total["reach"])
    best_reach = max(items, key=lambda i: i.get("reach") or 0)
    best_eng = max(items, key=lambda i: (i.get("interactions") or 0, i.get("eng_rate") or 0))
    for it in items:
        tags = []
        if it is best_reach and (it.get("reach") or 0) > 0:
            tags.append("MAIS ALCANCE")
        if it is best_eng and it is not best_reach and (it.get("interactions") or 0) > 0:
            tags.append("MAIS ENGAJAMENTO")
        it["tag"] = tags[0] if tags else it["kind"]
        x = d(it["date"])
        it["day"] = f"{x.day:02d}"
        it["mon"] = MESES_UP[x.month - 1]
        it["eng_s"] = fmt_pct(it.get("eng_rate")) if it.get("eng_rate") is not None else None
        it["reach_s"] = fmt_compact(it.get("reach") or 0)
        it["views_s"] = fmt_compact(it.get("views") or 0)
    items.sort(key=lambda i: i["date"], reverse=True)
    return {"cards": items[:n], "total": total, "hidden": max(0, len(items) - n)}


def build_campaigns(data, n=8):
    rows = []
    for a in active_meta(data):
        for r in a.get("campaigns") or []:
            name, spend, conv, leads, clicks, imp = (r + [0] * 6)[:6]
            if not spend:
                continue
            rows.append({
                "name": name, "spend": spend, "conv": conv or 0, "leads": leads or 0, "clicks": clicks or 0, "imp": imp or 0,
            })
    if not rows:
        return None
    rows.sort(key=lambda r: r["spend"], reverse=True)
    show_conv = any(r["conv"] for r in rows)
    tot_leads = sum(r["leads"] for r in rows)
    tot_conv = sum(r["conv"] for r in rows)
    show_leads = tot_leads > 0 and (tot_conv == 0 or tot_leads >= 0.2 * tot_conv)
    for r in rows:
        r["display"] = re.sub(r"\s+", " ", r["name"].replace("_", " ")).strip()
        r["spend_s"] = fmt_brl(r["spend"])
        r["conv_s"] = fmt_num(r["conv"])
        r["cpconv_s"] = fmt_brl(r["spend"] / r["conv"]) if r["conv"] else "—"
        r["leads_s"] = fmt_num(r["leads"])
        r["cpl_s"] = fmt_brl(r["spend"] / r["leads"]) if r["leads"] else "—"
        res = r["conv"] + r["leads"]
        r["cpr_s"] = fmt_brl(r["spend"] / res) if res else "—"
        r["clicks_s"] = fmt_num(r["clicks"])
        r["cpc_s"] = fmt_brl(r["spend"] / r["clicks"]) if r["clicks"] else "—"
    hidden = rows[n:]
    return {
        "rows": rows[:n],
        "hidden": len(hidden),
        "hidden_spend": fmt_brl(sum(r["spend"] for r in hidden)) if hidden else None,
        "show_conv": show_conv,
        "show_leads": show_leads,
    }


# --------------------------------------------------------------------------- KPIs


def kpi_from_spec(spec, M):
    if "key" in spec:
        m = M.get(spec["key"])
        if m is None:
            raise KeyError(f"métrica {spec['key']} não existe para este cliente (disponíveis: {sorted(M)})")
        value = spec.get("value") or m.cur_s
        delta = spec.get("delta")
        tone = spec.get("tone")
        if delta is None:
            if m.delta is not None:
                delta = f"{m.delta_s} vs. semana anterior" if m.delta_s != "= estável" else "estável vs. semana anterior"
                tone = tone or m.tone
            else:
                delta = ""
        return {"value": value, "suffix": spec.get("suffix", ""), "label": spec.get("label") or m.label, "delta": delta, "tone": tone or "neutral"}
    return {"value": spec["value"], "suffix": spec.get("suffix", ""), "label": spec["label"], "delta": spec.get("delta", ""), "tone": spec.get("tone", "neutral")}


def split_value(v):
    """'R$ 37,81' -> ('R$', '37,81'); '7 vídeos' -> ('7', 'vídeos')."""
    if v.startswith("R$"):
        return "R$", v[2:].strip(), "pre"
    m = re.match(r"^([\d.,+\-–]+)\s+(.+)$", v)
    if m:
        return m.group(1), m.group(2), "post"
    return v, "", "none"


# --------------------------------------------------------------------------- paginação

PAGE_CONTENT_H = 958  # px úteis entre o cabeçalho e o rodapé (medido no A4 a 96 dpi)


def paginate(blocks):
    """Empacota os blocos nas páginas. Blocos 'float' (gráfico) podem subir para
    preencher um espaço que sobraria vazio; cabeçalho de seção nunca fica sozinho."""
    queue = list(blocks)
    pages, cur, h = [], [], 0
    while queue:
        b = queue[0]
        if cur and h + b["h"] > PAGE_CONTENT_H:
            # tenta encaixar um bloco flutuante que caiba no espaço restante
            fl = next((x for x in queue[1:] if x.get("float") and h + x["h"] <= PAGE_CONTENT_H), None)
            if fl is not None and cur[-1]["type"] != "section":
                queue.remove(fl)
                cur.append(fl)
                h += fl["h"]
                continue
            if cur[-1]["type"] == "section":
                moved = cur.pop()
                pages.append(cur)
                cur, h = [moved], moved["h"]
            else:
                pages.append(cur)
                cur, h = [], 0
        queue.pop(0)
        cur.append(b)
        h += b["h"]
    if cur:
        pages.append(cur)
    return [p for p in pages if p]


def comparison_height(groups):
    rows = sum(len(g) for _, g in groups)
    return 70 + len(groups) * 34 + rows * 33


# --------------------------------------------------------------------------- build


def build_client(week_dir: Path, slug: str, env):
    data = json.loads((week_dir / "data" / f"{slug}.json").read_text())
    nar = json.loads((week_dir / "narrativas" / f"{slug}.json").read_text())
    M, groups = build_metrics(data)
    chart = build_chart(data, nar.get("chart"))
    content = build_content(data)
    campaigns = build_campaigns(data)

    pc, pp = data["period"]["cur"], data["period"]["prev"]
    ctx = {
        "client": data["client"],
        "client_short": nar.get("client_short", data["client"]),
        "period_cur": period_label(pc),
        "period_prev": period_label(pp),
        "week_label": f"Semana de {period_label(pc)}/{d(pc[1]).year}",
        "nar": nar,
        "markup": markup,
    }

    # capa
    strip = []
    for s in nar["strip"]:
        if "key" in s:
            m = M[s["key"]]
            val = s.get("value") or m.cur_s
        else:
            val = s["value"]
        a, b, mode = split_value(val)
        strip.append({"a": a, "b": b, "mode": mode, "desc": markup(s["desc"])})
    ctx["strip"] = strip

    kpis = [kpi_from_spec(k, M) for k in nar["kpis"]]

    # tabela comparativa
    key_rows = set(nar.get("key_rows", []))
    table = []
    for title, keys in groups:
        table.append({"title": title, "rows": [{"m": M[k], "key": k in key_rows} for k in keys]})
    ctx["table"] = table

    # blocos para paginação
    blocks = []
    blocks.append({"type": "section", "h": 132, "num": "01", "eyebrow": "SEMANA × SEMANA",
                   "title": nar.get("s1_title", "Os números, *semana a semana*"), "intro": nar.get("s1_intro", "")})
    blocks.append({"type": "kpis", "h": 150, "kpis": kpis})
    cmp_block = {"type": "comparison", "h": comparison_height(groups)}
    blocks.append(cmp_block)
    if chart:
        blocks.append({"type": "chart", "h": 290, "chart": chart, "float": True, "note": nar.get("footnote1")})
    elif nar.get("footnote1"):
        cmp_block["note"] = nar["footnote1"]

    s2_has = campaigns or content
    blocks.append({"type": "section", "h": 132, "num": "02", "eyebrow": nar.get("s2_eyebrow", "CAMPANHAS E CONTEÚDO"),
                   "title": nar.get("s2_title", "O que *puxou* a semana"), "intro": nar.get("s2_intro", "")})
    if campaigns:
        blocks.append({"type": "campaigns", "h": 96 + 38 * len(campaigns["rows"]) + (26 if campaigns["hidden"] else 0), "c": campaigns})
    if content:
        n_cards = len(content["cards"]) + 1
        blocks.append({"type": "content", "h": 30 + math.ceil(n_cards / 2) * 124, "c": content})
    if not s2_has:
        pass
    blocks.append({"type": "leitura", "h": 40 + 22 * math.ceil(len(nar["leitura"]) / 105), "text": nar["leitura"]})
    blocks.append({"type": "proximos", "h": 168, "list": nar["proximos"]})
    if nar.get("footnote2"):
        blocks.append({"type": "footnote", "h": 44, "text": nar["footnote2"]})

    for i, b in enumerate(blocks):
        b["i"] = i
    out_html = week_dir / "html" / f"{slug}.html"
    out_html.parent.mkdir(parents=True, exist_ok=True)
    tpl = env.get_template("report.html.j2")

    # 1ª passada: mede a altura real de cada bloco no navegador
    out_html.write_text(tpl.render(**ctx, pages=[blocks], measure=True))
    res = subprocess.run(["node", str(TEMPLATE_DIR / "measure.js"), str(out_html)], check=True, capture_output=True, text=True)
    heights = json.loads(res.stdout)
    for b in blocks:
        b["h"] = heights[str(b["i"])]

    # 2ª passada: pagina com as alturas medidas
    ctx["pages"] = paginate(blocks)
    out_html.write_text(tpl.render(**ctx, measure=False))
    return data, out_html


def main():
    week_dir = Path(sys.argv[1]).resolve()
    slugs = sys.argv[2:] or sorted(p.stem for p in (week_dir / "narrativas").glob("*.json"))
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=False)
    env.filters["markup"] = markup
    jobs = []
    for slug in slugs:
        data, html = build_client(week_dir, slug, env)
        pc = data["period"]["cur"]
        a, b = d(pc[0]), d(pc[1])
        nar = json.loads((week_dir / "narrativas" / f"{slug}.json").read_text())
        import unicodedata
        base = unicodedata.normalize("NFKD", nar.get("client_short", data["client"])).encode("ascii", "ignore").decode()
        name = re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_")
        pdf = week_dir / "pdf" / f"Report_Semanal_{name}_{a.day:02d}-{b.day:02d}{MESES[b.month - 1]}{b.year}.pdf"
        pdf.parent.mkdir(parents=True, exist_ok=True)
        jobs.append({"html": str(html), "pdf": str(pdf)})
        print("html:", html)
    subprocess.run(["node", str(TEMPLATE_DIR / "render_pdf.js"), json.dumps(jobs)], check=True)


if __name__ == "__main__":
    main()
