from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .matcher import rank_bids
from .models import MatchCriteria
from .scraper import scrape_bids_from_file, scrape_bids_from_url


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GeM bid scraper + matcher")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--source-url", help="Bid listing URL")
    source.add_argument("--source-file", help="Path to saved HTML page")

    parser.add_argument("--location", action="append", default=[], help="Preferred location")
    parser.add_argument("--skill", action="append", default=[], help="Skill/category keyword")
    parser.add_argument(
        "--experience", action="append", default=[], help="Experience keyword"
    )
    parser.add_argument("--min-value", type=float, default=0.0, help="Minimum bid value")
    parser.add_argument("--limit", type=int, default=20, help="Maximum results")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    bids = (
        scrape_bids_from_url(args.source_url)
        if args.source_url
        else scrape_bids_from_file(args.source_file)
    )

    criteria = MatchCriteria(
        locations=args.location,
        required_skills=args.skill,
        experience_keywords=args.experience,
        min_bid_value=args.min_value,
    )

    ranked = rank_bids(bids, criteria)

    payload = []
    for item in ranked[: args.limit]:
        bid_dict = asdict(item.bid)
        if item.bid.end_date is not None:
            bid_dict["end_date"] = item.bid.end_date.isoformat()

        payload.append(
            {
                "score": item.score,
                "match_reasons": item.reasons,
                **bid_dict,
            }
        )

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
