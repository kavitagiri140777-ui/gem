from __future__ import annotations

from datetime import datetime
from html.parser import HTMLParser
import re
from urllib.request import urlopen

from .models import Bid


BID_NUMBER_PATTERN = re.compile(r"\b(?:GEM/\d{4}/B/\d+|BID[-\s:]?\d{4,})\b", re.IGNORECASE)


def fetch_listing_html(url: str, timeout_s: int = 25) -> str:
    with urlopen(url, timeout=timeout_s) as response:
        return response.read().decode("utf-8", errors="ignore")


def parse_money(value: str) -> float:
    cleaned = re.sub(r"[^0-9.]", "", value or "")
    if not cleaned:
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def parse_date(value: str) -> datetime | None:
    value = (value or "").strip()
    if not value:
        return None

    patterns = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d %b %Y", "%d %B %Y"]
    for p in patterns:
        try:
            return datetime.strptime(value, p)
        except ValueError:
            continue
    return None


def extract_bid_number(*parts: str) -> str:
    for part in parts:
        match = BID_NUMBER_PATTERN.search(part or "")
        if match:
            return match.group(0)
    return ""


class _SimpleTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_tr = False
        self.in_cell = False
        self.current_cell_data: list[str] = []
        self.current_row: list[str] = []
        self.rows: list[list[str]] = []
        self.row_first_href: str = ""
        self.row_hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "tr":
            self.in_tr = True
            self.current_row = []
            self.row_first_href = ""
        elif self.in_tr and tag in {"td", "th"}:
            self.in_cell = True
            self.current_cell_data = []
        elif self.in_tr and tag == "a":
            href = (attrs_dict.get("href") or "").strip()
            if not self.row_first_href and href:
                self.row_first_href = href

    def handle_endtag(self, tag: str) -> None:
        if self.in_tr and tag in {"td", "th"} and self.in_cell:
            text = "".join(self.current_cell_data).strip()
            self.current_row.append(re.sub(r"\s+", " ", text))
            self.current_cell_data = []
            self.in_cell = False
        elif tag == "tr" and self.in_tr:
            if self.current_row:
                self.rows.append(self.current_row)
                self.row_hrefs.append(self.row_first_href)
            self.in_tr = False
            self.current_row = []
            self.row_first_href = ""

    def handle_data(self, data: str) -> None:
        if self.in_tr and self.in_cell:
            self.current_cell_data.append(data)


def _cell_text(cells: list[str], idx: int) -> str:
    return cells[idx] if idx < len(cells) else ""


def parse_bids_from_html(html: str) -> list[Bid]:
    parser = _SimpleTableParser()
    parser.feed(html)

    bids: list[Bid] = []
    for i, cells in enumerate(parser.rows):
        if len(cells) < 3:
            continue

        title = _cell_text(cells, 0)
        if not title or "title" in title.lower():
            continue

        raw_text = " ".join(cells)
        bid_number = extract_bid_number(_cell_text(cells, 0), _cell_text(cells, 1), raw_text)

        bids.append(
            Bid(
                title=title,
                bid_number=bid_number,
                department=_cell_text(cells, 1),
                location=_cell_text(cells, 2),
                category=_cell_text(cells, 3),
                bid_value=parse_money(_cell_text(cells, 4)),
                end_date=parse_date(_cell_text(cells, 5)),
                url=parser.row_hrefs[i] if i < len(parser.row_hrefs) else "",
                raw_text=raw_text,
            )
        )

    return bids


def scrape_bids_from_url(url: str) -> list[Bid]:
    return parse_bids_from_html(fetch_listing_html(url))


def scrape_bids_from_urls(urls: list[str]) -> list[Bid]:
    all_bids: list[Bid] = []
    for url in urls:
        try:
            all_bids.extend(scrape_bids_from_url(url))
        except Exception:
            continue

    seen: set[str] = set()
    unique: list[Bid] = []
    for bid in all_bids:
        key = f"{bid.bid_number}|{bid.title}|{bid.department}|{bid.location}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(bid)
    return unique


def scrape_bids_from_file(path: str) -> list[Bid]:
    with open(path, "r", encoding="utf-8") as f:
        return parse_bids_from_html(f.read())
