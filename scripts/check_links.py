#!/usr/bin/env python3
"""Re-fetch every URL in tools.json. Prints failures; exit 1 if any live tool fails. Never edits tools.json."""
import json, sys, ssl, urllib.request, concurrent.futures, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
ctx = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (compatible; pm-tools-linkcheck/1.0; +https://github.com/)"}
def chk(t):
    if t["status"] not in ("live","beta"): return None
    try:
        with urllib.request.urlopen(urllib.request.Request(t["url"], headers=UA), timeout=20, context=ctx) as r:
            body = r.read(100000).decode("utf-8","ignore").lower()
            parked = any(k in body for k in ["domain is for sale","buy this domain","this domain may be for sale","hugedomains","afternic"])
            return (t["name"], t["url"], "parked" if parked else None)
    except Exception as e:
        code = getattr(e, "code", None)
        if code in (401,403,405,429,999): return None  # bot-blocked, not down
        return (t["name"], t["url"], f"{type(e).__name__}: {str(e)[:80]}")
tools = json.load(open(ROOT / "tools.json"))
with concurrent.futures.ThreadPoolExecutor(16) as ex: res = [r for r in ex.map(chk, tools) if r and r[2]]
for name, url, why in res: print(f"FAIL {name} {url} :: {why}")
print(f"checked {sum(1 for t in tools if t['status'] in ('live','beta'))} live URLs, {len(res)} failures")
sys.exit(1 if res else 0)
