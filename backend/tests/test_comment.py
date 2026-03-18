ARTICLE_ID = "675e8a1f2c4d3e8f9a1b2c3d"
COMMENT_ID_SEED = "693fd7e7255db70d804fbdfe"


def test_add_comment_success(client, auth_headers_user):
    print("\n[TEST CASE] Add Comment - Berhasil")
    response = client.post("/comment/add", json={
        "article_id": ARTICLE_ID,
        "comment_content": "This is a test comment.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    print(f"    confirmation: {response.json().get('confirmation')}")
    assert response.status_code == 200
    assert response.json()["confirmation"] == "successful"
    assert "comments" in response.json()


def test_add_comment_empty_content(client, auth_headers_user):
    print("\n[TEST CASE] Add Comment - Konten Kosong")
    response = client.post("/comment/add", json={
        "article_id": ARTICLE_ID,
        "comment_content": "",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_add_comment_invalid_article(client, auth_headers_user):
    print("\n[TEST CASE] Add Comment - Article Tidak Ada")
    response = client.post("/comment/add", json={
        "article_id": "000000000000000000000000",
        "comment_content": "This is a test comment.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_add_comment_no_token(client):
    print("\n[TEST CASE] Add Comment - Tanpa Token")
    response = client.post("/comment/add", json={
        "article_id": ARTICLE_ID,
        "comment_content": "No token comment."
    })
    assert response.status_code == 401


def test_add_reply_comment(client, auth_headers_user):
    print("\n[TEST CASE] Add Comment - Reply ke Komentar")
    response = client.post("/comment/add", json={
        "article_id": ARTICLE_ID,
        "comment_content": "This is a reply.",
        "parent_comment_id": COMMENT_ID_SEED
    }, headers=auth_headers_user)
    print(f"    confirmation: {response.json().get('confirmation')}")
    assert response.json()["confirmation"] == "successful"


def test_add_reply_invalid_parent(client, auth_headers_user):
    print("\n[TEST CASE] Add Comment - Parent Tidak Ada")
    response = client.post("/comment/add", json={
        "article_id": ARTICLE_ID,
        "comment_content": "Reply to nonexistent.",
        "parent_comment_id": "000000000000000000000000"
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_edit_get_comment_not_owner(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Get Comment - Bukan Pemilik")
    response = client.post("/comment/edit/get", json={
        "comment_id": COMMENT_ID_SEED
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


def test_delete_comment_admin_can_delete(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Delete Comment - Admin Bisa Hapus Komentar User Lain")
    add_resp = client.post("/comment/add", json={
        "article_id": ARTICLE_ID,
        "comment_content": "Comment to be deleted by admin.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    assert add_resp.json()["confirmation"] == "successful"

    comments = add_resp.json()["comments"]
    target = next((c for c in comments if c["comment_content"] == "Comment to be deleted by admin."), None)
    assert target is not None

    del_resp = client.post("/comment/delete", json={
        "comment_id": target["comment_id"]
    }, headers=auth_headers_admin)
    print(f"    confirmation: {del_resp.json().get('confirmation')}")
    assert del_resp.json()["confirmation"] == "successful"
