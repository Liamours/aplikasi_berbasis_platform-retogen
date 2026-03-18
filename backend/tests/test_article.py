def test_add_article_success(client):
    print("\n[TEST CASE] Add Article - Data Valid")

    payload = {
        "article_title": "Judul Test",
        "article_preview": "Preview Test",
        "article_content": "Isi artikel lengkap",
        "article_tag": "tech",
        "article_image": "aGVsbG8="
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"    {k}: {v}")

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(f"    response: {response.json()}")

    assert response.status_code == 200
    assert response.json()["confirmation"] == "success: article added"

    print("[RESULT]")
    print("    Artikel berhasil ditambahkan")

def test_add_article_not_admin(client):
    print("\n[TEST CASE] Add Article - Bukan Admin")

    from main import app
    from core.dependencies import get_current_user

    async def fake_user():
        return {"email": "user@mail.com", "role": "user"}

    app.dependency_overrides[get_current_user] = fake_user

    payload = {
        "article_title": "Judul Test",
        "article_preview": "Preview Test",
        "article_content": "Isi artikel",
        "article_tag": "tech",
        "article_image": "aGVsbG8="
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"    {k}: {v}")

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(f"    response: {response.json()}")

    assert response.json()["confirmation"] == "not admin"

    print("[RESULT]")
    print("    Sistem menolak user non-admin")


def test_add_article_invalid_title(client):
    print("\n[TEST CASE] Add Article - Title Kosong")

    payload = {
        "article_title": "",
        "article_preview": "Preview",
        "article_content": "Isi",
        "article_tag": "tech",
        "article_image": "aGVsbG8="
    }

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(f"    response: {response.json()}")

    assert "Title must be" in response.json()["confirmation"]

    print("[RESULT]")
    print("    Sistem menolak title kosong")


def test_add_article_invalid_preview(client):
    print("\n[TEST CASE] Add Article - Preview Kosong")

    payload = {
        "article_title": "Judul",
        "article_preview": "",
        "article_content": "Isi",
        "article_tag": "tech",
        "article_image": "aGVsbG8="
    }

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(f"    response: {response.json()}")

    assert "Preview must be" in response.json()["confirmation"]

    print("[RESULT]")
    print("    Sistem menolak preview kosong")


def test_add_article_invalid_content(client):
    print("\n[TEST CASE] Add Article - Content Kosong")

    payload = {
        "article_title": "Judul",
        "article_preview": "Preview",
        "article_content": "",
        "article_tag": "tech",
        "article_image": "aGVsbG8="
    }

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(f"    response: {response.json()}")

    assert "Content must be" in response.json()["confirmation"]

    print("[RESULT]")
    print("    Sistem menolak content kosong")


def test_add_article_invalid_image_format(client):
    print("\n[TEST CASE] Add Article - Image Tidak Valid")

    payload = {
        "article_title": "Judul",
        "article_preview": "Preview",
        "article_content": "Isi",
        "article_tag": "tech",
        "article_image": "bukan_base64!!!"
    }

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(f"    response: {response.json()}")

    assert "Image format must be valid Base64." in response.json()["confirmation"]

    print("[RESULT]")
    print("    Sistem menolak format image tidak valid")

import base64

# =========================
# HELPER
# =========================

import base64

def dummy_base64():
    return base64.b64encode(b"\xff\xd8\xff\xe0fakejpeg").decode()

VALID_ID = "507f1f77bcf86cd799439011"

def create_article(client):
    payload = {
        "article_title": "Judul Test",
        "article_preview": "Preview Test",
        "article_content": "Content Test",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }
    res = client.post("/article/add", json=payload)
    assert res.status_code == 200
    return VALID_ID


# =========================
# ADD ARTICLE (biar reusable)
# =========================

def create_article(client):
    payload = {
        "article_title": "Judul Test",
        "article_preview": "Preview Test",
        "article_content": "Content Test",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }
    res = client.post("/article/add", json=payload)
    assert res.status_code == 200
    return payload


# =========================
# EDIT GET ARTICLE
# =========================

def test_edit_get_article_success(client):
    create_article(client)

    res = client.post("/article/edit/get", json={
        "article_id": VALID_ID
    })

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "successful"


def test_edit_get_article_not_found(client):
    res = client.post("/article/edit/get", json={
        "article_id": "invalid"
    })

    assert res.json()["confirmation"] == "backend error"


# =========================
# EDIT UPDATE ARTICLE
# =========================

def test_update_article_success(client):
    create_article(client)

    payload = {
        "article_id": VALID_ID,
        "article_title": "Updated",
        "article_preview": "Updated",
        "article_content": "Updated",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }

    res = client.post("/article/edit/update", json=payload)
    data = res.json()

    assert res.status_code == 200
    assert "successful" in data["confirmation"]


def test_update_article_invalid_title(client):
    create_article(client)

    payload = {
        "article_id": VALID_ID,
        "article_title": "",  # ❌ invalid
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }

    res = client.post("/article/edit/update", json=payload)

    assert res.json()["confirmation"] == "Title must be 1-256 characters long."


def test_update_article_invalid_image(client):
    create_article(client)

    payload = {
        "article_id": VALID_ID,
        "article_title": "Valid",
        "article_preview": "Valid",
        "article_content": "Valid",
        "article_tag": "tech",
        "article_image": "not_base64"
    }

    res = client.post("/article/edit/update", json=payload)

    assert res.json()["confirmation"] == "invalid image format"


# =========================
# VIEW ARTICLE
# =========================

def test_view_article_success(client):
    create_article(client)

    res = client.post("/article/view", json={
        "article_id": VALID_ID
    })

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "successful"
    assert "article_title" in data
    assert "comments" in data
    assert "ratings" in data


def test_view_article_not_found(client):
    res = client.post("/article/view", json={
        "article_id": "invalid"
    })

    assert res.json()["confirmation"] == "backend error"


# =========================
# DELETE ARTICLE
# =========================

def test_delete_article_success(client):
    create_article(client)

    res = client.post("/article/delete", json={
        "article_id": "507f1f77bcf86cd799439011"  # valid ObjectId format
    })

    data = res.json()

    assert res.status_code == 200
    assert "successful" in data["confirmation"]


def test_delete_article_invalid_id(client):
    res = client.post("/article/delete", json={
        "article_id": "invalid_id"
    })

    assert res.json()["confirmation"] == "backend error"