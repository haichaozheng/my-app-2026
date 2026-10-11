"""Shared helpers for the search-paper clients.

Keep this module free of third-party dependencies so every client can import
it unconditionally; ``httpx`` stays in the clients, ``python-dotenv`` is
optional.
"""

import re
from typing import Optional

DOI_URL_PREFIX = re.compile(r"^(https?://(dx\.)?doi\.org/)")


def load_env() -> None:
    """Load the repo-root ``.env`` once (S2_API_KEY / Serp_API_KEY / CONTACT_EMAIL).

    Centralizing the load here removes the hidden import-order dependency the
    individual clients used to have. python-dotenv is optional: without it
    real environment variables still work and ``.env`` is simply ignored.
    """
    if getattr(load_env, "_done", False):
        return
    load_env._done = True
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv()


def normalize_doi(doi: Optional[str]) -> Optional[str]:
    """Lowercase a DOI and strip any https://(dx.)doi.org/ prefix."""
    if not doi:
        return None
    doi = doi.strip().lower()
    doi = DOI_URL_PREFIX.sub("", doi)
    return doi or None
