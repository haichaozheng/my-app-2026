import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional

import httpx

ARXIV_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

BOOLEAN_OPS = {"AND", "OR", "ANDNOT"}


def _tokenize(query: str) -> List[str]:
    """Split a query into tokens, keeping double-quoted phrases intact."""
    return re.findall(r'"[^"]*"|[^\s]+', query.strip())


def build_search_query(query: str, from_year: Optional[int] = None) -> str:
    """Build an arXiv search_query string.

    Rules:
    - Every bare token is fielded as ``all:<token>`` (AND semantics by default).
    - Quoted phrases become ``all:"<phrase>"`` for exact-phrase matching.
    - Explicit boolean operators (AND / OR / ANDNOT) are passed through.
    - ``from_year`` pushes a server-side ``submittedDate`` range into the query
      so year filtering happens before pagination, not after (avoids losing
      results that fall outside the fetched page).
    """
    parts = []
    for tok in _tokenize(query):
        if tok.upper() in BOOLEAN_OPS:
            parts.append(tok.upper())
        else:
            parts.append(f"all:{tok}")
    core = " ".join(parts)
    if from_year:
        now = datetime.now().strftime("%Y%m%d%H%M")
        core = f"({core}) AND submittedDate:[{from_year}01010000 TO {now}]"
    return core


def _entry_to_record(e) -> dict:
    title_el = e.find("atom:title", ARXIV_NS)
    summary_el = e.find("atom:summary", ARXIV_NS)
    published_el = e.find("atom:published", ARXIV_NS)
    id_el = e.find("atom:id", ARXIV_NS)
    doi_el = e.find("arxiv:doi", ARXIV_NS)
    pdf_el = None
    for link in e.findall("atom:link", ARXIV_NS):
        if link.get("title") == "pdf" or link.get("type") == "application/pdf":
            pdf_el = link
            break

    arxiv_id = ""
    if id_el is not None and id_el.text:
        arxiv_id = id_el.text.rsplit("/", 1)[-1]
    date = published_el.text[:10] if published_el is not None and published_el.text else None
    year = int(date[:4]) if date else None

    return {
        "title": " ".join((title_el.text or "").split()) if title_el is not None else "",
        "authors": [
            a.find("atom:name", ARXIV_NS).text
            for a in e.findall("atom:author", ARXIV_NS)
            if a.find("atom:name", ARXIV_NS) is not None
        ],
        "year": year,
        "date": date,
        "venue": "arXiv",
        "doi": doi_el.text if doi_el is not None else None,
        "arxiv_id": arxiv_id,
        "url": f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None,
        "source": "arxiv",
        "abstract": " ".join((summary_el.text or "").split()) if summary_el is not None else None,
        "open_access": True,
        "pdf_url": pdf_el.get("href") if pdf_el is not None else (
            f"https://arxiv.org/pdf/{arxiv_id}" if arxiv_id else None
        ),
    }


ARXIV_API = "http://export.arxiv.org/api/query"


def _get(params: dict) -> httpx.Response:
    last_error = None
    for _ in range(3):
        try:
            resp = httpx.get(
                ARXIV_API,
                params=params,
                timeout=30,
                follow_redirects=True,
                headers={"User-Agent": "search-paper-skill/1.1 (teaching; contact via repo)"},
            )
        except httpx.TransportError as exc:
            # Connection / timeout failures are worth retrying, not just 5xx.
            last_error = exc
            time.sleep(3)  # arXiv asks for >=3s between retries
            continue
        if resp.status_code == 200:
            return resp
        if resp.status_code in (429, 500, 502, 503):
            last_error = resp
            time.sleep(3)
            continue
        # Other 4xx (e.g. a malformed search_query) won't improve on retry:
        # return it and let raise_for_status report the bad request.
        return resp
    if isinstance(last_error, Exception):
        raise last_error
    if last_error is not None:
        last_error.raise_for_status()
    raise RuntimeError("arXiv request failed")


def search_arxiv(query: str, max_results: int = 20, from_year: Optional[int] = None) -> List[dict]:
    search_query = build_search_query(query, from_year=from_year)
    resp = _get(
        {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
    )
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    return [_entry_to_record(e) for e in root.findall("atom:entry", ARXIV_NS)]
