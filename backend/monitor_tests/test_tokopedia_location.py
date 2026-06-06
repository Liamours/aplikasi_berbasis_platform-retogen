import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from monitor import scraper
from monitor.parser import normalize_product


def _raw_product(name="HP Pavilion Plus 14 Laptop", city="Kab. Bandung"):
    return {
        "name": name,
        "price": "Rp15.000.000",
        "ratingAverage": "4.8",
        "shop": {"name": "Local Store", "city": city},
    }


def test_payload_includes_fcity_when_location_filter_is_used():
    payload = json.loads(scraper._build_payload("ASUS ROG Zephyrus G14", rows=10, fcity="176"))

    params = payload[0]["variables"]["params"]
    assert "q=ASUS+ROG+Zephyrus+G14" in params
    assert "rows=10" in params
    assert "fcity=176" in params


def test_location_names_map_to_tokopedia_city_ids():
    assert scraper._resolve_location_filter(location="Jakarta Pusat") == ("Jakarta Pusat", "176")
    assert scraper._resolve_location_filter(location="DKI Jakarta Pusat") == ("Jakarta Pusat", "176")
    assert scraper._resolve_location_filter(location="Bojongsoang") == ("Kab. Bandung", "148")
    assert scraper._resolve_location_filter(location="Dayeuhkolot") == ("Kab. Bandung", "148")
    assert scraper._resolve_location_filter(location="Kabupaten Bandung") == ("Kab. Bandung", "148")
    assert scraper._resolve_location_filter(location="Jakarta Pusat", fcity="176") == ("Jakarta Pusat", "176")


def test_normalize_product_keeps_seller_city():
    product = normalize_product(_raw_product(city="Jakarta Pusat"))

    assert product["store"] == "Local Store"
    assert product["seller_city"] == "Jakarta Pusat"


def test_obvious_accessory_matches_do_not_stop_product_monitoring():
    raw_products = [
        _raw_product(name="Keyboard Protector ASUS ROG Zephyrus G14 2024 GA403", city="Jakarta Pusat"),
        _raw_product(name="Pelindung Keyboard MacBook Pro M3 14 inch", city="Jakarta Pusat"),
        _raw_product(name="180W Adaptor Compatible with ASUS ROG Zephyrus G14 2024", city="Jakarta Pusat"),
        _raw_product(name="Trackpad Touchpad MacBook Pro M3 14 inch Original", city="Jakarta Pusat"),
        _raw_product(name="Case iPhone 15 Pro Max Magnetic Ring Silicone", city="Jakarta Pusat"),
        _raw_product(name="Filter Pelindung Layar Privacy MacBook Pro M3 14 inch", city="Jakarta Pusat"),
        _raw_product(name="Macbook Air Pro Max M1 M2 M3 Chip 16 15 14 Inch Cleaner Kit", city="Jakarta Pusat"),
        _raw_product(name="Stylus S Pen Samsung Galaxy S24 Ultra SPen", city="Jakarta Pusat"),
        _raw_product(name="Dompet Kartu Card Holder MagSafe for iPhone 16 15 14 Pro Max", city="Jakarta Pusat"),
        _raw_product(name="Keyboard Dell XPS 15 9530 Precision M3800", city="Jakarta Pusat"),
        _raw_product(name="Garskin Stiker Laptop MSI Stealth 14 Studio A13V", city="Jakarta Pusat"),
        _raw_product(name="Portable Switch Dock Charging Station HUB for Nintendo Switch OLED", city="Jakarta Pusat"),
        _raw_product(name="Ring Pelindung Kamera Samsung Galaxy S24 Ultra", city="Jakarta Pusat"),
        _raw_product(name="Wireless Controller Gamepad for Nintendo Switch OLED", city="Jakarta Pusat"),
        _raw_product(name="ASUS ROG Zephyrus G14 2024 Ryzen 9 RTX 4060 Laptop", city="Jakarta Pusat"),
    ]

    scored, errors = scraper._score_products(raw_products, "ASUS ROG Zephyrus G14 2024", min_score=0.0)

    assert errors == []
    assert [item["product"] for item in scored] == [
        "ASUS ROG Zephyrus G14 2024 Ryzen 9 RTX 4060 Laptop",
    ]


def test_negated_query_model_does_not_pass_relevance_filter():
    raw_products = [
        _raw_product(name="Samsung Galaxy S25 Ultra Garansi Resmi [ Bukan S24 Plus ]", city="Jakarta Pusat"),
        _raw_product(name="Samsung Galaxy S26 Ultra Garansi Resmi Flagship S25 S24", city="Jakarta Pusat"),
        _raw_product(name="Samsung Galaxy S24 Ultra 5G 12GB 256GB Garansi Resmi", city="Jakarta Pusat"),
    ]

    scored, errors = scraper._score_products(raw_products, "Samsung Galaxy S24 Ultra", min_score=0.0)

    assert errors == []
    assert [item["product"] for item in scored] == [
        "Samsung Galaxy S24 Ultra 5G 12GB 256GB Garansi Resmi",
    ]


def test_search_tries_yearless_keyword_with_location_before_broad_fallback(monkeypatch):
    calls = []

    def fake_fetch(session, keyword, rows=20, fcity=None):
        calls.append((keyword, rows, fcity))
        if keyword == "HP Pavilion Plus 14" and fcity == "148":
            return [_raw_product()]
        return []

    monkeypatch.setattr(scraper, "_get_session", lambda: object())
    monkeypatch.setattr(scraper, "_fetch_raw", fake_fetch)

    result = scraper.scrape_tokopedia(
        "HP Pavilion Plus 14 2024",
        limit=5,
        location="Bojongsoang",
        min_score=0.0,
    )

    assert calls == [
        ("HP Pavilion Plus 14 2024", 50, "148"),
        ("HP Pavilion Plus 14", 50, "148"),
    ]
    assert result["total"] == 1
    assert result["applied_location"] == "Kab. Bandung"
    assert result["location_filter_applied"] is True
    assert result["location_fallback_used"] is False
    assert result["results"][0]["seller_city"] == "Kab. Bandung"


def test_search_falls_back_to_broad_results_when_local_filter_is_empty(monkeypatch):
    calls = []

    def fake_fetch(session, keyword, rows=20, fcity=None):
        calls.append((keyword, rows, fcity))
        if keyword == "ASUS ROG Zephyrus G14 2024" and fcity is None:
            return [_raw_product(name="ASUS ROG Zephyrus G14 2024 Laptop", city="Jakarta Selatan")]
        return []

    monkeypatch.setattr(scraper, "_get_session", lambda: object())
    monkeypatch.setattr(scraper, "_fetch_raw", fake_fetch)

    result = scraper.scrape_tokopedia(
        "ASUS ROG Zephyrus G14 2024",
        limit=5,
        location="Jakarta Pusat",
        min_score=0.0,
    )

    assert calls == [
        ("ASUS ROG Zephyrus G14 2024", 50, "176"),
        ("ASUS ROG Zephyrus G14", 50, "176"),
        ("ASUS ROG Zephyrus G14 2024", 50, None),
        ("ASUS ROG Zephyrus G14", 50, None),
    ]
    assert result["total"] == 1
    assert result["applied_location"] == "Jakarta Pusat"
    assert result["location_filter_applied"] is False
    assert result["location_fallback_used"] is True
    assert result["results"][0]["seller_city"] == "Jakarta Selatan"


def test_yearless_keyword_recovers_when_full_name_has_no_valid_results(monkeypatch):
    calls = []

    def fake_fetch(session, keyword, rows=20, fcity=None):
        calls.append((keyword, rows, fcity))
        if keyword == "ASUS TUF A15 2025" and fcity == "176":
            return [_raw_product(name="Case ASUS TUF A15 2025 Hardcase", city="Jakarta Pusat")]
        if keyword == "ASUS TUF A15" and fcity == "176":
            return [_raw_product(name="ASUS TUF A15 Ryzen 7 RTX 4060 Gaming Laptop", city="Jakarta Pusat")]
        return []

    monkeypatch.setattr(scraper, "_get_session", lambda: object())
    monkeypatch.setattr(scraper, "_fetch_raw", fake_fetch)

    result = scraper.scrape_tokopedia(
        "ASUS TUF A15 2025",
        limit=5,
        location="Jakarta Pusat",
        min_score=0.0,
    )

    assert calls == [
        ("ASUS TUF A15 2025", 50, "176"),
        ("ASUS TUF A15", 50, "176"),
    ]
    assert result["total"] == 1
    assert result["location_filter_applied"] is True
    assert result["results"][0]["product"] == "ASUS TUF A15 Ryzen 7 RTX 4060 Gaming Laptop"
