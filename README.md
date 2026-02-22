# GeM Bid Matcher + Park Bid Finder UI

This project supports:
1. **GeM advanced-search based sourcing** of bid pages using keywords.
2. A **Park Bid Finder** frontend component in React for quick shortlist review.
3. **Bid number extraction/display** in backend output and frontend cards.

## Merge-conflict resolved files

This branch reconciles changes for files that commonly conflict during PR merge:
- `README.md`
- `gem_bid_matcher/cli.py`
- `gem_bid_matcher/matcher.py`
- `gem_bid_matcher/models.py`
- `gem_bid_matcher/scraper.py`
- `sample-bids.html`

## Advanced search on GeM portal

```bash
python -m gem_bid_matcher.cli --use-park-profile --gem-advanced-search
```

Custom keyword search:

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

- `Bid.bid_number` is part of parsed and ranked output.
- Parser extracts patterns like `GEM/2026/B/510001` from bid title/row text.
