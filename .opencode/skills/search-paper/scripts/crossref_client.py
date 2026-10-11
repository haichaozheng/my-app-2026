import html
import os
import re
import time
from typing import List, Optional

import httpx

from common import normalize_doi

CROSSREF_API = "https://api.crossref.org/works"


def _mailto() -> Optional[str]:
    return os.environ.get("CONTACT_EMAIL") or os.environ.get("CROSSREF_MAILTO")


def _get(params: dict) -> httpx.Response:
    last_error = None
    for attempt in range(3):
        try:
            resp = httpx.get(
                CROSSREF_API,
                params=params,
                timeout=30,
                follow_redirects=True,
                headers={"User-Agent": "search-paper-skill/1.1 (teaching; contact via repo)"},
            )
        except httpx.TransportError as exc:
            # Connection / timeout failures are worth retrying, not just 5xx.
            last_error = exc
            time.sleep(2 ** attempt)
            continue
        if resp.status_code not in (429, 500, 502, 503):
            return resp
        last_error = resp
        time.sleep(float(resp.headers.get("Retry-After", 2 ** attempt)))
    if isinstance(last_error, Exception):
        raise last_error
    if last_error is not None:
        last_error.raise_for_status()
    raise RuntimeError("CrossRef request failed")


def _year_from_item(item: dict) -> Optional[int]:
    for key in ("published-print", "published-online", "issued"):
        parts = (item.get(key) or {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            return int(parts[0][0])
    return None


def _is_oa(item: dict) -> bool:
    # CrossRef's `link` field appears for most records (text-and-data-mining
    # links) and does not imply open access. Only a CC / public-domain license
    # is a reliable OA signal; OpenAlex's `is_oa` fills the gap at merge time.
    for lic in item.get("license") or []:
        url = (lic.get("URL") or "").lower()
        if "creativecommons" in url or "publicdomain" in url:
            return True
    return False


def _normalize(item: dict) -> dict:
    abstract = item.get("abstract") or ""
    if abstract:
        abstract = re.sub(r"<[^>]+>", "", abstract)
        abstract = html.unescape(abstract)
        abstract = " ".join(abstract.split())

    title = " ".join(item.get("title") or [])
    if title:
        # CrossRef titles may carry double-escaped HTML entities
        # ("Simulation&amp;nbsp;") which would pollute display and
        # title-based dedupe matching.
        title = re.sub(r"<[^>]+>", "", title)
        title = html.unescape(html.unescape(title))
        title = title.replace("\xa0", " ").strip()

    authors = []
    for a in item.get("author", []) or []:
        given = a.get("given", "")
        family = a.get("family", "")
        name = f"{given} {family}".strip()
        if name:
            authors.append(name)

    venue = ""
    ct = item.get("container-title") or []
    if ct:
        venue = ct[0]

    year = _year_from_item(item)
    doi = normalize_doi(item.get("DOI"))

    return {
        "title": title,
        "authors": authors,
        "year": year,
        "date": str(year) if year else None,
        "venue": venue or None,
        "doi": doi,
        "arxiv_id": None,
        "url": f"https://doi.org/{doi}" if doi else None,
        "source": "crossref",
        "abstract": abstract or None,
        "open_access": _is_oa(item),
        "pdf_url": None,
    }


def search_crossref(query: str, rows: int = 20, from_year: Optional[int] = None) -> List[dict]:
    # query.bibliographic restricts matching to title/author/venue-level fields,
    # which is far more precise than the catch-all `query` parameter.
    params = {
        "query.bibliographic": query,
        "rows": rows,
        "select": "DOI,title,author,published-print,published-online,issued,container-title,abstract,license",
    }
    if from_year:
        params["filter"] = f"from-pub-date:{from_year}-01-01"
    mailto = _mailto()
    if mailto:
        params["mailto"] = mailto
    resp = _get(params)
    resp.raise_for_status()
    items = resp.json().get("message", {}).get("items", [])
    return [_normalize(item) for item in items]
