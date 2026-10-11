import os
import re
import time
from typing import List, Optional, Tuple

import httpx

# .env is loaded centrally by search.py via common.load_env(); the key is read
# from os.environ at call time.

SERPAPI_API = "https://serpapi.com/search.json"

# publication_info.summary looks like "ZH Zhou, B Author - 2021 - books.google.com"
# or "Nature 566, 190-194, 2019". Year is the first 19xx/20xx token.
YEAR_RE = re.compile(r"\b((?:19|20)\d{2})\b")
DOI_RE = re.compile(r"doi\.org/(10\.\d{4,9}/[^\s&#?]+)", re.IGNORECASE)

SERPAPI_KEY_HINT = (
    "未配置 Serp_API_KEY，已跳过 Google Scholar 源（其余来源不受影响）。"
    "SerpAPI 免费注册: https://serpapi.com/manage-api-key （约 100 次/月，"
    "同参数 1 小时内命中缓存不计费）。申请后把 Key 写入仓库根目录 .env 的 "
    "Serp_API_KEY=...，不要提交到 git。"
)


class SerpApiKeyMissing(RuntimeError):
    """No SerpAPI key configured. Informational: the caller should skip the
    scholar source (degraded) instead of failing the whole search."""


def _api_key() -> str:
    # Canonical name is SERPAPI_KEY; this repo's .env uses Serp_API_KEY.
    return (
        os.environ.get("Serp_API_KEY")
        or os.environ.get("SERPAPI_KEY")
        or ""
    )


def _get(params: dict) -> httpx.Response:
    last_error = None
    for attempt in range(3):
        try:
            resp = httpx.get(SERPAPI_API, params=params, timeout=60, follow_redirects=True)
        except httpx.TransportError as exc:
            # Connection / timeout failures are worth retrying, not just 5xx.
            last_error = exc
            time.sleep(2 ** attempt)
            continue
        if resp.status_code in (401, 403):
            # Invalid key or exhausted plan: retrying won't help.
            raise RuntimeError(
                f"SerpAPI 拒绝了请求 (HTTP {resp.status_code})：请检查 .env 中的 "
                f"Serp_API_KEY 是否有效、计划额度是否用尽。"
            )
        if resp.status_code not in (429, 500, 502, 503):
            return resp
        last_error = resp
        time.sleep(float(resp.headers.get("Retry-After", 2 ** attempt)))
    if isinstance(last_error, Exception):
        raise last_error
    if last_error is not None:
        last_error.raise_for_status()
    raise RuntimeError("SerpAPI request failed")


def _parse_summary(summary: Optional[str]) -> Tuple[Optional[int], Optional[str], Optional[List[str]]]:
    """Parse GS summary like "ZH Zhou, B Author - 2021 - books.google.com".

    Returns (year, venue, fallback_authors). Author and venue parts are absent
    in summaries like "Nature 566, 190-194, 2019".
    """
    if not summary:
        return None, None, None
    parts = [p.strip() for p in summary.split(" - ") if p.strip()]
    year = None
    venue = None
    authors = None
    for i, part in enumerate(parts):
        m = YEAR_RE.search(part)
        if m:
            year = int(m.group(1))
            if i + 1 < len(parts):
                venue = parts[i + 1]
            if i > 0:
                authors = [a.strip() for a in parts[0].split(",") if a.strip()]
            break
    if year is None:
        m = YEAR_RE.search(summary)
        if m:
            year = int(m.group(1))
    # GS puts a host (books.google.com, arxiv.org) in the venue slot; real
    # venues are prose like "Nature 566, 190-194". Drop domain-looking values.
    if venue and " " not in venue and "." in venue:
        venue = None
    return year, venue, authors


def _find_doi(urls: List[Optional[str]]) -> Optional[str]:
    for url in urls:
        if not url:
            continue
        m = DOI_RE.search(url)
        if m:
            return m.group(1)
    return None


def _normalize(result: dict) -> dict:
    pub = result.get("publication_info") or {}
    year, venue, fallback_authors = _parse_summary(pub.get("summary"))
    authors = [a.get("name") for a in (pub.get("authors") or []) if a.get("name")]
    if not authors and fallback_authors:
        authors = fallback_authors

    link = result.get("link")
    resources = result.get("resources") or []
    resource_links = [r.get("link") for r in resources]
    doi = _find_doi([link] + resource_links)

    # resources[] are the [PDF] direct links shown inline on GS.
    pdf_url = next((u for u in resource_links if u), None)

    inline = result.get("inline_links") or {}
    cited_by = (inline.get("cited_by") or {}).get("total")

    return {
        "title": result.get("title") or "",
        "authors": authors,
        "year": year,
        "date": str(year) if year else None,
        "venue": venue,
        "doi": doi,
        "arxiv_id": None,
        "url": link,
        "source": "scholar",
        # GS snippets are fragments ("… from data is called learning…"), not
        # abstracts: leave empty so dedupe fills it from other sources.
        "abstract": None,
        "open_access": bool(pdf_url),
        "pdf_url": pdf_url,
        "cited_by": cited_by,
    }


def search_serpapi(query: str, limit: int = 20, from_year: Optional[int] = None) -> List[dict]:
    api_key = _api_key()
    if not api_key:
        raise SerpApiKeyMissing(SERPAPI_KEY_HINT)

    params = {
        "engine": "google_scholar",
        "q": query,
        "num": min(limit, 20),  # Google Scholar hard cap
        "hl": "en",
        "api_key": api_key,
    }
    if from_year:
        params["as_ylo"] = from_year

    resp = _get(params)
    resp.raise_for_status()
    results = resp.json().get("organic_results") or []
    return [_normalize(r) for r in results]
