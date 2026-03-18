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
    create_article(client)

    res = add_comment(client)

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "successful"
    assert "comments" in data


def test_add_comment_empty_content(client):
    create_article(client)

    res = add_comment(client, "")

    assert res.json()["confirmation"] == "backend error"


def test_add_comment_article_not_found(client):
    payload = {
        "article_id": "invalid",
        "comment_content": "isi",
        "parent_comment_id": None
    }

    res = client.post("/comment/add", json=payload)

    assert res.json()["confirmation"] == "backend error"


def test_add_comment_invalid_parent(client):
    create_article(client)

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "comment_content": "reply",
        "parent_comment_id": "invalid_id"
    }

    res = client.post("/comment/add", json=payload)

    assert res.json()["confirmation"] == "backend error"


# =========================
# EDIT COMMENT
# =========================

def test_edit_comment_success(client):
    create_article(client)
    add_comment(client)

    # ambil comment_id dari fake DB
    from services.comment_service import db
    comment_id = str(db.comment.comments[0]["_id"])

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "comment_id": comment_id,
        "comment_content": "Updated comment",
        "parent_comment_id": None
    }

    res = client.post("/comment/edit/update", json=payload)

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"


def test_edit_comment_invalid_content(client):
    create_article(client)
    add_comment(client)

    from services.comment_service import db
    comment_id = str(db.comment.comments[0]["_id"])

    payload = {
        "article_id": VALID_ARTICLE_ID,
        "comment_id": comment_id,
        "comment_content": "",  # ❌ invalid
        "parent_comment_id": None
    }

    res = client.post("/comment/edit/update", json=payload)

    assert res.json()["confirmation"] == "backend error"


# =========================
# EDIT GET COMMENT
# =========================

def test_get_comment_success(client):
    create_article(client)
    add_comment(client)

    from services.comment_service import db
    comment_id = str(db.comment.comments[0]["_id"])

    res = client.post("/comment/edit/get", json={
        "comment_id": comment_id
    })

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"


def test_get_comment_not_found(client):
    res = client.post("/comment/edit/get", json={
        "comment_id": "invalid"
    })

    assert res.json()["confirmation"] == "backend error"


# =========================
# DELETE COMMENT
# =========================

def test_delete_comment_success(client):
    create_article(client)
    add_comment(client)

    from services.comment_service import db
    comment_id = str(db.comment.comments[0]["_id"])

    res = client.post("/comment/delete", json={
        "comment_id": comment_id
    })

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"


def test_delete_comment_not_found(client):
    res = client.post("/comment/delete", json={
        "comment_id": "invalid"
    })

    assert res.json()["confirmation"] == "backend error"