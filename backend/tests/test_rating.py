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
    create_article(client)

    res = add_rating(client)

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "successful"
    assert "ratings" in data


def test_add_rating_invalid_value(client):
    create_article(client)

    res = add_rating(client, 10)

    assert res.status_code == 422


def test_add_rating_article_not_found(client):
    payload = {
        "article_id": "invalid",
        "rating_value": 5
    }

    res = client.post("/rating/add", json=payload)

    assert res.json()["confirmation"] == "backend error"


def test_add_rating_already_rated(client):
    create_article(client)

    add_rating(client)
    res = add_rating(client)  # rating kedua

    assert res.json()["confirmation"] == "already rated"


# =========================
# EDIT GET RATING
# =========================

def test_get_rating_success(client):
    create_article(client)
    add_rating(client)

    from services.rating_service import db
    rating_id = str(db.rating.ratings[0]["_id"])

    res = client.post("/rating/edit/get", json={
        "rating_id": rating_id,
        "article_id": VALID_ARTICLE_ID
    })

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"


def test_get_rating_not_found(client):
    res = client.post("/rating/edit/get", json={
        "rating_id": "invalid",
        "article_id": VALID_ARTICLE_ID
    })

    assert res.json()["confirmation"] == "backend error"


# =========================
# EDIT UPDATE RATING
# =========================

def test_edit_rating_success(client):
    create_article(client)
    add_rating(client)

    from services.rating_service import db
    rating_id = str(db.rating.ratings[0]["_id"])

    payload = {
        "rating_id": rating_id,
        "article_id": VALID_ARTICLE_ID,
        "rating_value": 4
    }

    res = client.post("/rating/edit/update", json=payload)

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"


def test_edit_rating_invalid_value(client):
    create_article(client)
    add_rating(client)

    from services.rating_service import db
    rating_id = str(db.rating.ratings[0]["_id"])

    payload = {
        "rating_id": rating_id,
        "article_id": VALID_ARTICLE_ID,
        "rating_value": 10  # ❌ invalid
    }

    res = client.post("/rating/edit/update", json=payload)

    assert res.json()["confirmation"] == "backend error"


def test_edit_rating_not_found(client):
    create_article(client)

    payload = {
        "rating_id": "invalid",
        "article_id": VALID_ARTICLE_ID,
        "rating_value": 4
    }

    res = client.post("/rating/edit/update", json=payload)

    assert res.json()["confirmation"] == "backend error"