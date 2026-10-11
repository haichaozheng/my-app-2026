import os
import time
from typing import List, Optional

import httpx

# .env is loaded centrally by search.py via common.load_env(); keys are read
# from os.environ at call time.

S2_API = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "title,authors,year,venue,externalIds,url,abstract,openAccessPdf,isOpenAccess"


def _get(params: dict, headers: dict) -> httpx.Response:
    last_error = None
    for attempt in range(4):
        try:
            resp = httpx.get(S2_API, params=params, headers=headers, timeout=30, follow_redirects=True)
        except httpx.TransportError as exc:
            # Connection / timeout failures are worth retrying, not just 429.
            last_error = exc
            time.sleep(2 ** attempt)
            continue
        if resp.status_code != 429:
            return resp
        last_error = resp
        wait = float(resp.headers.get("Retry-After", 2 ** attempt))
        time.sleep(wait)
    if isinstance(last_error, Exception):
        raise last_error
    if last_error is not None:
        last_error.raise_for_status()
    raise RuntimeError("Semantic Scholar request failed")


def search_s2(query: str, limit: int = 20, from_year: Optional[int] = None) -> List[dict]:
    headers = {}
    api_key = os.environ.get("S2_API_KEY", "")
    if api_key:
        headers["x-api-key"] = api_key

    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": FIELDS,
    }
    if from_year:
        params["year"] = f"{from_year}-"

    resp = _get(params, headers)
    resp.raise_for_status()
    papers = resp.json().get("data") or []
    records = []
    for p in papers:
        ext = p.get("externalIds") or {}
        authors = [a.get("name") for a in (p.get("authors") or []) if a.get("name")]
        pdf = (p.get("openAccessPdf") or {})
        records.append({
            "title": p.get("title") or "",
            "authors": authors,
            "year": p.get("year"),
            "date": str(p.get("year")) if p.get("year") else None,
            "venue": p.get("venue") or None,
            "doi": ext.get("DOI"),
            "arxiv_id": ext.get("ArXiv"),
            "url": p.get("url"),
            "source": "s2",
            "abstract": p.get("abstract"),
            "open_access": bool(p.get("isOpenAccess") or pdf.get("url")),
            "pdf_url": pdf.get("url"),
        })
    return records
