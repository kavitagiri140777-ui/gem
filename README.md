# GeM Bid Matcher + Park Bid Finder UI

This project supports:
1. **GeM advanced-search based sourcing** of bid pages using keywords.
2. A **Park Bid Finder** frontend component in React for quick shortlist review.
3. **Bid number extraction/display** in backend output and frontend cards.

## Advanced search on GeM portal

Use Park profile defaults (Visakhapatnam + Navy + your work categories) and fetch from generated GeM advanced-search URLs:

```bash
python -m gem_bid_matcher.cli \
  --use-park-profile \
  --gem-advanced-search
```

Add/override keywords and location:

```bash
python -m gem_bid_matcher.cli \
  --gem-advanced-search \
  --location "Visakhapatnam" \
  --skill "safety nets" \
  --skill "safety posters" \
  --skill "acrylic boards" \
  --buyer "Indian Navy"
```

## Bid Number

- `Bid.bid_number` is now part of parsed and ranked output.
- Parser extracts patterns like `GEM/2026/B/510001` from bid title/row text.
- UI shows `Bid No` in list and details.

If GeM page structure changes, tune `gem_bid_matcher/scraper.py` parser.
