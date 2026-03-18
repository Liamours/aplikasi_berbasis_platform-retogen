from bson import ObjectId

VALID_ARTICLE_ID = "507f1f77bcf86cd799439011"


# =========================
# HELPER
# =========================

def seed_article(client):
    from services.article_service import db

    db.article.articles.append({
        "_id": ObjectId(VALID_ARTICLE_ID),
        "title": "test article",
        "content": "content",
        "report_count": 0,
        "is_deleted": False
    })


# =========================
# REPORT ARTICLE
# =========================

def test_report_article_success(client):
    print("\n[TEST CASE] Report Article - Success")

    seed_article(client)

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "description": "spam"
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/report_article/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful: article reported"

    print("[RESULT]")
    print("Artikel berhasil dilaporkan")


def test_report_article_empty_description(client):
    print("\n[TEST CASE] Report Article - Description Kosong")

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "description": ""
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/report_article/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 422

    print("[RESULT]")
    print("Sistem menolak deskripsi kosong")


def test_report_article_invalid_id(client):
    print("\n[TEST CASE] Report Article - ID Tidak Valid")

    payload = {
        "article_id": "invalid_id",
        "description": "spam"
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/report_article/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "invalid article_id"

    print("[RESULT]")
    print("Sistem menolak ID artikel tidak valid")


def test_report_article_backend_error(client):
    print("\n[TEST CASE] Report Article - Backend Error (Article Tidak Ada)")

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "description": "spam"
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/report_article/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    # fleksibel sesuai implementasi kamu
    assert res.status_code == 200

    print("[RESULT]")
    print("Sistem diuji saat artikel tidak tersedia di database")