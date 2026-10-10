import os
import re
import time
from typing import List, Optional

import httpx

OPENALEX_API = "https://api.openalex.org/works"

ARXIV_URL_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?|[a-z\-]+(?:\.[A-Z]{2})?/[0-9]{7})",
    re.IGNORECASE,
)

SELECT_FIELDS = (
    "doi,display_name,publication_year,authorships,primary_location,"
    "locations,open_access,best_oa_location,abstract_inverted_index"
)


def _mailto() -> Optional[str]:
    return os.environ.get("CONTACT_EMAIL") or os.environ.get("OPENALEX_MAILTO")


def _get(params: dict) -> httpx.Response:
    last_error = None
    for attempt in range(4):
        resp = httpx.get(
            OPENALEX_API,
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
    raise RuntimeError("OpenAlex request failed")


def _abstract_from_inverted(idx: Optional[dict]) -> Optional[str]:
    if not idx:
        return None
    positions = {}
    for word, pos_list in idx.items():
        for p in pos_list:
            positions[p] = word
    return " ".join(positions[i] for i in sorted(positions)) if positions else None


def _arxiv_id_from_locations(work: dict) -> Optional[str]:
    for loc in work.get("locations") or []:
        for key in ("landing_page_url", "pdf_url"):
            url = loc.get(key) or ""
            m = ARXIV_URL_RE.search(url)
            if m:
                return m.group(1)
    return None


def _normalize_doi(doi: Optional[str]) -> Optional[str]:
    if not doi:
        return None
    doi = doi.strip().lower()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/)", "", doi)
    return doi or None


def _normalize(work: dict) -> dict:
    authorships = work.get("authorships") or []
    authors = [
        (a.get("author") or {}).get("display_name")
        for a in authorships
    ]
    authors = [a for a in authors if a]

    primary = work.get("primary_location") or {}
    source = primary.get("source") or {}
    venue = source.get("display_name")

    best_oa = work.get("best_oa_location") or {}
    open_access = (work.get("open_access") or {}).get("is_oa")

    return {
        "title": work.get("display_name") or "",
        "authors": authors,
        "year": work.get("publication_year"),
        "date": str(work.get("publication_year")) if work.get("publication_year") else None,
        "venue": venue,
        "doi": _normalize_doi(work.get("doi")),
        "arxiv_id": _arxiv_id_from_locations(work),
        "url": (work.get("doi") or (primary.get("landing_page_url") if primary else None)),
        "source": "openalex",
        "abstract": _abstract_from_inverted(work.get("abstract_inverted_index")),
        "open_access": bool(open_access or best_oa.get("pdf_url")),
        "pdf_url": best_oa.get("pdf_url"),
    }


def search_openalex(query: str, limit: int = 20, from_year: Optional[int] = None) -> List[dict]:
    params = {
        "search": query,
        "per-page": min(limit, 200),
        "select": SELECT_FIELDS,
    }
    if from_year:
        params["filter"] = f"from_publication_date:{from_year}-01-01"
    mailto = _mailto()
    if mailto:
        params["mailto"] = mailto
    resp = _get(params)
    resp.raise_for_status()
    works = resp.json().get("results", [])
    return [_normalize(w) for w in works]
