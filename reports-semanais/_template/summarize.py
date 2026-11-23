"""Resumo em texto dos dados de um cliente (apoio para escrever a narrativa)."""
import json, sys
from pathlib import Path
import build
wk = Path(sys.argv[1])
for slug in sys.argv[2:]:
    data = json.loads((wk / "data" / f"{slug}.json").read_text())
    M, groups = build.build_metrics(data)
    print(f"===== {data['client']} ({slug})")
    for title, keys in groups:
        print(" ", title)
        for k in keys:
            m = M[k]
            print(f"    {k:22s} {m.label:28s} prev={m.prev_s:>12s} cur={m.cur_s:>12s} {m.delta_s} {m.tone}")
    extra = [k for k in M if not any(k in g for _, g in groups)]
    for k in extra:
        print(f"    (extra) {k}: {M[k].label} cur={M[k].cur_s} prev={M[k].prev_s}")
    for a in data.get("meta_ads", []):
        if a.get("daily"):
            print("  daily", a["account_name"], [(r[0][8:], round(r[1]), r[2], r[3], r[4]) for r in a["daily"]])
        for c in a.get("campaigns") or []:
            name, sp, cv, ld, ck, im = (c + [0]*6)[:6]
            print(f"    camp {name[:40]:40s} R${sp:>8.2f} conv={cv} cpconv={sp/cv if cv else 0:.2f} leads={ld} clk={ck} imp={im}")
    for ig in data.get("instagram", []):
        for kind in ("reels", "posts"):
            for r in ig.get(kind) or []:
                print(f"    {kind} {r['date']} reach={r['reach']} views={r['views']} int={r['interactions']} eng={r.get('eng_rate')} | {r['title']}")
    for o in data.get("other", []):
        print("  other", o.get("platform"), o.get("account_name"), [(m['label_pt'], m.get('prev'), m.get('cur')) for m in o.get('metrics', [])])
    print("  errors:", data.get("errors"))
    print("  notes:", data.get("notes"))
