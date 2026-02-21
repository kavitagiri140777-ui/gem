from __future__ import annotations

from .models import Bid, MatchCriteria, RankedBid


def _contains_any(text: str, keywords: list[str]) -> list[str]:
    lowered = text.lower()
    return [k for k in keywords if k and k.lower() in lowered]


def rank_bids(bids: list[Bid], criteria: MatchCriteria) -> list[RankedBid]:
    ranked: list[RankedBid] = []

    for bid in bids:
        reasons: list[str] = []
        score = 0.0

        searchable = " ".join(
            [bid.title, bid.department, bid.location, bid.category, bid.raw_text]
        )

        if bid.bid_value < criteria.min_bid_value:
            continue

        if criteria.locations:
            matches = _contains_any(bid.location, criteria.locations)
            if matches:
                score += 20
                reasons.append(f"location_match:{', '.join(matches)}")

        if criteria.required_skills:
            matches = _contains_any(searchable, criteria.required_skills)
            if matches:
                score += min(40, 10 * len(matches))
                reasons.append(f"skill_match:{', '.join(matches)}")

        if criteria.experience_keywords:
            matches = _contains_any(searchable, criteria.experience_keywords)
            if matches:
                score += min(25, 5 * len(matches))
                reasons.append(f"experience_match:{', '.join(matches)}")

        if criteria.preferred_buyers:
            matches = _contains_any(bid.department, criteria.preferred_buyers)
            if matches:
                score += 20
                reasons.append(f"buyer_match:{', '.join(matches)}")

        if score > 0:
            ranked.append(RankedBid(bid=bid, score=score, reasons=reasons))

    return sorted(ranked, key=lambda b: b.score, reverse=True)
