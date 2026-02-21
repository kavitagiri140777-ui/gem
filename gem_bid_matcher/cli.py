from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .gem_search import build_gem_advanced_search_urls, build_keyword_search_urls
from .matcher import rank_bids
from .models import MatchCriteria
from .profile import park_enterprises_profile
from .scraper import scrape_bids_from_file, scrape_bids_from_url, scrape_bids_from_urls


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GeM bid scraper + matcher")
    source = parser.add_mutually_exclusive_group(required=False)
    source.add_argument("--source-url", help="Bid listing URL")
    source.add_argument("--source-file", help="Path to saved HTML page")

    parser.add_argument("--gem-advanced-search", action="store_true", help="Fetch from GeM advanced-search URLs built from keywords")
    parser.add_argument("--location", action="append", default=[], help="Preferred location")
    parser.add_argument("--skill", action="append", default=[], help="Skill/category keyword")
    parser.add_argument("--experience", action="append", default=[], help="Experience keyword")
    parser.add_argument("--buyer", action="append", default=[], help="Preferred buyer/department")
    parser.add_argument("--min-value", type=float, default=0.0, help="Minimum bid value")
    parser.add_argument("--limit", type=int, default=20, help="Maximum results")
    parser.add_argument("--use-park-profile", action="store_true", help="Use built-in Park Enterprises profile (Vizag + Navy + requested keywords)")
    parser.add_argument("--print-search-urls", help="Print generated advanced search URLs for a base search page URL")
    return parser


def _merge_criteria(args: argparse.Namespace) -> MatchCriteria:
    profile = park_enterprises_profile() if args.use_park_profile else MatchCriteria()
    return MatchCriteria(
        locations=[*profile.locations, *args.location],
        required_skills=[*profile.required_skills, *args.skill],
        experience_keywords=[*profile.experience_keywords, *args.experience],
        preferred_buyers=[*profile.preferred_buyers, *args.buyer],
        min_bid_value=max(profile.min_bid_value, args.min_value),
    )


def _load_bids(args: argparse.Namespace, criteria: MatchCriteria):
    if args.source_url:
        return scrape_bids_from_url(args.source_url), []
    if args.source_file:
        return scrape_bids_from_file(args.source_file), []
    if args.gem_advanced_search:
        location = criteria.locations[0] if criteria.locations else None
        search_urls = build_gem_advanced_search_urls(criteria.required_skills, location=location)
        return scrape_bids_from_urls(search_urls), search_urls
    raise SystemExit("Provide one source: --source-url, --source-file, or --gem-advanced-search")


def main() -> None:
    args = build_parser().parse_args()
    criteria = _merge_criteria(args)
    bids, gem_urls = _load_bids(args, criteria)
    ranked = rank_bids(bids, criteria)

    payload = []
    for item in ranked[: args.limit]:
        bid_dict = asdict(item.bid)
        if item.bid.end_date is not None:
            bid_dict["end_date"] = item.bid.end_date.isoformat()
        payload.append({"score": item.score, "match_reasons": item.reasons, **bid_dict})

    output = {"criteria": asdict(criteria), "matches": payload}

    if args.print_search_urls:
        output["suggested_search_urls"] = build_keyword_search_urls(
            base_url=args.print_search_urls,
            location=(criteria.locations[0] if criteria.locations else "Visakhapatnam"),
            keywords=criteria.required_skills,
        )
    if gem_urls:
        output["gem_advanced_search_urls"] = gem_urls

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
