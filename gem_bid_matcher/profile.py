from __future__ import annotations

from .models import MatchCriteria


def park_enterprises_profile() -> MatchCriteria:
    """Default profile tailored for Park Enterprises' GeM bid discovery."""
    return MatchCriteria(
        locations=["Visakhapatnam", "Vizag", "Andhra Pradesh"],
        required_skills=[
            "fabrication",
            "paneling",
            "wooden work",
            "stitching",
            "equipment cover",
            "safety nets",
            "safety posters",
            "acrylic boards",
        ],
        experience_keywords=[
            "Indian Navy",
            "naval",
            "dockyard",
            "defence",
            "defense",
            "ship",
            "marine",
        ],
        preferred_buyers=["Indian Navy", "Naval", "Defence", "Defense"],
        min_bid_value=0.0,
    )
