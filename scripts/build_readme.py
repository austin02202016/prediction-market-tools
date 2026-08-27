#!/usr/bin/env python3
"""Generate README.md from tools.json. Run: python3 scripts/build_readme.py"""
import json, datetime, collections, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
tools = json.load(open(ROOT / "tools.json"))
ORDER = ["Terminals & Aggregators","Trading Bots & Chat Trading","Arbitrage","Copy Trading & Portfolio","Analytics & Whale Tracking","Alerts","AI Agents & Research","Data & APIs","Dashboards","Infrastructure & DeFi","Parlays & Leverage","News & Education","Directories & Other"]
STATUS = {"live":"Live","beta":"Beta","shut_down":"Shut down","domain_expired":"Domain expired","unreachable":"Unreachable","unverified":"Unverified"}
def ex(v): return {True:"Yes",False:"No"}.get(v,"?")
def venues(v): return ", ".join(v) if v else ""
def esc(s): return (s or "").replace("|","\\|")
def anchor(s): return re.sub(r"[^a-z0-9 -]","",s.lower()).replace(" ","-")
by = collections.defaultdict(list)
for t in tools: by[t["category"]].append(t)
live = [t for t in tools if t["status"] in ("live","beta")]
dead = [t for t in tools if t["status"] in ("shut_down","domain_expired")]
today = max(t["last_verified"] for t in tools)
out = []
out.append("# Prediction Market Tools, Verified\n")
out.append(f"A maintained directory of prediction market tools for Polymarket, Kalshi, Predict.fun, Limitless, Myriad, Hyperliquid, Manifold and the wider forecasting ecosystem. Every entry carries the venues it covers, whether it executes trades, its pricing, and a **status with a last-verified date**. Links are re-checked automatically every week; anything that stops resolving is flagged, not silently kept.\n")
out.append(f"**{len(tools)} tools. {len(live)} live or in beta. {len(dead)} shut down or expired. Last full verification: {today}.**\n")
out.append("The data lives in [`tools.json`](tools.json); this README is generated from it. To add or correct a tool, edit `tools.json` and open a pull request (see [CONTRIBUTING.md](CONTRIBUTING.md)). Descriptions state what a tool does; accuracy and profit claims are the vendor's, not ours.\n")
out.append("## Contents\n")
for c in ORDER:
    if by.get(c): out.append(f"- [{c}](#{anchor(c)}) ({len(by[c])})")
out.append(f"- [Shut down or expired](#shut-down-or-expired) ({len(dead)})")
out.append("- [How verification works](#how-verification-works)\n")
for c in ORDER:
    items = [t for t in by.get(c, []) if t["status"] not in ("shut_down","domain_expired")]
    if not items: continue
    out.append(f"## {c}\n")
    out.append("| Tool | What it does | Venues | Executes | Pricing | Status |")
    out.append("|---|---|---|---|---|---|")
    for t in sorted(items, key=lambda x: (0 if x.get("featured") else 1, x["name"].lower())):
        name = f"[{esc(t['name'])}]({t['url']})"
        if t.get("github") and t.get("github") != t["url"]: name += f" ([source]({t['github']}))"
        st = STATUS[t["status"]] + f" · {t['last_verified']}"
        out.append(f"| {name} | {esc(t['description'])} | {esc(venues(t.get('venues')))} | {ex(t.get('executes_trades'))} | {esc(t.get('pricing') or 'Not published')} | {st} |")
    out.append("")
out.append("## Shut down or expired\n")
out.append("Kept for the record so nobody routes money through a dead tool. Each row states the evidence.\n")
out.append("| Tool | Was | Status | Evidence |")
out.append("|---|---|---|---|")
for t in sorted(dead, key=lambda x: x["name"].lower()):
    out.append(f"| {esc(t['name'])} | {esc(t['category'])} | {STATUS[t['status']]} · {t['last_verified']} | {esc(t.get('status_note',''))} |")
out.append("")
out.append("## How verification works\n")
out.append("- **Status** is set from evidence, never from a vendor's own claim: `live` means the site loads and shows current activity; `beta` means the vendor labels it so; `shut_down` needs a shutdown notice or a news article; `domain_expired` needs a registrar or parking page; `unreachable` means it failed our check and no other signal was found; `unverified` means we have not checked it yet.")
out.append("- **Executes** is Yes only if the tool places orders on a venue itself. Alert bots, screeners, and dashboards that link out to a venue are No.")
out.append("- **A weekly GitHub Action** re-fetches every URL. Failures open an issue rather than editing the table, so a bot never marks a tool dead on a transient error; a human confirms.")
out.append("- **Descriptions** describe function. We do not repeat accuracy percentages, ROI claims, or 'first' claims from vendor copy.")
out.append("- Every field has a `sources` list in `tools.json` with the pages we loaded.\n")
out.append("## Contributing\n")
out.append("Add a tool by adding an object to `tools.json` and running `python3 scripts/build_readme.py`. Required: name, url, category, description (your own words, under 30 words), venues, executes_trades, pricing, status, status_note, last_verified, sources. Vendors may submit their own tool; say so in the PR. Entries with unverifiable claims are edited, not rejected.\n")
out.append("## License\n")
out.append("Data (`tools.json`) and text: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Scripts: MIT.\n")
(ROOT / "README.md").write_text("\n".join(out))
print(f"README written: {len(tools)} tools, {len(live)} live, {len(dead)} dead")
