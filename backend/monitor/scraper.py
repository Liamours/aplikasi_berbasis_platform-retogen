import json
import logging
import re
import threading
import time
from difflib import SequenceMatcher
from typing import Optional
from urllib.parse import quote_plus

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
    "        shop { name city }"
    "      }"
    "    }"
    "  }"
    "}"
)

FCITY_BY_LOCATION = {
    "dki jakarta": ("DKI Jakarta", "174,175,176,177,178,179"),
    "jakarta": ("DKI Jakarta", "174,175,176,177,178,179"),
    "jakarta barat": ("Jakarta Barat", "174"),
    "jakarta selatan": ("Jakarta Selatan", "175"),
    "jakarta pusat": ("Jakarta Pusat", "176"),
    "jakarta utara": ("Jakarta Utara", "177"),
    "jakarta timur": ("Jakarta Timur", "178"),
    "jabodetabek": ("Jabodetabek", "144,146,150,151,167,168,171,174,175,176,177,178,179"),
    "kab. bandung": ("Kab. Bandung", "148"),
    "kabupaten bandung": ("Kab. Bandung", "148"),
    "bojongsoang": ("Kab. Bandung", "148"),
    "dayeuhkolot": ("Kab. Bandung", "148"),
    "bandung": ("Bandung", "165"),
    "surabaya": ("Surabaya", "252"),
    "kab. tangerang": ("Kab. Tangerang", "144"),
    "kabupaten tangerang": ("Kab. Tangerang", "144"),
    "tangerang": ("Tangerang", "146"),
    "tangerang selatan": ("Jabodetabek", "144,146,150,151,167,168,171,174,175,176,177,178,179"),
    "kab. bekasi": ("Kab. Bekasi", "150"),
    "kabupaten bekasi": ("Kab. Bekasi", "150"),
    "bekasi": ("Bekasi", "167"),
    "kab. bogor": ("Kab. Bogor", "151"),
    "kabupaten bogor": ("Kab. Bogor", "151"),
    "bogor": ("Bogor", "168"),
    "depok": ("Depok", "171"),
}

ACCESSORY_TERMS = (
    "keyboard protector",
    "pelindung keyboard",
    "keyboard cover",
    "body protector",
    "screen protector",
    "protector",
    "screen guard",
    "pelindung layar",
    "filter pelindung layar",
    "pelindung kamera",
    "ring pelindung",
    "tempered glass",
    "anti-spy",
    "privacy",
    "anti-blueray",
    "anti-blue",
    "hardcase",
    "softcase",
    "case",
    "cover",
    "casing",
    "sleeve",
    "skin",
    "garskin",
    "sticker",
    "stiker",
    "vinyl",
    "charger",
    "adapter",
    "adaptor",
    "cable",
    "kabel",
    "converter",
    "cooling fan",
    "kipas",
    "battery",
    "baterai",
    "trackpad",
    "touchpad",
    "speaker",
    "stylus",
    "s pen",
    "flipsuit",
    "anti gores",
    "hydrogel",
    "magnetic ring",
    "magsafe",
    "card holder",
    "wallet",
    "dompet",
    "jelly",
    "silicone",
    "protective",
    "cleaner",
    "pembersih",
    "kain lap",
    "microfiber",
    "sports suit",
    "dobe",
    "dock",
    "charging station",
    "hub",
    "controller",
    "gamepad",
    "lcd",
    "spare part",
    "sparepart",
    "tas laptop",
)

ACCESSORY_PATTERNS = tuple(
    re.compile(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])")
    for term in ACCESSORY_TERMS
)
ACCESSORY_PREFIX_TERMS = ("keyboard",)


def _build_search_params(keyword: str, rows: int = 20, fcity: Optional[str] = None) -> str:
    params = f"device=desktop&q={quote_plus(keyword)}&rows={rows}&page=1&st=product&source=universe"
    if fcity:
        params = f"{params}&fcity={quote_plus(fcity)}"
    return params


def _build_payload(keyword: str, rows: int = 20, fcity: Optional[str] = None) -> str:
    params = _build_search_params(keyword, rows, fcity)
    return json.dumps([{
        "operationName": "SearchProductQueryV4",
        "variables": {"params": params},
        "query": GQL_QUERY,
    }])


def _fallback_keywords(product_name: str) -> list[str]:
    without_year = re.sub(r"\b20\d{2}\b", "", product_name)
    without_year = re.sub(r"\s+", " ", without_year).strip()

    if without_year and without_year.lower() != product_name.lower():
        return [without_year]

    return []


def _search_keywords(product_name: str) -> list[str]:
    keywords = [product_name.strip(), *_fallback_keywords(product_name)]
    deduped = []
    seen = set()

    for keyword in keywords:
        normalized = keyword.lower()
        if keyword and normalized not in seen:
            deduped.append(keyword)
            seen.add(normalized)

    return deduped


def _normalize_location_name(location: str) -> str:
    value = location.lower().strip()
    value = re.sub(r"^kota\s+", "", value)
    value = re.sub(r"\s+", " ", value)
    return value


def _resolve_location_filter(
    location: Optional[str] = None,
    fcity: Optional[str] = None,
) -> tuple[Optional[str], Optional[str]]:
    if fcity:
        return location.strip() if location else "Custom location", fcity.strip()

    if not location:
        return None, None

    normalized = _normalize_location_name(location)
    direct = FCITY_BY_LOCATION.get(normalized)
    if direct:
        return direct

    for key, value in sorted(FCITY_BY_LOCATION.items(), key=lambda item: len(item[0]), reverse=True):
        if key in normalized:
            return value

    return None, None


_thread_local = threading.local()


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


def _get_session() -> cffi_requests.Session:
    if not hasattr(_thread_local, "session"):
        session = cffi_requests.Session(impersonate="chrome120")
        _warmup_session(session)
        _thread_local.session = session
    return _thread_local.session


def _fetch_raw(
    session: cffi_requests.Session,
    keyword: str,
    rows: int = 20,
    fcity: Optional[str] = None,
) -> list:
    search_params = _build_search_params(keyword, rows, fcity)
    headers = {
        **HEADERS,
        "Referer": f"https://www.tokopedia.com/search?{search_params}",
    }
    resp = session.post(GQL_URL, headers=headers, data=_build_payload(keyword, rows, fcity), timeout=20)
    resp.raise_for_status()
    body = resp.json()
    try:
        return body[0]["data"]["ace_search_product_v4"]["data"]["products"]
    except (KeyError, IndexError, TypeError) as e:
        logger.error("Unexpected GQL response shape: %s | body: %r", e, body)
        return []


def _relevance_score(query: str, product_name: str) -> float:
    q = query.lower().strip()
    p = product_name.lower().strip()

    query_tokens = set(q.split())
    product_tokens = set(p.split())
    if not query_tokens:
        return 0.0

    token_overlap = len(query_tokens & product_tokens) / len(query_tokens)
    seq_ratio = SequenceMatcher(None, q, p).ratio()
    return round(0.65 * token_overlap + 0.35 * seq_ratio, 4)


def _normalized_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _contains_accessory_term(text: str) -> bool:
    text_lower = text.lower()
    starts_with_accessory = any(
        text_lower.startswith(f"{term} ") for term in ACCESSORY_PREFIX_TERMS
    )
    return starts_with_accessory or any(pattern.search(text_lower) for pattern in ACCESSORY_PATTERNS)


def _is_accessory_result(query: str, product_name: str) -> bool:
    return _contains_accessory_term(product_name) and not _contains_accessory_term(query)


def _is_year_token(token: str) -> bool:
    return bool(re.fullmatch(r"20\d{2}", token))


def _model_tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"\b[a-z]*\d+[a-z0-9]*\b", text.lower())
        if not _is_year_token(token)
    }


def _has_negated_query_model(query: str, product_name: str) -> bool:
    product_lower = product_name.lower()
    for token in _model_tokens(query):
        if re.search(rf"\b(bukan|not)\s+{re.escape(token)}\b", product_lower):
            return True
    return False


def _token_prefix(token: str) -> str:
    match = re.match(r"[a-z]+", token)
    return match.group(0) if match else ""


def _conflicts_with_query_token(candidate: str, query_token: str) -> bool:
    if candidate == query_token:
        return False

    candidate_prefix = _token_prefix(candidate)
    query_prefix = _token_prefix(query_token)

    if candidate_prefix or query_prefix:
        return candidate_prefix == query_prefix

    return candidate.isdigit() and query_token.isdigit()


def _has_conflicting_primary_model(query: str, product_name: str) -> bool:
    query_models = _model_tokens(query)
    if not query_models:
        return False

    product_models = [
        token
        for token in re.findall(r"\b[a-z]*\d+[a-z0-9]*\b", product_name.lower())
        if not _is_year_token(token)
    ]

    for candidate in product_models:
        if candidate in query_models:
            return False

        if any(_conflicts_with_query_token(candidate, query_token) for query_token in query_models):
            return True

    return False


def _has_required_model_tokens(query: str, product_name: str) -> bool:
    query_models = _model_tokens(query)
    if not query_models:
        return True

    product_tokens = set(_normalized_tokens(product_name))
    return query_models.issubset(product_tokens)


def _is_valid_product_match(query: str, product_name: str) -> bool:
    if _is_accessory_result(query, product_name):
        return False

    if _has_negated_query_model(query, product_name):
        return False

    if _has_conflicting_primary_model(query, product_name):
        return False

    return _has_required_model_tokens(query, product_name)


def _score_products(raw_products: list, product_name: str, min_score: float) -> tuple[list, list[str]]:
    errors = []
    scored = []

    for i, raw in enumerate(raw_products):
        product = normalize_product(raw)
        if not product:
            msg = f"Item {i} skipped - normalization failed"
            logger.warning(msg)
            errors.append(msg)
            continue

        if not _is_valid_product_match(product_name, product["product"]):
            logger.debug("Excluded invalid product match '%s'", product["product"])
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

    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    return scored, errors


def _result_key(product: dict) -> tuple[str, str, str, str]:
    return (
        str(product.get("product") or "").lower(),
        str(product.get("store") or "").lower(),
        str(product.get("seller_city") or "").lower(),
        str(product.get("price") or ""),
    )


def scrape_tokopedia(
    product_name: str,
    limit: int = 10,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    min_score: float = 0.3,
    location: Optional[str] = None,
    fcity: Optional[str] = None,
) -> dict:
    del latitude, longitude

    requested_location = location.strip() if location else None
    applied_location, resolved_fcity = _resolve_location_filter(requested_location, fcity)
    session = _get_session()
    fetch_rows = 50

    errors = []
    results = []
    seen_results = set()
    raw_products = []
    final_keyword = product_name
    result_fcity = None
    broad_fallback_used = False

    try:
        keywords = _search_keywords(product_name)
        location_candidates = [(keyword, resolved_fcity) for keyword in keywords] if resolved_fcity else []
        broad_candidates = [(keyword, None) for keyword in keywords]
        candidate_groups = [location_candidates, broad_candidates] if location_candidates else [broad_candidates]

        for candidates in candidate_groups:
            before_group_count = len(results)
            for keyword, candidate_fcity in candidates:
                raw_products = _fetch_raw(session, keyword, fetch_rows, candidate_fcity)
                scored, attempt_errors = _score_products(raw_products, product_name, min_score)
                errors.extend(attempt_errors)
                final_keyword = keyword

                if candidate_fcity and scored:
                    result_fcity = candidate_fcity
                elif resolved_fcity and scored:
                    broad_fallback_used = True

                for product in scored:
                    key = _result_key(product)
                    if key in seen_results:
                        continue

                    seen_results.add(key)
                    results.append(product)

                    if len(results) >= limit:
                        break

                if len(results) >= limit:
                    break

                if not scored:
                    logger.info("No scored results for %r with fcity=%r", keyword, candidate_fcity)

            if len(results) > before_group_count:
                break
    except Exception as e:
        if hasattr(_thread_local, "session"):
            del _thread_local.session
        msg = f"GQL fetch failed: {e}"
        logger.error(msg)
        return {
            "results": [],
            "errors": [msg],
            "total": 0,
            "detected_city": requested_location,
            "applied_location": applied_location,
            "location_filter_applied": False,
            "location_fallback_used": False,
        }

    location_filter_applied = bool(result_fcity)
    location_fallback_used = bool(broad_fallback_used)

    logger.info(
        "scrape_tokopedia: query=%r final_query=%r fcity=%r fetched=%d returned=%d threshold=%.2f",
        product_name, final_keyword, result_fcity, len(raw_products), len(results), min_score
    )

    return {
        "results": results,
        "errors": errors,
        "total": len(results),
        "detected_city": requested_location,
        "applied_location": applied_location,
        "location_filter_applied": location_filter_applied,
        "location_fallback_used": location_fallback_used,
    }
