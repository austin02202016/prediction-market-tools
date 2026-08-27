#!/usr/bin/env python3
import json, sys, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CATS = {"Terminals & Aggregators","Trading Bots & Chat Trading","Arbitrage","Copy Trading & Portfolio","Analytics & Whale Tracking","Alerts","AI Agents & Research","Data & APIs","Dashboards","Infrastructure & DeFi","Parlays & Leverage","News & Education","Directories & Other"}
STATUS = {"live","beta","shut_down","domain_expired","unreachable","unverified"}
REQ = ["name","url","category","description","venues","executes_trades","pricing","status","status_note","last_verified","sources"]
tools = json.load(open(ROOT / "tools.json")); errs = []; seen = set()
for t in tools:
    for k in REQ:
        if k not in t: errs.append(f"{t.get('name')}: missing {k}")
    if t.get("category") not in CATS: errs.append(f"{t.get('name')}: bad category {t.get('category')}")
    if t.get("status") not in STATUS: errs.append(f"{t.get('name')}: bad status")
    if len((t.get("description") or "").split()) > 32: errs.append(f"{t.get('name')}: description over 30 words")
    if re.search(r"[—–]", t.get("description","")): errs.append(f"{t.get('name')}: dash in description")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", t.get("last_verified","")): errs.append(f"{t.get('name')}: bad last_verified")
    key = t.get("url","").lower().rstrip("/")
    if key in seen: errs.append(f"duplicate url {key}")
    seen.add(key)
print("\n".join(errs) or f"ok: {len(tools)} tools"); sys.exit(1 if errs else 0)
