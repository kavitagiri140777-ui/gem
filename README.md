# GeM Bid Matcher (Starter Application)

This project is a starter app that helps you:

1. Scrape bid listing pages from the GeM portal (or saved HTML export).
2. Normalize bids into structured data.
3. Filter and score bids using your criteria:
   - preferred locations
   - required categories / keywords
   - your experience keywords
   - minimum bid value

> ⚠️ Note: Government portals may use login, anti-bot controls, and Terms of Service restrictions. Use this only in ways allowed by GeM policies.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m gem_bid_matcher.cli --help
```

## Run from a URL

```bash
python -m gem_bid_matcher.cli \
  --source-url "https://example.com/gem-bids-listing" \
  --location "Delhi" \
  --location "Noida" \
  --skill "IT services" \
  --skill "network maintenance" \
  --experience "government project" \
  --experience "SLA" \
  --min-value 100000
```

## Run from saved HTML file

```bash
python -m gem_bid_matcher.cli \
  --source-file ./sample-bids.html \
  --location "Mumbai" \
  --skill "civil work" \
  --experience "road construction"
```

## Input assumptions

The parser expects bid entries to be in table rows (`<tr>`) with columns that include details like:
- bid title / description
- department / buyer
- location
- category
- bid value
- end date
- URL

If GeM changes page structure, update `gem_bid_matcher/scraper.py` selectors.

## Output

The CLI prints ranked matches as JSON to stdout, with fields:
- `score`
- `title`
- `location`
- `category`
- `bid_value`
- `match_reasons`
- `url`

## Next improvements

- Add authenticated scraping workflow (if allowed).
- Export matches to CSV/Excel.
- Add scheduler + daily email/WhatsApp alerts.
- Build a small web UI for non-technical users.
