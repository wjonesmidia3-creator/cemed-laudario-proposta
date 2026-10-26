"""Componentes visuais do modelo Grupo Opera (relatório semanal)."""
import html as _html
import re

# ---------------------------------------------------------------- formatação

def _milhar(s):
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def n0(x):
    return _milhar(f"{x:,.0f}")


def n1(x):
    return _milhar(f"{x:,.1f}")


def _round(x, dec):
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-dec), rounding=ROUND_HALF_UP))


def brl(x, dec=2):
    return "R$\u00a0" + _milhar(f"{_round(x, dec):,.{dec}f}")


def pct(x, dec=1):
    return _milhar(f"{x:,.{dec}f}") + "%"


def mil(x):
    """21758 -> '21,8 mil'"""
    if x >= 1000:
        return n1(x / 1000) + " mil"
    return n0(x)


def esc(s):
    return _html.escape(s, quote=False)


def rich(s):
    """Marcação leve: <o>texto</o> vira destaque laranja; <b> e <br> passam."""
    s = s.replace("<o>", '<span class="o">').replace("</o>", "</span>")
    s = s.replace("<l>", '<span class="l">').replace("</l>", "</span>")
    return re.sub(r"R\$ (?=\d)", "R$\u00a0", s)


def delta(cur, prev, good="up", fmt="pct"):
    """Pílula de variação. good: 'up' (subir é bom), 'down' (cair é bom), 'neutral'."""
    if prev in (None, 0):
        if cur in (None, 0):
            return ""
        return '<span class="pill neu">novo</span>'
    ch = (cur - prev) / prev * 100
    if abs(ch) < 0.5:
        return '<span class="pill neu">= estável</span>'
    up = ch > 0
    arrow = "▲" if up else "▼"
    if good == "neutral":
        cls = "neu"
    else:
        cls = "pos" if (up == (good == "up")) else "neg"
    txt = f"{arrow} {n0(abs(ch))}%" if abs(ch) >= 10 else f"{arrow} {n1(abs(ch))}%"
    return f'<span class="pill {cls}">{txt}</span>'


def delta_txt(cur, prev, good="up", suffix=" vs. semana anterior"):
    if prev in (None, 0):
        return ("pos", "novo na semana")
    ch = (cur - prev) / prev * 100
    up = ch > 0
    arrow = "▲" if up else "▼"
    cls = "neu" if good == "neutral" else ("pos" if (up == (good == "up")) else "neg")
    val = n0(abs(ch)) if abs(ch) >= 10 else n1(abs(ch))
    return (cls, f"{arrow} {val}%{suffix}")


# ---------------------------------------------------------------- CSS

CSS = r"""
@page { size: A4; margin: 0; }
:root{
  --navy:#00247d; --navy2:#0b2d82; --orange:#e85d1b; --orange-l:#f6a24e; --sky:#a9c3e6;
  --ink:#00247d; --body:#47547a; --muted:#7b86a3; --line:#e2e8f2; --panel:#eef3fb;
  --green:#1e7e34; --green-bg:#e8f1ea; --red:#b42318; --red-bg:#fbeae8; --neu-bg:#eef1f6;
}
*{ box-sizing:border-box; margin:0; padding:0; }
html,body{ background:#fff; }
body{ font-family:'Inter',system-ui,sans-serif; color:var(--body); -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.page{ width:794px; height:1123px; position:relative; overflow:hidden; page-break-after:always; break-after:page; background:#fff; }
.page:last-child{ page-break-after:auto; break-after:auto; }
.o{ color:var(--orange); }
.l{ color:var(--sky); }
b{ font-weight:700; color:var(--ink); }

/* ---------- capa ---------- */
.cover{ background:var(--navy); color:#fff; }
.cover::before{ content:""; position:absolute; right:-160px; top:-170px; width:620px; height:620px; border-radius:50%;
  background:radial-gradient(circle, rgba(120,150,220,.30) 0%, rgba(60,90,170,.12) 40%, rgba(0,36,125,0) 70%); }
.cover .logo{ position:absolute; left:47px; top:52px; }
.logo{ font-family:'Poppins',sans-serif; font-weight:800; font-size:23px; letter-spacing:-.5px; color:#fff; }
.logo .dot{ color:var(--orange); }
.cover .head{ position:absolute; left:47px; top:205px; width:700px; }
.cover .eyebrow{ display:flex; align-items:center; gap:12px;
  font-family:'Sora',sans-serif; font-weight:600; font-size:10px; letter-spacing:.32em; color:var(--orange-l); text-transform:uppercase; }
.cover .eyebrow::before{ content:""; width:26px; height:3px; background:var(--orange-l); border-radius:2px; }
.cover h1{ margin-top:18px; font-family:'Poppins',sans-serif; font-weight:800;
  font-size:47px; line-height:1.04; letter-spacing:-1.6px; color:#fff; }
.cover h1 .o{ color:var(--orange-l); }
.cover h1 .l2{ display:block; color:var(--sky); }
.cover .intro{ margin-top:24px; width:520px; font-size:14px; line-height:1.55; color:#d5def0; }
.cover .intro b{ color:#fff; }
.cover .chips{ margin-top:22px; display:flex; gap:10px; }
.chip{ font-family:'Inter'; font-weight:700; font-size:11px; padding:9px 15px; border-radius:99px; border:1px solid rgba(169,195,230,.35); color:#fff; }
.chip.on{ background:var(--orange); border-color:var(--orange); }
.cover .hl{ position:absolute; left:47px; right:47px; bottom:133px; border:1px solid rgba(169,195,230,.22); border-radius:16px;
  background:linear-gradient(135deg, rgba(255,255,255,.07), rgba(255,255,255,.02)); display:flex; gap:26px; align-items:center; padding:26px 30px; }
.hl .big{ text-align:center; min-width:118px; }
.hl .big .num{ font-family:'Poppins'; font-weight:800; font-size:58px; line-height:1; letter-spacing:-2px; color:#fff; }
.hl .big .lab{ margin-top:8px; font-family:'Sora'; font-weight:600; font-size:9px; letter-spacing:.3em; color:var(--orange-l); }
.hl .txt .kick{ font-family:'Sora'; font-weight:600; font-size:9px; letter-spacing:.3em; color:var(--orange-l); margin-bottom:6px; }
.hl .txt h3{ font-family:'Poppins'; font-weight:800; font-size:19px; line-height:1.22; letter-spacing:-.4px; color:#fff; }
.hl .txt h3 .o{ color:var(--orange-l); }
.hl .txt p{ margin-top:7px; font-size:11.5px; line-height:1.5; color:#c9d5ee; }
.cover .strip{ position:absolute; left:0; right:0; bottom:0; height:104px; border-top:1px solid rgba(169,195,230,.18); display:grid; grid-template-columns:repeat(4,1fr); }
.strip .cell{ padding:19px 18px 0 22px; border-right:1px solid rgba(169,195,230,.16); }
.strip .cell:last-child{ border-right:0; }
.strip .v{ font-family:'Poppins'; font-weight:800; font-size:23px; letter-spacing:-.6px; color:#fff; white-space:nowrap; }
.strip .v .o{ color:var(--orange-l); }
.strip .t{ margin-top:5px; font-size:10px; line-height:1.4; color:#c9d5ee; }

/* ---------- páginas internas ---------- */
.topbar{ height:62px; background:var(--navy); display:flex; justify-content:space-between; align-items:center; padding:0 40px 0 40px; position:relative; overflow:hidden; }
.topbar::after{ content:""; position:absolute; right:-80px; top:-120px; width:300px; height:300px; border-radius:50%; background:radial-gradient(circle, rgba(120,150,220,.28), rgba(0,36,125,0) 65%); }
.topbar .logo{ font-size:18px; }
.topbar .brand{ font-family:'Sora'; font-weight:600; font-size:7.5px; letter-spacing:.36em; color:#c9d5ee; margin-top:3px; text-transform:uppercase; }
.topbar .rt{ text-align:right; position:relative; z-index:1; }
.topbar .rt .a{ font-family:'Poppins'; font-weight:800; font-size:12.5px; color:#fff; }
.topbar .rt .b{ font-size:10.5px; color:var(--sky); letter-spacing:.02em; margin-top:1px; }
.content{ padding:26px 40px 0 40px; }
.sec{ font-family:'Sora'; font-weight:600; font-size:9.5px; letter-spacing:.3em; text-transform:uppercase; color:var(--orange); display:flex; gap:12px; }
.sec .n{ color:var(--muted); letter-spacing:.12em; }
h2{ font-family:'Poppins'; font-weight:800; font-size:27px; line-height:1.1; letter-spacing:-.8px; color:var(--ink); margin-top:8px; }
.lead{ font-size:12.5px; line-height:1.55; color:var(--body); margin-top:8px; max-width:640px; }
.lead b{ color:#1b2550; }

.kpis{ display:grid; grid-template-columns:repeat(4,1fr); gap:11px; margin-top:16px; }
.kpi{ border:1px solid var(--line); border-radius:13px; padding:15px 14px 13px 15px; position:relative; }
.kpi::before{ content:""; position:absolute; left:15px; top:-1px; width:26px; height:4px; border-radius:0 0 3px 3px; background:var(--orange); }
.kpi .v{ font-family:'Poppins'; font-weight:800; font-size:23px; letter-spacing:-.6px; color:var(--ink); line-height:1.1; white-space:nowrap; }
.kpi .v small{ font-size:12px; color:var(--orange); letter-spacing:0; margin-left:2px; }
.kpi .t{ font-size:10.5px; line-height:1.4; margin-top:6px; color:var(--body); }
.kpi .d{ font-size:10px; font-weight:700; margin-top:6px; }
.d.pos,.pos-t{ color:var(--green); } .d.neg{ color:var(--red); } .d.neu{ color:var(--muted); }

.cols{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:16px; }
.col{ border:1px solid var(--line); border-radius:13px; overflow:hidden; }
.col .hd{ display:flex; justify-content:space-between; align-items:center; padding:12px 18px; background:var(--panel); }
.col .hd .a{ font-family:'Poppins'; font-weight:800; font-size:15px; color:var(--ink); }
.col .hd .b{ font-family:'Sora'; font-weight:600; font-size:8.5px; letter-spacing:.14em; color:var(--muted); text-transform:uppercase; }
.col.cur .hd{ background:var(--orange); }
.col.cur .hd .a, .col.cur .hd .b{ color:#fff; }
.col .bd{ padding:4px 18px 10px 18px; }
.grp{ font-family:'Sora'; font-weight:600; font-size:8px; letter-spacing:.24em; color:var(--orange); text-transform:uppercase; margin:10px 0 2px; }
.row{ display:flex; justify-content:space-between; align-items:center; padding:5px 0; border-bottom:1px solid #edf0f6; font-size:11.3px; }
.row:last-child{ border-bottom:0; }
.row .k{ color:var(--body); }
.row .val{ font-family:'Poppins'; font-weight:700; font-size:12px; color:var(--ink); display:flex; align-items:center; gap:6px; white-space:nowrap; }
.row .val.hi{ color:var(--orange); }
.row .val.dim{ color:#a3acc2; font-weight:600; }
.pill{ font-family:'Inter'; font-weight:700; font-size:8.6px; padding:2px 6px; border-radius:99px; letter-spacing:0; }
.pill.pos{ background:var(--green-bg); color:var(--green); }
.pill.neg{ background:var(--red-bg); color:var(--red); }
.pill.neu{ background:var(--neu-bg); color:var(--muted); }

.mtd{ margin-top:14px; border-radius:13px; background:var(--navy); color:#fff; display:grid; grid-template-columns:1.25fr 1fr 1fr 1fr 1fr; overflow:hidden; position:relative; }
.mtd .cap{ padding:15px 16px 14px 18px; border-right:1px solid rgba(169,195,230,.18); }
.mtd .cap .k{ font-family:'Sora'; font-weight:600; font-size:8px; letter-spacing:.24em; color:var(--orange-l); }
.mtd .cap .h{ font-family:'Poppins'; font-weight:800; font-size:12.5px; margin-top:5px; line-height:1.2; }
.mtd .cap .s{ font-size:9.5px; color:#c9d5ee; margin-top:4px; line-height:1.4; }
.mtd .c{ padding:15px 12px 12px 14px; border-right:1px solid rgba(169,195,230,.14); }
.mtd .c:last-child{ border-right:0; }
.mtd .c .v{ font-family:'Poppins'; font-weight:800; font-size:17px; letter-spacing:-.4px; white-space:nowrap; }
.mtd .c .v .o{ color:var(--orange-l); }
.mtd .c .t{ font-size:9.3px; line-height:1.38; color:#c9d5ee; margin-top:4px; }

.note{ font-size:8.6px; line-height:1.5; color:#8a93ab; margin-top:12px; }
.foot{ position:absolute; left:40px; right:40px; bottom:22px; border-top:1px solid var(--line); padding-top:10px; display:flex; justify-content:space-between; font-size:9px; color:var(--muted); }
.foot b{ font-family:'Poppins'; font-weight:800; color:var(--ink); }
.foot b .o{ color:var(--orange); }

/* ---------- campanhas ---------- */
.card{ border:1px solid var(--line); border-radius:13px; padding:14px 16px; margin-top:14px; }
.card-h{ display:flex; justify-content:space-between; align-items:baseline; margin-bottom:8px; }
.card-h .a{ font-family:'Poppins'; font-weight:800; font-size:13.5px; color:var(--ink); }
.card-h .b{ font-size:9.5px; color:var(--muted); }
table.ct{ width:100%; border-collapse:collapse; font-size:10.2px; }
table.ct th{ font-family:'Sora'; font-weight:600; font-size:7.6px; letter-spacing:.16em; text-transform:uppercase; color:var(--muted); text-align:right; padding:0 0 6px 8px; border-bottom:1px solid var(--line); white-space:nowrap; }
table.ct th:first-child{ text-align:left; padding-left:0; }
table.ct td{ padding:6.5px 0 6.5px 8px; border-bottom:1px solid #edf0f6; text-align:right; color:#1b2550; white-space:nowrap; font-variant-numeric:tabular-nums; }
table.ct tr:last-child td{ border-bottom:0; }
table.ct td:first-child{ text-align:left; padding-left:0; white-space:normal; }
table.ct td .nm{ font-weight:600; color:var(--ink); font-size:10px; word-break:break-word; }
table.ct td .tg{ display:inline-block; font-size:8px; font-weight:700; color:var(--muted); background:var(--neu-bg); border-radius:4px; padding:1px 5px; margin-left:4px; vertical-align:1px; }
table.ct td.best{ color:var(--green); font-weight:700; }
table.ct td.worst{ color:var(--red); font-weight:700; }
table.ct td.strong{ font-family:'Poppins'; font-weight:700; color:var(--ink); }
.share{ display:flex; align-items:center; justify-content:flex-end; gap:6px; }
.share .bar{ width:64px; height:7px; border-radius:4px; background:#eef1f6; overflow:hidden; }
.share .bar i{ display:block; height:100%; background:var(--orange); border-radius:4px; }
.share .p{ font-size:9px; color:var(--muted); width:24px; text-align:right; }

.split{ display:grid; grid-template-columns:1.05fr 1fr; gap:14px; margin-top:14px; }
.split .card{ margin-top:0; }
.legend{ display:flex; gap:14px; font-size:9.5px; color:var(--body); margin-top:6px; }
.legend i{ display:inline-block; width:9px; height:9px; border-radius:3px; margin-right:5px; vertical-align:-1px; }
.post{ display:flex; gap:10px; padding:8px 0; border-bottom:1px solid #edf0f6; }
.post:last-child{ border-bottom:0; }
.post .dt{ flex:0 0 46px; height:46px; border-radius:9px; background:var(--navy); color:#fff; text-align:center; padding-top:7px; }
.post .dt .d1{ font-family:'Poppins'; font-weight:800; font-size:15px; line-height:1; }
.post .dt .d2{ font-family:'Sora'; font-weight:600; font-size:6.5px; letter-spacing:.18em; margin-top:4px; color:var(--sky); }
.post .tp{ font-family:'Sora'; font-weight:600; font-size:7px; letter-spacing:.18em; text-transform:uppercase; color:var(--orange); }
.post .cap{ font-size:10px; color:#1b2550; font-weight:600; line-height:1.35; margin-top:2px; }
.post .ms{ font-size:9.3px; color:var(--muted); margin-top:3px; }
.post .ms b{ font-family:'Poppins'; color:var(--ink); }

.read{ margin-top:14px; background:#fdf0e9; border-left:4px solid var(--orange); border-radius:0 12px 12px 0; padding:13px 18px; }
.read .k{ font-family:'Sora'; font-weight:600; font-size:8px; letter-spacing:.28em; color:var(--orange); }
.read p{ font-size:11px; line-height:1.55; color:#1b2550; margin-top:5px; }
.next{ display:grid; grid-template-columns:repeat(3,1fr); gap:11px; margin-top:12px; }
.next .it{ border:1px solid var(--line); border-radius:12px; padding:12px 14px; }
.next .it .k{ font-family:'Sora'; font-weight:600; font-size:7.5px; letter-spacing:.2em; color:var(--orange); }
.next .it .h{ font-family:'Poppins'; font-weight:800; font-size:12.5px; color:var(--ink); margin-top:4px; line-height:1.25; }
.next .it p{ font-size:9.8px; line-height:1.5; margin-top:4px; color:var(--body); }

.duo{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:12px; }
.fmt{ border:1px solid var(--line); border-radius:12px; padding:13px 15px; }
.fmt.win{ border-color:var(--orange); box-shadow:0 0 0 1px var(--orange) inset; }
.fmt .k{ font-family:'Sora'; font-weight:600; font-size:7.5px; letter-spacing:.2em; color:var(--orange); }
.fmt .h{ font-family:'Poppins'; font-weight:800; font-size:13px; color:var(--ink); margin-top:3px; }
.fmt .g{ display:grid; grid-template-columns:repeat(4,1fr); gap:6px; margin-top:9px; }
.fmt .g .v{ font-family:'Poppins'; font-weight:800; font-size:15px; color:var(--ink); white-space:nowrap; }
.fmt .g .t{ font-size:8.8px; color:var(--muted); margin-top:1px; }

/* ---------- plataformas ---------- */
.plat .pgrid{ display:grid; grid-template-columns:1fr 1.15fr; gap:18px; align-items:center; }
.pb{ display:flex; align-items:center; gap:10px; margin:5px 0; }
.pb .pl{ width:58px; font-size:9.5px; color:var(--muted); font-weight:600; }
.pbar{ flex:1; display:flex; height:20px; gap:2px; }
.pbar i{ display:flex; align-items:center; justify-content:center; font-style:normal; font-size:8.5px; font-weight:700; color:#fff; border-radius:4px; }
.pts{ display:flex; gap:10px; }
.pt{ flex:1; border-left:1px solid var(--line); padding-left:10px; }
.pt .pn{ font-size:9.5px; font-weight:600; color:var(--body); display:flex; align-items:center; gap:5px; }
.pt .pn i{ width:8px; height:8px; border-radius:2px; display:inline-block; }
.pt .pv{ font-family:'Poppins'; font-weight:800; font-size:16px; color:var(--ink); margin-top:2px; white-space:nowrap; }
.pt .pv.best{ color:var(--green); }
.pt .ps{ font-size:8.6px; color:var(--muted); margin-top:1px; line-height:1.35; }
.funnel{ display:grid; grid-template-columns:repeat(3,1fr); gap:3px; margin-top:4px; }
.fs{ padding:10px 14px 10px 16px; background:var(--panel); }
.fs:nth-child(1){ border-radius:10px 0 0 10px; } .fs:nth-child(3){ border-radius:0 10px 10px 0; background:#fdf0e9; }
.fs:nth-child(2){ background:#e6edf8; }
.fs .k{ font-family:'Sora'; font-weight:600; font-size:7.5px; letter-spacing:.18em; color:var(--muted); text-transform:uppercase; }
.fs .v{ font-family:'Poppins'; font-weight:800; font-size:20px; color:var(--ink); margin-top:2px; }
.fs .p{ font-size:9px; color:var(--muted); margin-top:1px; }
.frate{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:8px; font-size:10px; color:var(--body); }

/* ---------- ChatGPT Ads (Sanrire) ---------- */
.gpt{ margin-top:14px; border-radius:14px; background:var(--navy); color:#fff; padding:16px 18px 14px; position:relative; overflow:hidden; }
.gpt::after{ content:""; position:absolute; right:-90px; top:-110px; width:300px; height:300px; border-radius:50%; background:radial-gradient(circle, rgba(120,150,220,.28), rgba(0,36,125,0) 65%); }
.gpt .top{ display:flex; justify-content:space-between; align-items:flex-start; position:relative; z-index:1; }
.gpt .k{ font-family:'Sora'; font-weight:600; font-size:8px; letter-spacing:.26em; color:var(--orange-l); }
.gpt .h{ font-family:'Poppins'; font-weight:800; font-size:16px; margin-top:4px; }
.gpt .h .o{ color:var(--orange-l); }
.gpt .cmp{ font-size:9.5px; color:#c9d5ee; margin-top:3px; }
.gpt .tag{ font-size:8.5px; font-weight:700; background:rgba(255,255,255,.1); border:1px solid rgba(169,195,230,.3); border-radius:99px; padding:4px 9px; color:#fff; white-space:nowrap; }
.gpt .pair{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:11px; position:relative; z-index:1; }
.gpt .per{ background:rgba(255,255,255,.06); border:1px solid rgba(169,195,230,.2); border-radius:11px; padding:10px 12px; }
.gpt .per.on{ background:var(--orange); border-color:var(--orange); }
.gpt .per .ph{ display:flex; justify-content:space-between; align-items:baseline; }
.gpt .per .ph .a{ font-family:'Poppins'; font-weight:800; font-size:12.5px; }
.gpt .per .ph .b{ font-family:'Sora'; font-weight:600; font-size:7.5px; letter-spacing:.16em; opacity:.85; }
.gpt .per .g{ display:grid; grid-template-columns:repeat(3,1fr); gap:7px 8px; margin-top:8px; }
.gpt .per .g .v{ font-family:'Poppins'; font-weight:800; font-size:14.5px; white-space:nowrap; letter-spacing:-.3px; }
.gpt .per .g .t{ font-size:8.5px; opacity:.85; margin-top:1px; }
.gpt .prints{ display:grid; grid-template-columns:1.2fr 1fr; gap:10px; margin-top:10px; position:relative; z-index:1; }
.gpt .prints figure{ background:#fff; border-radius:8px; padding:5px; }
.gpt .prints img{ width:100%; display:block; border-radius:4px; }
.gpt .prints figcaption{ font-size:7.5px; color:var(--muted); margin-top:3px; font-family:'Sora'; letter-spacing:.12em; text-transform:uppercase; }
.cprints{ position:absolute; left:47px; right:47px; top:502px; }
.cprints .k{ font-family:'Sora'; font-weight:600; font-size:9px; letter-spacing:.3em; color:var(--orange-l); margin-bottom:8px; }
.cprints figure{ background:#fff; border-radius:10px; padding:6px 8px 4px; margin-bottom:8px; }
.cprints img{ width:100%; display:block; }
.cprints figcaption{ font-family:'Sora'; font-weight:600; font-size:7.5px; letter-spacing:.16em; text-transform:uppercase; color:var(--muted); margin-top:3px; }
.gpt .fn{ font-size:8.4px; line-height:1.45; color:#c9d5ee; margin-top:9px; position:relative; z-index:1; }

table.cmp3{ width:100%; border-collapse:collapse; font-size:10.6px; }
table.cmp3 th{ white-space:nowrap; font-family:'Sora'; font-weight:600; font-size:7.6px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); text-align:right; padding:0 0 6px 6px; border-bottom:1px solid var(--line); }
table.cmp3 th:first-child{ text-align:left; padding-left:0; }
table.cmp3 td{ padding:5.2px 0 5.2px 6px; border-bottom:1px solid #edf0f6; text-align:right; white-space:nowrap; }
table.cmp3 td:first-child{ text-align:left; padding-left:0; }
table.cmp3 td.v{ font-family:'Poppins'; font-weight:700; color:var(--ink); }
table.cmp3 td.p{ color:#a3acc2; font-family:'Poppins'; font-weight:600; }
table.cmp3 tr.grp td{ font-family:'Sora'; font-weight:600; font-size:7.6px; letter-spacing:.22em; color:var(--orange); text-transform:uppercase; padding-top:9px; border-bottom:0; }
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@700;800;900'
         '&family=Sora:wght@400;600&display=swap" rel="stylesheet">')


def document(title, pages):
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{esc(title)}</title>'
            f'{FONTS}<style>{CSS}</style></head><body>{"".join(pages)}</body></html>')


LOGO = '<div class="logo">Grupo Opera<span class="dot">.</span></div>'


def footer(brand, n):
    return (f'<div class="foot"><span><b>Grupo Opera<span class="o">.</span></b> · Relatório semanal {esc(brand)}</span>'
            f'<span>{n:02d}</span></div>')


def topbar(brand, a, b):
    return (f'<div class="topbar"><div>{LOGO}<div class="brand">{esc(brand)}</div></div>'
            f'<div class="rt"><div class="a">{esc(a)}</div><div class="b">{esc(b)}</div></div></div>')


# ---------------------------------------------------------------- capa

def cover(b):
    c = b["cover"]
    h1 = rich(c["h1"][0]) + f'<span class="l2">{rich(c["h1"][1])}</span>'
    strip = "".join(f'<div class="cell"><div class="v">{rich(v)}</div><div class="t">{rich(t)}</div></div>' for v, t in c["strip"])
    return f'''
<section class="page cover">
  {LOGO.replace('class="logo"', 'class="logo"')}
  <div class="head">
  <div class="eyebrow">Relatório semanal · {esc(b["brand_upper"])}</div>
  <h1>{h1}</h1>
  <p class="intro">{rich(c["intro"])}</p>
  <div class="chips">
    <span class="chip">Semana anterior · 11 a 17/10</span><span class="chip on">Semana atual · 18 a 24/10</span>
  </div>
  </div>
  {c.get("extra", "")}
  <div class="hl">
    <div class="big"><div class="num" style="font-size:{c.get("hl_size", 58)}px">{c["hl_num"]}</div><div class="lab">{esc(c["hl_lab"])}</div></div>
    <div class="txt"><div class="kick">DESTAQUE DA SEMANA</div><h3>{rich(c["hl_h"])}</h3><p>{rich(c["hl_p"])}</p></div>
  </div>
  <div class="strip">{strip}</div>
</section>'''


# ---------------------------------------------------------------- página de números

def kpi_cards(kpis):
    out = []
    for k in kpis:
        v = rich(k["v"])
        if k.get("small"):
            v += f'<small>{rich(k["small"])}</small>'
        cls, txt = k["d"]
        out.append(f'<div class="kpi"><div class="v">{v}</div><div class="t">{rich(k["t"])}</div><div class="d {cls}">{rich(txt)}</div></div>')
    return f'<div class="kpis">{"".join(out)}</div>'


def columns(groups):
    """groups: [(titulo, [(rotulo, prev_txt, cur_txt, pill_html, hi_bool)])]"""
    prev_rows, cur_rows = [], []
    for title, rows in groups:
        prev_rows.append(f'<div class="grp">{esc(title)}</div>')
        cur_rows.append(f'<div class="grp">{esc(title)}</div>')
        for lab, p, c, pill, hi in rows:
            pcls = "val dim" if p == "—" else "val"
            prev_rows.append(f'<div class="row"><span class="k">{esc(lab)}</span><span class="{pcls}">{p}</span></div>')
            ccls = "val hi" if hi else "val"
            cur_rows.append(f'<div class="row"><span class="k">{esc(lab)}</span><span class="{ccls}">{c}{pill}</span></div>')
    return f'''
<div class="cols">
  <div class="col"><div class="hd"><span class="a">Semana anterior</span><span class="b">11 a 17/10 · 7 dias</span></div><div class="bd">{"".join(prev_rows)}</div></div>
  <div class="col cur"><div class="hd"><span class="a">Semana atual</span><span class="b">18 a 24/10 · 7 dias</span></div><div class="bd">{"".join(cur_rows)}</div></div>
</div>'''


def mtd_strip(cap_h, cap_s, cells):
    cs = "".join(f'<div class="c"><div class="v">{rich(v)}</div><div class="t">{rich(t)}</div></div>' for v, t in cells)
    return (f'<div class="mtd"><div class="cap"><div class="k">OUTUBRO ATÉ AGORA</div><div class="h">{rich(cap_h)}</div>'
            f'<div class="s">{rich(cap_s)}</div></div>{cs}</div>')


def page_numbers(b, n=2):
    p = b["numbers"]
    return f'''
<section class="page">
  {topbar(b["brand_upper"], "Relatório semanal", "Semana de 18 a 24/10/2026")}
  <div class="content">
    <div class="sec"><span class="n">01</span><span>Semana × semana anterior</span></div>
    <h2>{rich(p["h2"])}</h2>
    <p class="lead">{rich(p["lead"])}</p>
    {kpi_cards(p["kpis"])}
    {columns(p["groups"])}
    {mtd_strip(*p["mtd"])}
    {p.get("extra", "")}
    <p class="note">{rich(p["note"])}</p>
  </div>
  {footer(b["brand"], n)}
</section>'''


# ---------------------------------------------------------------- gráficos (SVG)

def svg_daily_pair(prev, cur, labels, w=330, h=150, peak_fmt=None):
    """14 barras diárias: semana anterior (azul) + semana atual (laranja)."""
    vals = list(prev) + list(cur)
    mx = max(vals) or 1
    # eixo "redondo"
    import math
    tick, top = nice_axis(mx)
    padl, padb, padt = 30, 18, 16
    pw, ph = w - padl - 4, h - padb - padt
    n = len(vals)
    gap = 3
    bw = (pw - gap * (n - 1)) / n
    g = []
    t = 0
    while t <= top + 1e-9:
        y = padt + ph - ph * t / top
        lab = mil_short(t)
        g.append(f'<line x1="{padl}" x2="{w-4}" y1="{y:.1f}" y2="{y:.1f}" stroke="#edf0f6" stroke-width="1"/>'
                 f'<text x="{padl-6}" y="{y+3:.1f}" text-anchor="end" font-size="8" fill="#8a93ab" font-family="Inter">{lab}</text>')
        t += tick
    imax = vals.index(mx)
    for i, v in enumerate(vals):
        x = padl + i * (bw + gap)
        bh = max(ph * v / top, 1.5 if v > 0 else 0)
        y = padt + ph - bh
        col = "#00247d" if i < len(prev) else "#e85d1b"
        r = min(3, bw / 2)
        if bh > 0:
            g.append(f'<path d="M{x:.1f},{padt+ph:.1f} V{y+r:.1f} Q{x:.1f},{y:.1f} {x+r:.1f},{y:.1f} H{x+bw-r:.1f} Q{x+bw:.1f},{y:.1f} {x+bw:.1f},{y+r:.1f} V{padt+ph:.1f} Z" fill="{col}"/>')
        if i in (0, 7, 13):
            anc, xx = ("end", x + bw) if i == n - 1 else (("start", x) if i == 0 else ("middle", x + bw / 2))
            g.append(f'<text x="{xx:.1f}" y="{h-5}" text-anchor="{anc}" font-size="8" fill="#8a93ab" font-family="Inter">{labels[i]}</text>')
    xm = padl + imax * (bw + gap) + bw / 2
    ym = padt + ph - ph * mx / top
    txt = f"pico {n0(mx)} em {labels[imax]}" if not peak_fmt else peak_fmt(mx, labels[imax])
    anchor = "start" if imax < n * 0.55 else "end"
    dx = -4 if anchor == "start" else 4
    g.append(f'<text x="{xm+dx:.1f}" y="{ym-5:.1f}" text-anchor="{anchor}" font-size="8.5" font-weight="700" fill="#e85d1b" font-family="Inter">{txt}</text>')
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{"".join(g)}</svg>'


def svg_daily_single(days, values, w=330, h=140, color="#e85d1b", money=True, mark=None):
    """Barras diárias (uma série). days: rótulos dd/mm; values: números."""
    import math
    mx = max(values) or 1
    tick, top = nice_axis(mx)
    padl, padb, padt = 34, 18, 10
    pw, ph = w - padl - 4, h - padb - padt
    n = len(values)
    gap = 2
    bw = (pw - gap * (n - 1)) / n
    g = []
    t = 0
    while t <= top + 1e-9:
        y = padt + ph - ph * t / top
        lab = ("R$" + n0(t)) if money else mil_short(t)
        g.append(f'<line x1="{padl}" x2="{w-4}" y1="{y:.1f}" y2="{y:.1f}" stroke="#edf0f6"/>'
                 f'<text x="{padl-5}" y="{y+3:.1f}" text-anchor="end" font-size="7.5" fill="#8a93ab" font-family="Inter">{lab}</text>')
        t += tick
    for i, v in enumerate(values):
        x = padl + i * (bw + gap)
        bh = ph * v / top
        if v > 0 and bh < 1.5:
            bh = 1.5
        y = padt + ph - bh
        col = color(i) if callable(color) else color
        r = min(2.5, bw / 2)
        if bh > 0:
            g.append(f'<path d="M{x:.1f},{padt+ph:.1f} V{y+r:.1f} Q{x:.1f},{y:.1f} {x+r:.1f},{y:.1f} H{x+bw-r:.1f} Q{x+bw:.1f},{y:.1f} {x+bw:.1f},{y+r:.1f} V{padt+ph:.1f} Z" fill="{col}"/>')
        if i % 4 == 0 or i == n - 1:
            anc, xx = ("end", x + bw) if i == n - 1 else ("middle", x + bw / 2)
            if i == n - 1 or n - 1 - i >= 3:
                g.append(f'<text x="{xx:.1f}" y="{h-5}" text-anchor="{anc}" font-size="7.5" fill="#8a93ab" font-family="Inter">{days[i]}</text>')
    if mark:
        i0, i1, txt = mark
        x0 = padl + i0 * (bw + gap) - 1
        x1 = padl + i1 * (bw + gap) + bw + 1
        g.insert(0, f'<rect x="{x0:.1f}" y="{padt}" width="{x1-x0:.1f}" height="{ph}" fill="#fdf0e9" rx="3"/>')
        g.append(f'<text x="{(x0+x1)/2:.1f}" y="{padt+ph/2:.1f}" text-anchor="middle" font-size="8" font-weight="700" fill="#e85d1b" font-family="Inter">{txt}</text>')
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{"".join(g)}</svg>'


def nice_axis(mx, max_ticks=4):
    import math
    base = 10 ** (int(math.floor(math.log10(mx))) - 1) if mx >= 10 else 1
    for mult in (1, 2, 2.5, 5, 10, 20, 25, 50, 100):
        tick = base * mult
        if math.ceil(mx / tick) <= max_ticks:
            return tick, tick * math.ceil(mx / tick)
    return mx, mx


def mil_short(t):
    if t >= 1000:
        v = t / 1000
        return (n0(v) if v == int(v) else n1(v)) + "k"
    return n0(t)


# ---------------------------------------------------------------- página de campanhas

def meta_table(camps, total_spend):
    """camps: [nome, resultado, tipo, custo_resultado, gasto, alcance, impressões, ctr, cpc, cpm, freq]"""
    conv_costs = [c[3] for c in camps if c[2] == "Conversa" and c[1] > 0]
    best = min(conv_costs) if len(conv_costs) > 1 else None
    worst = max(conv_costs) if len(conv_costs) > 1 else None
    rows = []
    for c in sorted(camps, key=lambda c: -c[4]):
        nome, res, tipo, cpr, gasto, alc, imp, ctr, cpc = c[:9]
        sh = gasto / total_spend * 100
        lab = {"Conversa": "conversas", "Link Click": "cliques no link", "Visita ao perfil": "visitas ao perfil"}.get(tipo, tipo)
        if tipo == "Conversa" and res == 1:
            lab = "conversa"
        cls = ""
        if tipo == "Conversa" and best is not None and cpr == best:
            cls = "best"
        elif tipo == "Conversa" and worst is not None and cpr == worst:
            cls = "worst"
        rows.append(
            f'<tr><td><span class="nm">{esc(nome)}</span></td>'
            f'<td><div class="share">{brl(gasto, 0)}<span class="bar"><i style="width:{sh:.1f}%"></i></span><span class="p">{n0(sh)}%</span></div></td>'
            f'<td class="strong">{n0(res)} <span style="font-family:Inter;font-weight:500;color:#7b86a3;font-size:9px">{lab}</span></td>'
            f'<td class="{cls}">{brl(cpr)}</td><td>{pct(ctr)}</td><td>{n0(alc)}</td></tr>')
    return ('<table class="ct"><thead><tr><th>Campanha</th><th>Investimento · % da verba</th><th>Resultado</th>'
            '<th>Custo/result.</th><th>CTR</th><th>Alcance</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table>')


def gads_table(camps):
    """camps: [nome, tipo, cliques, custo, impressões, conversões, ctr(fração), cpc, custo/conv]"""
    rows = []
    for c in sorted(camps, key=lambda c: -c[3]):
        nome, tipo, cl, cost, imp, conv, ctr, cpc, cpconv = c
        cc = brl(cpconv) if conv > 0 else '<span style="color:#a3acc2">—</span>'
        rows.append(f'<tr><td><span class="nm">{esc(nome)}</span><span class="tg">{esc(tipo)}</span></td><td>{brl(cost, 0)}</td>'
                    f'<td>{n0(cl)}</td><td>{n0(imp)}</td><td>{pct(ctr*100)}</td><td>{brl(cpc)}</td>'
                    f'<td class="strong">{n1(conv) if conv and conv != int(conv) else n0(conv)}</td><td>{cc}</td></tr>')
    return ('<table class="ct"><thead><tr><th>Campanha</th><th>Invest.</th><th>Cliques</th><th>Impr.</th><th>CTR</th><th>CPC</th>'
            '<th>Conv.</th><th>Custo/conv.</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table>')


def posts_list(posts, limit=3):
    meses = {"10": "OUT", "09": "SET"}
    out = []
    for p in posts[:limit]:
        d, tipo, cap, url, reach, views, inter, eng = p[:8]
        dd, mm = d[8:10], d[5:7]
        out.append(f'<div class="post"><div class="dt"><div class="d1">{dd}</div><div class="d2">{meses.get(mm, mm)}</div></div>'
                   f'<div><div class="tp">{esc(tipo)}</div><div class="cap">{esc(cap)}</div>'
                   f'<div class="ms"><b>{n0(reach)}</b> alcance · <b>{n0(views)}</b> views · <b>{n0(inter)}</b> interações · <b>{pct(eng*100)}</b> eng.</div></div></div>')
    return "".join(out)


def read_box(txt):
    return f'<div class="read"><div class="k">LEITURA</div><p>{rich(txt)}</p></div>'


def next_steps(items):
    its = "".join(f'<div class="it"><div class="k">PRÓXIMO 0{i+1}</div><div class="h">{rich(h)}</div><p>{rich(t)}</p></div>'
                  for i, (h, t) in enumerate(items))
    return f'<div class="next">{its}</div>'


PLAT_COL = {"Facebook": "#00247d", "Instagram": "#e85d1b", "Outros": "#a9b3c9"}


def platform_split(rows, total_spend, total_conv, note=""):
    """rows: [(nome, gasto, conversas)]; inclui 'Outros' se a soma não fechar o total."""
    rows = list(rows)
    rs = total_spend - sum(r[1] for r in rows)
    rc = total_conv - sum(r[2] for r in rows)
    if rs > 1 or rc > 0:
        rows.append(("Outros", rs, rc))

    def bar(idx, total, label):
        segs = []
        for r in rows:
            v = r[idx]
            if v <= 0:
                continue
            w = v / total * 100
            txt = f"{n0(w)}%" if w >= 9 else ""
            segs.append(f'<i style="width:{w:.2f}%;background:{PLAT_COL[r[0]]}">{txt}</i>')
        return f'<div class="pb"><span class="pl">{label}</span><span class="pbar">{"".join(segs)}</span></div>'
    tiles = []
    costs = {r[0]: (r[1] / r[2] if r[2] else None) for r in rows}
    valid = [c for c in costs.values() if c]
    best = min(valid) if len(valid) > 1 else None
    for r in rows:
        cp = costs[r[0]]
        cls = " best" if cp and cp == best else ""
        tiles.append(f'<div class="pt"><div class="pn"><i style="background:{PLAT_COL[r[0]]}"></i>{r[0]}</div>'
                     f'<div class="pv{cls}">{brl(cp) if cp else "—"}</div><div class="ps">por conversa<br>{n0(r[2])} conv. · {brl(r[1], 0)}</div></div>')
    return (f'<div class="card plat"><div class="card-h"><span class="a">Facebook × Instagram</span><span class="b">onde as conversas nasceram · semana atual</span></div>'
            f'<div class="pgrid"><div>{bar(1, total_spend, "Verba")}{bar(2, total_conv, "Conversas")}</div><div class="pts">{"".join(tiles)}</div></div>'
            + (f'<p class="note" style="margin-top:8px">{rich(note)}</p>' if note else "") + '</div>')
