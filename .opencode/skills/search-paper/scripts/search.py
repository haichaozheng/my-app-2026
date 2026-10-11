import argparse
import difflib
import json
import re
import sys
import time
from typing import Iterable, List, Optional, Tuple, Union

from arxiv_client import search_arxiv
from common import load_env, normalize_doi
from crossref_client import search_crossref
from openalex_client import search_openalex
from serpapi_client import SerpApiKeyMissing, search_serpapi
from s2_client import search_s2

# Load .env (S2_API_KEY / Serp_API_KEY / CONTACT_EMAIL) exactly once, before
# any client reads os.environ. Clients no longer load_dotenv themselves.
load_env()

ALL_SOURCES = ["arxiv", "crossref", "s2", "openalex", "scholar"]

# Polite request interval (seconds) between consecutive queries to the same
# source. arXiv asks for >=3s between requests; anonymous S2 has a tiny
# per-IP budget, so we pace it too. OpenAlex/CrossRef are generous. SerpAPI
# is a paid aggregator with no per-request courtesy budget, 1s is enough.
QUERY_INTERVAL = {"arxiv": 3.0, "s2": 1.5, "crossref": 0.2, "openalex": 0.2, "scholar": 1.0}

RATE_LIMIT_HINT = (
    "rate limited (匿名额度低). 其他来源不受影响；S2 与 OpenAlex 覆盖大量重叠，"
    "结果完整性基本不受损。免费申请 Key: https://www.semanticscholar.org/product/api#api-key-form"
)

SCHOLAR_QUOTA_HINT = (
    "rate limited (SerpAPI 限流或额度用尽). 其他来源不受影响。免费计划约 100 次/月，"
    "同参数 1 小时内命中缓存不计费；查看额度: https://serpapi.com/manage-api-key"
)

DEGRADED_HINTS = {"s2": RATE_LIMIT_HINT, "scholar": SCHOLAR_QUOTA_HINT}

# Fields used to fill gaps when merging duplicate records across sources.
# cited_by comes from Google Scholar only and is merged into records from
# other sources when titles match.
MERGE_FIELDS = ("doi", "arxiv_id", "year", "date", "venue", "abstract", "pdf_url", "url", "open_access", "authors", "cited_by")

FUZZY_TITLE_THRESHOLD = 0.95
FUZZY_YEAR_TOLERANCE = 1  # arXiv preprint vs. published version may differ by a year


def _norm_title(title: str) -> str:
    t = (title or "").lower()
    t = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", t)
    return " ".join(t.split())


def _norm_doi(doi: str) -> str:
    return normalize_doi(doi) or ""


def _norm_arxiv(arxiv_id: str) -> str:
    aid = (arxiv_id or "").strip().lower()
    aid = re.sub(r"v\d+$", "", aid)
    return aid


def _titles_similar(a: str, b: str) -> bool:
    if not a or not b:
        return False
    if a == b:
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= FUZZY_TITLE_THRESHOLD


def _years_compatible(a: Optional[int], b: Optional[int]) -> bool:
    if a is None or b is None:
        return True
    return abs(a - b) <= FUZZY_YEAR_TOLERANCE


def _find_duplicate(rec: dict, out: List[dict]) -> Optional[int]:
    doi = _norm_doi(rec.get("doi") or "")
    arxiv_id = _norm_arxiv(rec.get("arxiv_id") or "")
    title = _norm_title(rec.get("title") or "")
    for i, prev in enumerate(out):
        if doi and _norm_doi(prev.get("doi") or "") == doi:
            return i
        if arxiv_id and _norm_arxiv(prev.get("arxiv_id") or "") == arxiv_id:
            return i
    # Title match is a weaker signal: only merge after identifier checks fail.
    for i, prev in enumerate(out):
        prev_title = _norm_title(prev.get("title") or "")
        if title and prev_title and _titles_similar(title, prev_title):
            if _years_compatible(rec.get("year"), prev.get("year")):
                return i
    return None


def dedupe(records: Iterable[dict]) -> List[dict]:
    """Merge duplicate records.

    - First occurrence becomes the base record.
    - Identifier matches (DOI / arXiv ID) merge unconditionally.
    - Near-identical titles (ratio >= 0.95) merge only when years are compatible.
    - Merged records keep: union of sources, best (lowest) rank, and the first
      non-empty value of each metadata field.
    """
    out: List[dict] = []
    for rec in records:
        idx = _find_duplicate(rec, out)
        if idx is None:
            merged = dict(rec)
            merged["matched_sources"] = [rec.get("source")]
            merged["best_rank"] = rec.get("rank", 999)
            out.append(merged)
            continue
        prev = out[idx]
        if rec.get("source") and rec.get("source") not in prev["matched_sources"]:
            prev["matched_sources"].append(rec.get("source"))
        prev["best_rank"] = min(prev.get("best_rank", 999), rec.get("rank", 999))
        for key in MERGE_FIELDS:
            if prev.get(key) in (None, "", [], False) and rec.get(key) not in (None, "", [], False):
                prev[key] = rec[key]
    return out


def _status_code(exc: Exception) -> Optional[int]:
    resp = getattr(exc, "response", None)
    return getattr(resp, "status_code", None)


def search(
    query: Union[str, List[str]],
    limit: int = 20,
    from_year: Optional[int] = None,
    sources: Optional[List[str]] = None,
) -> dict:
    """Search all sources.

    ``query`` may be a single string or a list of query variants (e.g. an
    acronym and its expansion). Each source is searched with each variant,
    and results are pooled, deduped and ranked by best in-source rank.

    Rate-limited queries (HTTP 429, typical for anonymous Semantic Scholar)
    are retried once after all other requests finish — by then the rate-limit
    window has often reset — and only reported in ``degraded`` (informational)
    instead of ``errors`` if they still fail.

    Google Scholar via SerpAPI is billed per search: it only searches the
    first query variant (same-parameter repeats within 1h hit SerpAPI's cache
    for free) and degrades into ``degraded`` instead of failing the search
    when the key is missing or the quota is exhausted.
    """
    queries = [query] if isinstance(query, str) else list(query)
    queries = [q for q in queries if q and q.strip()]
    if not queries:
        raise ValueError("At least one non-empty query is required")

    sources = sources or ALL_SOURCES
    unknown = [s for s in sources if s not in ALL_SOURCES]
    if unknown:
        raise ValueError(f"Unknown sources: {unknown}. Valid: {ALL_SOURCES}")

    client_map = {
        "arxiv": lambda q, limit, from_year: search_arxiv(q, max_results=limit, from_year=from_year),
        "crossref": lambda q, limit, from_year: search_crossref(q, rows=limit, from_year=from_year),
        "s2": search_s2,
        "openalex": search_openalex,
        "scholar": search_serpapi,
    }

    def run_one(source: str, q: str) -> List[dict]:
        client = client_map[source]
        found = client(q, limit=limit, from_year=from_year)
        for rank, rec in enumerate(found):
            rec["rank"] = rank
        return found

    errors = {}
    degraded = {}
    pending_retry: List[Tuple[str, str]] = []
    pooled = []
    for source in sources:
        interval = QUERY_INTERVAL.get(source, 0)
        for qi, q in enumerate(queries):
            if source == "scholar" and qi > 0:
                # SerpAPI charges per search (same-parameter repeats within
                # 1h hit their cache for free), so the scholar source only
                # fans out the first query variant.
                break
            if qi > 0 and interval:
                time.sleep(interval)
            try:
                pooled.extend(run_one(source, q))
            except SerpApiKeyMissing as exc:
                # Informational, mirrors anonymous-S2 degradation: the whole
                # search still succeeds with the other sources.
                degraded["scholar"] = str(exc)
                break
            except Exception as exc:
                if _status_code(exc) == 429:
                    pending_retry.append((source, q))
                else:
                    key = f"{source}" if len(queries) == 1 else f"{source} [query: {q[:50]}]"
                    errors[key] = str(exc)

    # Deferred retry for rate-limited queries: other sources have taken a few
    # seconds by now, so the anonymous budget may have recovered.
    for source, q in pending_retry:
        try:
            time.sleep(2)
            pooled.extend(run_one(source, q))
        except Exception as exc:
            key = f"{source}" if len(queries) == 1 else f"{source} [query: {q[:50]}]"
            degraded[key] = DEGRADED_HINTS.get(source, str(exc))

    records = dedupe(pooled)
    records.sort(key=lambda r: (r.get("best_rank", 999), -(r.get("year") or 0)))
    result = {
        "queries": queries,
        "from_year": from_year,
        "sources": sources,
        "n_raw": len(pooled),
        "n": len(records),
        "errors": errors,
        "records": records,
    }
    if degraded:
        result["degraded"] = degraded
    return result


def main():
    # Windows consoles often default to GBK; force UTF-8 so records with
    # non-ASCII author names/abstracts don't crash json.dump.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Search papers from arXiv, CrossRef, Semantic Scholar, OpenAlex, Google Scholar (SerpAPI)")
    parser.add_argument(
        "--query",
        action="append",
        required=True,
        help="检索词或布尔式；可重复传入多个变体（如缩写 + 全称）以提高覆盖",
    )
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--from-year", type=int, default=None)
    parser.add_argument(
        "--sources",
        default="arxiv,crossref,s2,openalex,scholar",
        help="逗号分隔的来源列表，默认全部。scholar 经 SerpAPI 按次计费（多变体只扇出第一个）且需要 .env 中的 Serp_API_KEY；不想要就把它从列表里去掉",
    )
    args = parser.parse_args()
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    result = search(args.query, limit=args.limit, from_year=args.from_year, sources=sources)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
