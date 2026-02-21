from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Bid:
    title: str
    bid_number: str = ""
    department: str = ""
    location: str = ""
    category: str = ""
    bid_value: float = 0.0
    end_date: datetime | None = None
    url: str = ""
    raw_text: str = ""


@dataclass
class MatchCriteria:
    locations: list[str] = field(default_factory=list)
    required_skills: list[str] = field(default_factory=list)
    experience_keywords: list[str] = field(default_factory=list)
    preferred_buyers: list[str] = field(default_factory=list)
    min_bid_value: float = 0.0


@dataclass
class RankedBid:
    bid: Bid
    score: float
    reasons: list[str] = field(default_factory=list)
