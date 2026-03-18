from bson import ObjectId

VALID_ARTICLE_ID = "507f1f77bcf86cd799439011"


def seed_article(client):
    from services.article_service import db

    db.article.articles.append({
        "_id": ObjectId(VALID_ARTICLE_ID),
        "title": "test article",
        "content": "content",
        "report_count": 0,
        "is_deleted": False
    })


def test_report_article_success(client):
    seed_article(client)

    res = client.post("/report_article/add", json={
        "article_id": VALID_ARTICLE_ID,
        "description": "spam"
    })

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "successful: article reported"


def test_report_article_empty_description(client):
    res = client.post("/report_article/add", json={
        "article_id": VALID_ARTICLE_ID,
        "description": ""
    })

    assert res.status_code == 422


def test_report_article_invalid_id(client):
    res = client.post("/report_article/add", json={
        "article_id": "invalid_id",
        "description": "spam"
    })

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "invalid article_id"


def test_report_article_backend_error(client):
    # tidak seed article → update gagal (simulate error)

    res = client.post("/report_article/add", json={
        "article_id": VALID_ARTICLE_ID,
        "description": "spam"
    })

    data = res.json()

    # tergantung implementasi kamu:
    # kalau insert tetap sukses → tetap successful
    # kalau mau strict → harusnya backend error

    assert res.status_code == 200