from bson import ObjectId

VALID_ARTICLE_ID = "507f1f77bcf86cd799439011"


# =========================
# HELPER
# =========================

def create_article(client):
    payload = {
        "article_title": "Judul Test",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tag": "tech",
        "article_image": "aGVsbG8="
    }
    client.post("/article/add", json=payload)


def add_rating(client, value=5):
    payload = {
        "article_id": VALID_ARTICLE_ID,
        "rating_value": value
    }
    return client.post("/rating/add", json=payload)


# =========================
# ADD RATING
# =========================

def test_add_rating_success(client):
    print("\n[TEST CASE] Add Rating - Success")

    create_article(client)

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "rating_value": 5
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/rating/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Rating berhasil ditambahkan")


def test_add_rating_invalid_value(client):
    print("\n[TEST CASE] Add Rating - Value Tidak Valid")

    create_article(client)

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "rating_value": 10
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/rating/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 422

    print("[RESULT]")
    print("Sistem menolak nilai rating tidak valid")


def test_add_rating_article_not_found(client):
    print("\n[TEST CASE] Add Rating - Article Tidak Ditemukan")

    payload = {
        "article_id": "invalid",
        "rating_value": 5
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/rating/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Sistem menolak karena artikel tidak ditemukan")


def test_add_rating_already_rated(client):
    print("\n[TEST CASE] Add Rating - Sudah Pernah Rating")

    create_article(client)

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "rating_value": 5
    }

    add_rating(client)

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/rating/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "already rated"

    print("[RESULT]")
    print("Sistem menolak duplicate rating")


# =========================
# GET RATING
# =========================

def test_get_rating_success(client):
    print("\n[TEST CASE] Get Rating - Success")

    create_article(client)
    add_rating(client)

    from services.rating_service import db
    rating_id = str(db.rating.ratings[0]["_id"])

    payload = {
        "rating_id": rating_id,
        "article_id": VALID_ARTICLE_ID
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/rating/edit/get", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Rating berhasil diambil")


def test_get_rating_not_found(client):
    print("\n[TEST CASE] Get Rating - Not Found")

    payload = {
        "rating_id": "invalid",
        "article_id": VALID_ARTICLE_ID
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/rating/edit/get", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Rating tidak ditemukan")


# =========================
# UPDATE RATING
# =========================

def test_edit_rating_success(client):
    print("\n[TEST CASE] Edit Rating - Success")

    create_article(client)
    add_rating(client)

    from services.rating_service import db
    rating_id = str(db.rating.ratings[0]["_id"])

    payload = {
        "rating_id": rating_id,
        "article_id": VALID_ARTICLE_ID,
        "rating_value": 4
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/rating/edit/update", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Rating berhasil diupdate")


def test_edit_rating_invalid_value(client):
    print("\n[TEST CASE] Edit Rating - Value Invalid")

    create_article(client)
    add_rating(client)

    from services.rating_service import db
    rating_id = str(db.rating.ratings[0]["_id"])

    payload = {
        "rating_id": rating_id,
        "article_id": VALID_ARTICLE_ID,
        "rating_value": 10
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/rating/edit/update", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Sistem menolak nilai rating tidak valid")


def test_edit_rating_not_found(client):
    print("\n[TEST CASE] Edit Rating - Not Found")

    payload = {
        "rating_id": "invalid",
        "article_id": VALID_ARTICLE_ID,
        "rating_value": 4
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/rating/edit/update", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Rating tidak ditemukan")