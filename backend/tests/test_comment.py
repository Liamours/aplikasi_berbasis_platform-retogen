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


def add_comment(client, content="Komentar pertama"):
    payload = {
        "article_id": VALID_ARTICLE_ID,
        "comment_content": content,
        "parent_comment_id": None
    }
    return client.post("/comment/add", json=payload)


# =========================
# ADD COMMENT
# =========================

def test_add_comment_success(client):
    print("\n[TEST CASE] Add Comment - Success")

    create_article(client)

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "comment_content": "Komentar pertama",
        "parent_comment_id": None
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/comment/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Komentar berhasil ditambahkan")


def test_add_comment_empty_content(client):
    print("\n[TEST CASE] Add Comment - Content Kosong")

    create_article(client)

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "comment_content": "",
        "parent_comment_id": None
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/comment/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Sistem menolak komentar kosong")


def test_add_comment_article_not_found(client):
    print("\n[TEST CASE] Add Comment - Article Tidak Ditemukan")

    payload = {
        "article_id": "invalid",
        "comment_content": "isi",
        "parent_comment_id": None
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/comment/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Sistem menolak karena artikel tidak ditemukan")


def test_add_comment_invalid_parent(client):
    print("\n[TEST CASE] Add Comment - Parent Invalid")

    create_article(client)

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "comment_content": "reply",
        "parent_comment_id": "invalid_id"
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/comment/add", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Sistem menolak parent comment tidak valid")


# =========================
# EDIT COMMENT
# =========================

def test_edit_comment_success(client):
    print("\n[TEST CASE] Edit Comment - Success")

    create_article(client)
    add_comment(client)

    from services.comment_service import db
    comment_id = str(db.comment.comments[0]["_id"])

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "comment_id": comment_id,
        "comment_content": "Updated comment",
        "parent_comment_id": None
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/comment/edit/update", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Komentar berhasil diupdate")


def test_edit_comment_invalid_content(client):
    print("\n[TEST CASE] Edit Comment - Content Invalid")

    create_article(client)
    add_comment(client)

    from services.comment_service import db
    comment_id = str(db.comment.comments[0]["_id"])

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "comment_id": comment_id,
        "comment_content": "",
        "parent_comment_id": None
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/comment/edit/update", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Sistem menolak update komentar kosong")


# =========================
# GET COMMENT
# =========================

def test_get_comment_success(client):
    print("\n[TEST CASE] Get Comment - Success")

    create_article(client)
    add_comment(client)

    from services.comment_service import db
    comment_id = str(db.comment.comments[0]["_id"])

    payload = {"comment_id": comment_id}

    print("[INPUT]")
    print(payload)

    res = client.post("/comment/edit/get", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Komentar berhasil diambil")


def test_get_comment_not_found(client):
    print("\n[TEST CASE] Get Comment - Not Found")

    payload = {"comment_id": "invalid"}

    print("[INPUT]")
    print(payload)

    res = client.post("/comment/edit/get", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Komentar tidak ditemukan")


# =========================
# DELETE COMMENT
# =========================

def test_delete_comment_success(client):
    print("\n[TEST CASE] Delete Comment - Success")

    create_article(client)
    add_comment(client)

    from services.comment_service import db
    comment_id = str(db.comment.comments[0]["_id"])

    payload = {"comment_id": comment_id}

    print("[INPUT]")
    print(payload)

    res = client.post("/comment/delete", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Komentar berhasil dihapus")


def test_delete_comment_not_found(client):
    print("\n[TEST CASE] Delete Comment - Not Found")

    payload = {"comment_id": "invalid"}

    print("[INPUT]")
    print(payload)

    res = client.post("/comment/delete", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "backend error"

    print("[RESULT]")
    print("Komentar tidak ditemukan")