import json
import logging
import threading
import time
from difflib import SequenceMatcher
from functools import lru_cache
from typing import Optional
from urllib.parse import quote_plus

import requests as std_requests
from curl_cffi import requests as cffi_requests
from monitor.parser import normalize_product

logger = logging.getLogger(__name__)

GQL_URL = "https://gql.tokopedia.com/graphql/SearchProductQueryV4"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": "https://www.tokopedia.com",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
    "x-device": "desktop-0.0",
    "x-source": "tokopedia-lite",
    "x-tkpd-lite-service": "zeus",
    "x-version": "e00e6cf",
    "tkpd-userid": "0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}

GQL_QUERY = (
    "query SearchProductQueryV4($params: String!) {"
    "  ace_search_product_v4(params: $params) {"
    "    data {"
    "      products {"
    "        name price ratingAverage"
    "        shop { name }"
    "      }"
    "    }"
    "  }"
    "}"
)


@lru_cache(maxsize=256)
def _reverse_geocode_cached(lat_r: float, lng_r: float) -> Optional[str]:
    try:
        resp = std_requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat_r, "lon": lng_r, "format": "json"},
            headers={"User-Agent": "retogen-app/1.0"},
            timeout=5,
        )
        data = resp.json()
        addr = data.get("address", {})
        city = (
            addr.get("city")
            or addr.get("town")
            or addr.get("county")
            or addr.get("state")
        )
        return city
    except Exception as e:
        logger.warning("Reverse geocode failed: %s", e)
        return None


def reverse_geocode(lat: float, lng: float) -> Optional[str]:
    """Nominatim reverse geocode → city/regency name. Coords rounded to 2dp (~1km) for cache efficiency."""
    return _reverse_geocode_cached(round(lat, 2), round(lng, 2))


def _build_payload(keyword: str, rows: int = 20) -> str:
    params = f"device=desktop&q={quote_plus(keyword)}&rows={rows}&page=1&st=product&source=universe"
    return json.dumps([{
        "operationName": "SearchProductQueryV4",
        "variables": {"params": params},
        "query": GQL_QUERY,
    }])


_thread_local = threading.local()


def _warmup_session(session: cffi_requests.Session) -> None:
    try:
        session.get("https://www.tokopedia.com/", headers={
            "User-Agent": HEADERS["User-Agent"],
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            "Accept-Language": HEADERS["Accept-Language"],
        }, timeout=15)
        time.sleep(2)  # OK here — runs inside asyncio.to_thread, not blocking event loop
    except Exception as e:
        logger.warning("Session warmup failed (continuing anyway): %s", e)


def _get_session() -> cffi_requests.Session:
    """Return a warmed cffi session for the current thread. Warms up once per worker thread."""
    if not hasattr(_thread_local, "session"):
        s = cffi_requests.Session(impersonate="chrome120")
        _warmup_session(s)
        _thread_local.session = s
    return _thread_local.session


def _fetch_raw(session: cffi_requests.Session, keyword: str, rows: int = 20) -> list:
    headers = {
        **HEADERS,
        "Referer": f"https://www.tokopedia.com/search?q={quote_plus(keyword)}",
    }
    resp = session.post(GQL_URL, headers=headers, data=_build_payload(keyword, rows), timeout=20)
    resp.raise_for_status()
    body = resp.json()
    try:
        return body[0]["data"]["ace_search_product_v4"]["data"]["products"]
    except (KeyError, IndexError, TypeError) as e:
        logger.error("Unexpected GQL response shape: %s | body: %r", e, body)
        return []


def _relevance_score(query: str, product_name: str) -> float:
    """
    Compute fuzzy relevance score between search query and product name.
    Uses two signals:
      1. Token overlap (keyword coverage) — what fraction of query words appear in product name
      2. Sequence similarity ratio (difflib)
    Returns weighted average in [0.0, 1.0].
    """
    q = query.lower().strip()
    p = product_name.lower().strip()

    # Token coverage: fraction of query tokens found in product name
    query_tokens = set(q.split())
    product_tokens = set(p.split())
    if not query_tokens:
        return 0.0
    token_overlap = len(query_tokens & product_tokens) / len(query_tokens)

    # Sequence similarity
    seq_ratio = SequenceMatcher(None, q, p).ratio()

    # Weight: token overlap matters more for product search (partial matches common)
    score = 0.65 * token_overlap + 0.35 * seq_ratio
    return round(score, 4)


def scrape_tokopedia(
    product_name: str,
    limit: int = 10,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    min_score: float = 0.3,
) -> dict:
    """
    Scrape Tokopedia for product listings matching product_name.

    Args:
        product_name: Search keyword
        limit: Max results to return after filtering
        latitude: Optional device latitude for geo-enhanced search
        longitude: Optional device longitude for geo-enhanced search
        min_score: Minimum fuzzy relevance score [0.0–1.0].
                   Results below threshold are excluded. Set 0.0 to disable filtering.
    """
    # Reverse geocode if coords provided — appends city to keyword
    detected_city = None
    keyword = product_name
    if latitude is not None and longitude is not None:
        detected_city = reverse_geocode(latitude, longitude)
        if detected_city:
            keyword = f"{product_name} {detected_city}"
            logger.info("Geo-enhanced search: %r (city: %s)", keyword, detected_city)

    session = _get_session()
    fetch_rows = min(limit * 2, 50)

    errors = []
    results = []

    try:
        raw_products = _fetch_raw(session, keyword, fetch_rows)
    except Exception as e:
        if hasattr(_thread_local, "session"):
            del _thread_local.session
        msg = f"GQL fetch failed: {e}"
        logger.error(msg)
        return {"results": [], "errors": [msg], "total": 0, "detected_city": detected_city}

    scored = []
    for i, raw in enumerate(raw_products):
        product = normalize_product(raw)
        if not product:
            msg = f"Item {i} skipped — normalization failed"
            logger.warning(msg)
            errors.append(msg)
            continue

        score = _relevance_score(product_name, product["product"])
        product["relevance_score"] = score

        if score < min_score:
            logger.debug(
                "Excluded '%s' (score=%.3f < threshold=%.3f)",
                product["product"], score, min_score
            )
            continue

        scored.append(product)

    # Sort by relevance descending, then cap at limit
    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    results = scored[:limit]

    logger.info(
        "scrape_tokopedia: query=%r fetched=%d passed_filter=%d returned=%d threshold=%.2f",
        product_name, len(raw_products), len(scored), len(results), min_score
    )

    return {"results": results, "errors": errors, "total": len(results), "detected_city": detected_city}
