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
    client.post("/article/add", json=payload)

def test_add_article_success(client):
    print("\n[TEST CASE] Add Article - Data Valid")

    payload = {
        "article_title": "Judul Test",
        "article_preview": "Preview Test",
        "article_content": "Isi artikel lengkap",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(response.json())

    assert response.status_code == 200
    assert response.json()["confirmation"] == "success: article added"

    print("[RESULT]")
    print("Artikel berhasil ditambahkan")


def test_add_article_not_admin(client):
    print("\n[TEST CASE] Add Article - Bukan Admin")

    from main import app
    from core.dependencies import get_current_user

    async def fake_user():
        return {"email": "user@mail.com", "role": "user"}

    app.dependency_overrides[get_current_user] = fake_user

    payload = {
        "article_title": "Judul",
        "article_preview": "Preview",
        "article_content": "Isi",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(response.json())

    assert response.json()["confirmation"] == "not admin"

    print("[RESULT]")
    print("Sistem menolak user non-admin")


def test_add_article_invalid_title(client):
    print("\n[TEST CASE] Add Article - Title Kosong")

    payload = {
        "article_title": "",
        "article_preview": "Preview",
        "article_content": "Isi",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(response.json())

    assert "Title must be" in response.json()["confirmation"]

    print("[RESULT]")
    print("Sistem menolak title kosong")


def test_add_article_invalid_preview(client):
    print("\n[TEST CASE] Add Article - Preview Kosong")

    payload = {
        "article_title": "Judul",
        "article_preview": "",
        "article_content": "Isi",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(response.json())

    assert "Preview must be 1-128 characters long." in response.json()["confirmation"]

    print("[RESULT]")
    print("Sistem menolak preview kosong")


def test_add_article_invalid_content(client):
    print("\n[TEST CASE] Add Article - Content Kosong")

    payload = {
        "article_title": "Judul",
        "article_preview": "Preview",
        "article_content": "",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(response.json())

    assert "Content must be" in response.json()["confirmation"]

    print("[RESULT]")
    print("Sistem menolak content kosong")


def test_add_article_invalid_image_format(client):
    print("\n[TEST CASE] Add Article - Image Tidak Valid")

    payload = {
        "article_title": "Judul",
        "article_preview": "Preview",
        "article_content": "Isi",
        "article_tag": "tech",
        "article_image": "bukan_base64!!!"
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    response = client.post("/article/add", json=payload)

    print("[OUTPUT]")
    print(response.json())

    assert "Base64" in response.json()["confirmation"]

    print("[RESULT]")
    print("Sistem menolak format image tidak valid")

def test_edit_get_article_success(client):
    print("\n[TEST CASE] Get Article - Success")

    create_article(client)

    payload = {"article_id": VALID_ID}

    print("[INPUT]")
    print(payload)

    res = client.post("/article/edit/get", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Berhasil mengambil data artikel")


def test_edit_get_article_not_found(client):
    print("\n[TEST CASE] Get Article - Not Found")

    payload = {"article_id": "invalid"}

    print("[INPUT]")
    print(payload)

    res = client.post("/article/edit/get", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Artikel tidak ditemukan")

def test_update_article_success(client):
    print("\n[TEST CASE] Update Article - Success")

    create_article(client)

    payload = {
        "article_id": VALID_ID,
        "article_title": "Updated",
        "article_preview": "Updated",
        "article_content": "Updated",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/article/edit/update", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert "successful" in res.json()["confirmation"]

    print("[RESULT]")
    print("Artikel berhasil diupdate")


def test_update_article_invalid_title(client):
    print("\n[TEST CASE] Update Article - Title Invalid")

    create_article(client)

    payload = {
        "article_id": VALID_ID,
        "article_title": "",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tag": "tech",
        "article_image": dummy_base64()
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/article/edit/update", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert "Title must be" in res.json()["confirmation"]

    print("[RESULT]")
    print("Sistem menolak title tidak valid")


def test_update_article_invalid_image(client):
    print("\n[TEST CASE] Update Article - Image Invalid")

    create_article(client)

    payload = {
        "article_id": VALID_ID,
        "article_title": "Valid",
        "article_preview": "Valid",
        "article_content": "Valid",
        "article_tag": "tech",
        "article_image": "not_base64"
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/article/edit/update", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert "invalid image" in res.json()["confirmation"]

    print("[RESULT]")
    print("Sistem menolak image tidak valid")


# =========================
# VIEW ARTICLE
# =========================

def test_view_article_success(client):
    print("\n[TEST CASE] View Article - Success")

    create_article(client)

    payload = {"article_id": VALID_ID}

    print("[INPUT]")
    print(payload)

    res = client.post("/article/view", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Artikel berhasil ditampilkan")


def test_view_article_not_found(client):
    print("\n[TEST CASE] View Article - Not Found")

    payload = {"article_id": "invalid"}

    print("[INPUT]")
    print(payload)

    res = client.post("/article/view", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Artikel tidak ditemukan")


# =========================
# DELETE ARTICLE
# =========================

def test_delete_article_success(client):
    print("\n[TEST CASE] Delete Article - Success")

    create_article(client)

    payload = {"article_id": VALID_ID}

    print("[INPUT]")
    print(payload)

    res = client.post("/article/delete", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert "successful" in res.json()["confirmation"]

    print("[RESULT]")
    print("Artikel berhasil dihapus")


def test_delete_article_invalid_id(client):
    print("\n[TEST CASE] Delete Article - Invalid ID")

    payload = {"article_id": "invalid_id"}

    print("[INPUT]")
    print(payload)

    res = client.post("/article/delete", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Sistem menolak ID tidak valid")