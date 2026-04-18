import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def parse_price(raw) -> Optional[int]:
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        return int(raw)
    if not isinstance(raw, str):
        logger.warning("Unexpected price type: %s (%r)", type(raw).__name__, raw)
        return None
    digits = re.sub(r"[^\d]", "", raw)
    if not digits:
        logger.warning("Could not extract digits from price: %r", raw)
        return None
    value = int(digits)
    if not (100 <= value <= 1_000_000_000):
        logger.warning("Price out of expected range: %d (raw: %r)", value, raw)
    return value


def parse_rating(raw) -> Optional[float]:
    if raw is None:
        return None
    if isinstance(raw, float):
        return raw if raw > 0 else None
    if isinstance(raw, int):
        return float(raw) if raw > 0 else None
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            return None
        try:
            value = float(raw.replace(",", "."))
            if not (0.0 <= value <= 5.0):
                logger.warning("Rating out of 0-5 range: %f (raw: %r)", value, raw)
            return value if value > 0 else None
        except ValueError:
            logger.warning("Could not parse rating: %r", raw)
            return None
    logger.warning("Unexpected rating type: %s (%r)", type(raw).__name__, raw)
    return None


def normalize_product(raw: dict) -> Optional[dict]:
    try:
        name = raw.get("name")
        if not name or not isinstance(name, str):
            logger.warning("Missing or invalid product name: %r", raw)
            return None
        store = raw.get("shop", {}).get("name") if isinstance(raw.get("shop"), dict) else None
        return {
            "product": name.strip(),
            "store": store.strip() if store else None,
            "price": parse_price(raw.get("price")),
            "rating": parse_rating(raw.get("ratingAverage")),
        }
    except Exception as e:
        logger.error("Failed to normalize product: %s | raw: %r", e, raw)
        return None
