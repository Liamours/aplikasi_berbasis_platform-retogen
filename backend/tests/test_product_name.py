"""
Tests for product_name field on articles.
Covers: add, view, edit/get, edit/update.
"""
import uuid
import pytest

SMALL_IMAGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="


def _unique_title():
    return f"ProdName Test {uuid.uuid4().hex[:6]}"


def _add_article(client, headers, product_name=None):
    payload = {
        "article_title": _unique_title(),
        "article_preview": "Preview text",
        "article_content": "Content body",
        "article_tags": ["laptop"],
        "article_image": SMALL_IMAGE_B64,
    }
    if product_name is not None:
        payload["product_name"] = product_name

    r = client.post("/article/add", json=payload, headers=headers)
    assert r.status_code == 200
    return payload["article_title"]


def _get_article_id_by_title(client, headers, title):
    resp = client.post("/article/main_page", json={}, headers=headers)
    articles = resp.json().get("list_article", [])
    match = next((a for a in articles if a["article_title"] == title), None)
    return match["article_id"] if match else None


# ── add with product_name ─────────────────────────────────────────────────────

def test_add_article_with_product_name(client, auth_headers_admin, auth_headers_user):
    print("\n[TEST CASE] product_name - Add Artikel Dengan product_name")
    pname = "Dell XPS 15 9530"
    title = _add_article(client, auth_headers_admin, product_name=pname)
    article_id = _get_article_id_by_title(client, auth_headers_admin, title)
    assert article_id is not None

    r = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    assert r.status_code == 200
    assert r.json().get("product_name") == pname


def test_add_article_without_product_name(client, auth_headers_admin, auth_headers_user):
    print("\n[TEST CASE] product_name - Add Artikel Tanpa product_name")
    title = _add_article(client, auth_headers_admin, product_name=None)
    article_id = _get_article_id_by_title(client, auth_headers_admin, title)
    assert article_id is not None

    r = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    assert r.status_code == 200
    # product_name should be None/null when not set
    assert r.json().get("product_name") is None


def test_view_returns_product_name_field(client, auth_headers_admin, auth_headers_user):
    print("\n[TEST CASE] product_name - View Artikel Kembalikan product_name Field")
    pname = "MacBook Pro 14 M3"
    title = _add_article(client, auth_headers_admin, product_name=pname)
    article_id = _get_article_id_by_title(client, auth_headers_admin, title)

    r = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    assert "product_name" in r.json()


def test_product_name_is_string_or_none(client, auth_headers_admin, auth_headers_user):
    print("\n[TEST CASE] product_name - product_name Bertipe String Atau None")
    pname = "ASUS ROG Zephyrus G14"
    title = _add_article(client, auth_headers_admin, product_name=pname)
    article_id = _get_article_id_by_title(client, auth_headers_admin, title)

    r = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    val = r.json().get("product_name")
    assert val is None or isinstance(val, str)


# ── edit/get returns product_name ─────────────────────────────────────────────

def test_edit_get_returns_product_name(client, auth_headers_admin):
    print("\n[TEST CASE] product_name - Edit Get Kembalikan product_name")
    pname = "Lenovo ThinkPad X1 Carbon Gen 12"
    title = _add_article(client, auth_headers_admin, product_name=pname)
    article_id = _get_article_id_by_title(client, auth_headers_admin, title)

    r = client.post("/article/edit/get", json={"article_id": article_id}, headers=auth_headers_admin)
    assert r.status_code == 200
    assert r.json().get("product_name") == pname


def test_edit_get_product_name_none_when_unset(client, auth_headers_admin):
    print("\n[TEST CASE] product_name - Edit Get product_name None Jika Tidak Di-set")
    title = _add_article(client, auth_headers_admin, product_name=None)
    article_id = _get_article_id_by_title(client, auth_headers_admin, title)

    r = client.post("/article/edit/get", json={"article_id": article_id}, headers=auth_headers_admin)
    assert r.json().get("product_name") is None


# ── edit/update product_name ──────────────────────────────────────────────────

def test_edit_update_product_name(client, auth_headers_admin, auth_headers_user):
    print("\n[TEST CASE] product_name - Edit Update product_name Berhasil")
    title = _add_article(client, auth_headers_admin, product_name="Old Product")
    article_id = _get_article_id_by_title(client, auth_headers_admin, title)

    new_pname = "HP Pavilion Plus 14 Updated"
    r = client.post("/article/edit/update", json={
        "article_id": article_id,
        "article_title": title,
        "article_preview": "Preview text",
        "article_content": "Content body",
        "article_tags": ["laptop"],
        "article_image": SMALL_IMAGE_B64,
        "product_name": new_pname,
    }, headers=auth_headers_admin)
    assert r.json()["confirmation"] == "successful: article edited"

    view = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    assert view.json().get("product_name") == new_pname


def test_edit_update_product_name_to_none_stays_unchanged(client, auth_headers_admin, auth_headers_user):
    print("\n[TEST CASE] product_name - Edit Update Tanpa product_name Tidak Hapus Nilai")
    title = _add_article(client, auth_headers_admin, product_name="Keep This")
    article_id = _get_article_id_by_title(client, auth_headers_admin, title)

    # Update without product_name field
    client.post("/article/edit/update", json={
        "article_id": article_id,
        "article_title": title,
        "article_preview": "Updated preview",
        "article_content": "Content body",
        "article_tags": ["laptop"],
        "article_image": SMALL_IMAGE_B64,
    }, headers=auth_headers_admin)

    view = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    # product_name should remain unchanged since we didn't send it
    assert view.json().get("product_name") == "Keep This"
