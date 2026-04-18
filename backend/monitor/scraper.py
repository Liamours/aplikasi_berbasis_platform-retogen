import json
import logging
import time
from typing import Optional

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


def _build_payload(keyword: str) -> str:
    params = f"device=desktop&q={keyword.replace(' ', '%20')}&rows=10&page=1&st=product&source=universe"
    return json.dumps([{
        "operationName": "SearchProductQueryV4",
        "variables": {"params": params},
        "query": GQL_QUERY,
    }])


def _warmup_session(session: cffi_requests.Session) -> None:
    try:
        session.get("https://www.tokopedia.com/", headers={
            "User-Agent": HEADERS["User-Agent"],
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            "Accept-Language": HEADERS["Accept-Language"],
        }, timeout=15)
        time.sleep(2)
    except Exception as e:
        logger.warning("Session warmup failed (continuing anyway): %s", e)


def _fetch_raw(session: cffi_requests.Session, keyword: str) -> list:
    headers = {
        **HEADERS,
        "Referer": f"https://www.tokopedia.com/search?q={keyword.replace(' ', '+')}",
    }
    resp = session.post(GQL_URL, headers=headers, data=_build_payload(keyword), timeout=20)
    resp.raise_for_status()
    body = resp.json()
    try:
        return body[0]["data"]["ace_search_product_v4"]["data"]["products"]
    except (KeyError, IndexError, TypeError) as e:
        logger.error("Unexpected GQL response shape: %s | body: %r", e, body)
        return []


def scrape_tokopedia(product_name: str, limit: int = 10) -> dict:
    session = cffi_requests.Session(impersonate="chrome120")
    _warmup_session(session)

    errors = []
    results = []

    try:
        raw_products = _fetch_raw(session, product_name)
    except Exception as e:
        msg = f"GQL fetch failed: {e}"
        logger.error(msg)
        return {"results": [], "errors": [msg], "total": 0}

    for i, raw in enumerate(raw_products[:limit]):
        product = normalize_product(raw)
        if product:
            results.append(product)
        else:
            msg = f"Item {i} skipped — normalization failed"
            logger.warning(msg)
            errors.append(msg)

    return {"results": results, "errors": errors, "total": len(results)}
