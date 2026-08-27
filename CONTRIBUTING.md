# Contributing

Edit `tools.json`, run `python3 scripts/build_readme.py`, commit both files, open a pull request.

One object per tool:

```json
{
  "name": "Example",
  "url": "https://example.com",
  "category": "Analytics & Whale Tracking",
  "description": "Under 30 words, your own wording, what it does. No accuracy or ROI claims.",
  "venues": ["Polymarket", "Kalshi"],
  "executes_trades": false,
  "pricing": "Free + Pro $29/mo",
  "open_source": false,
  "github": null,
  "backers": null,
  "status": "live",
  "status_note": "Site loads, changelog entry dated 2026-08-20.",
  "last_verified": "2026-08-27",
  "sources": ["https://example.com", "https://example.com/pricing"]
}
```

Rules:

- Vendors are welcome to add their own tool. Say so in the PR.
- `status` comes from evidence you looked at, stated in `status_note`. A vendor saying "live" is not evidence; a loading site with a dated post is.
- `executes_trades` is true only when the tool itself places orders on a venue.
- Descriptions state function. Accuracy percentages, ROI, "first", and "best" are removed in review.
- No dashes in descriptions (they break the table). Use a period or a comma.
- Dead tools stay in the file with `shut_down` or `domain_expired` and a source; they move to the bottom table automatically.
- Run `python3 scripts/validate.py` before pushing; CI runs the same check.
