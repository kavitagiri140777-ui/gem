# GeM Bid Matcher + Park Bid Finder UI

This project now supports two things:
1. **GeM advanced-search based sourcing** of bid pages using keywords.
2. A **Park Bid Finder** frontend component in React for quick shortlist review.

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

If GeM page structure changes, tune `gem_bid_matcher/scraper.py` parser.

## Frontend component

`frontend/ParkBidFinder.tsx` follows your requested list-detail layout with score cards and bid detail actions.
