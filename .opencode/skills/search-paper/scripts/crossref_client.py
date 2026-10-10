import os
import re
import time
from typing import List, Optional

import httpx

CROSSREF_API = "https://api.crossref.org/works"


def _mailto() -> Optional[str]:
    return os.environ.get("CONTACT_EMAIL") or os.environ.get("CROSSREF_MAILTO")


def _get(params: dict) -> httpx.Response:
    last_error = None
    for attempt in range(3):
        resp = httpx.get(
            CROSSREF_API,
            params=params,
            timeout=30,
            follow_redirects=True,
            headers={"User-Agent": "search-paper-skill/1.1 (teaching; contact via repo)"},
        )
        if resp.status_code not in (429, 500, 502, 503):
            return resp
        last_error = resp
        time.sleep(float(resp.headers.get("Retry-After", 2 ** attempt)))
    if last_error is not None:
        last_error.raise_for_status()
    raise RuntimeError("CrossRef request failed")


def _year_from_item(item: dict) -> Optional[int]:
    for key in ("published-print", "published-online", "issued"):
        parts = (item.get(key) or {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            return int(parts[0][0])
    return None


def _normalize_doi(doi: Optional[str]) -> Optional[str]:
    if not doi:
        return None
    doi = doi.strip().lower()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/)", "", doi)
    return doi or None


def _normalize(item: dict) -> dict:
    abstract = item.get("abstract") or ""
    if abstract:
        abstract = re.sub(r"<[^>]+>", "", abstract)
        abstract = " ".join(abstract.split())

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
    doi = _normalize_doi(item.get("DOI"))
    license_ok = bool(item.get("license"))
    oa = bool((item.get("link") or [])) or license_ok

    return {
        "title": " ".join(item.get("title") or []),
        "authors": authors,
        "year": year,
        "date": str(year) if year else None,
        "venue": venue or None,
        "doi": doi,
        "arxiv_id": None,
        "url": f"https://doi.org/{doi}" if doi else None,
        "source": "crossref",
        "abstract": abstract or None,
        "open_access": oa,
        "pdf_url": None,
    }


def search_crossref(query: str, rows: int = 20, from_year: Optional[int] = None) -> List[dict]:
    # query.bibliographic restricts matching to title/author/venue-level fields,
    # which is far more precise than the catch-all `query` parameter.
    params = {
        "query.bibliographic": query,
        "rows": rows,
        "select": "DOI,title,author,published-print,published-online,issued,container-title,abstract,URL,license,link",
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
