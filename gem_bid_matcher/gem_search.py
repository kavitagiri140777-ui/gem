from __future__ import annotations

from urllib.parse import urlencode

DEFAULT_GEM_ADVANCED_SEARCH_BASE = "https://mkp.gem.gov.in/search"


def build_advanced_search_url(
    base_url: str,
    keyword: str,
    location: str | None = None,
    category: str | None = None,
) -> str:
    """Build a GeM advanced-search URL with query parameters."""
    params = {"q": keyword}
    if location:
        params["location"] = location
    if category:
        params["category"] = category
    return f"{base_url}?{urlencode(params)}"


def build_keyword_search_urls(base_url: str, location: str, keywords: list[str]) -> list[str]:
    return [
        build_advanced_search_url(base_url, keyword=keyword, location=location)
        for keyword in keywords
    ]


def build_gem_advanced_search_urls(keywords: list[str], location: str | None = None) -> list[str]:
    """Create GeM portal advanced-search URLs for provided keywords."""
    urls: list[str] = []
    for keyword in keywords:
        urls.append(
            build_advanced_search_url(
                DEFAULT_GEM_ADVANCED_SEARCH_BASE,
                keyword=keyword,
                location=location,
            )
        )
    return urls
