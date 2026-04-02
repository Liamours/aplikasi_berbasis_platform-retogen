# ── existing tests ────────────────────────────────────────────────────────────

def test_add_comment_success(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Comment - Berhasil")
    response = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "This is a test comment.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    assert response.status_code == 200
    assert response.json()["confirmation"] == "successful"
    assert "comments" in response.json()


def test_add_comment_empty_content(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Comment - Konten Kosong")
    response = client.post("/comment/add", json={
        "article_id": article_id,
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


def test_add_comment_no_token(client, article_id):
    print("\n[TEST CASE] Add Comment - Tanpa Token")
    response = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "No token comment."
    })
    assert response.status_code == 401


def test_add_reply_comment(client, auth_headers_user, article_id, seed_comment_id):
    print("\n[TEST CASE] Add Comment - Reply ke Komentar")
    response = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "This is a reply.",
        "parent_comment_id": seed_comment_id
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "successful"


def test_add_reply_invalid_parent(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Comment - Parent Tidak Ada")
    response = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "Reply to nonexistent.",
        "parent_comment_id": "000000000000000000000000"
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_edit_get_comment_not_owner(client, auth_headers_admin, seed_comment_id):
    print("\n[TEST CASE] Edit Get Comment - Bukan Pemilik")
    response = client.post("/comment/edit/get", json={
        "comment_id": seed_comment_id
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


def test_delete_comment_admin_can_delete(client, auth_headers_user, auth_headers_admin, article_id):
    print("\n[TEST CASE] Delete Comment - Admin Bisa Hapus Komentar User Lain")
    add_resp = client.post("/comment/add", json={
        "article_id": article_id,
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
    assert del_resp.json()["confirmation"] == "successful"


# ── new tests: add comment ────────────────────────────────────────────────────

def test_add_comment_single_char_content(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Comment - Single Char Content")
    response = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "X",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "successful"


def test_add_comment_content_max_length_8192(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Comment - Content Max Length 8192 (Boundary)")
    response = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "A" * 8192,
        "parent_comment_id": None
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "successful"


def test_add_comment_content_over_max(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Comment - Content Over Max (8193 chars)")
    response = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "A" * 8193,
        "parent_comment_id": None
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_add_comment_admin_can_comment(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Add Comment - Admin Juga Bisa Komentar")
    response = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "Admin comment here.",
        "parent_comment_id": None
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful"


def test_add_comment_returns_comment_list(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Comment - Response Contains Comments List")
    response = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "Checking comment list in response.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    assert isinstance(response.json().get("comments"), list)


def test_add_comment_malformed_article_id(client, auth_headers_user):
    print("\n[TEST CASE] Add Comment - Malformed Article ID")
    response = client.post("/comment/add", json={
        "article_id": "not-a-valid-id",
        "comment_content": "Test comment.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_add_reply_to_reply(client, auth_headers_user, article_id, seed_comment_id):
    print("\n[TEST CASE] Add Comment - Reply to a Reply (Nested)")
    first_reply = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "First level reply.",
        "parent_comment_id": seed_comment_id
    }, headers=auth_headers_user)
    assert first_reply.json()["confirmation"] == "successful"

    comments = first_reply.json()["comments"]
    nested_parent = next((c for c in comments if c["comment_content"] == "First level reply."), None)
    assert nested_parent is not None

    second_reply = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "Second level reply.",
        "parent_comment_id": nested_parent["comment_id"]
    }, headers=auth_headers_user)
    assert second_reply.json()["confirmation"] == "successful"


# ── new tests: edit comment ───────────────────────────────────────────────────

def test_edit_comment_success(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Comment - Berhasil")
    add_resp = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "Original comment for edit.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    comments = add_resp.json()["comments"]
    target = next((c for c in comments if c["comment_content"] == "Original comment for edit."), None)
    assert target is not None

    edit_resp = client.post("/comment/edit/update", json={
        "comment_id": target["comment_id"],
        "article_id": article_id,
        "comment_content": "Edited comment content."
    }, headers=auth_headers_user)
    assert edit_resp.json()["confirmation"] == "successful"


def test_edit_comment_empty_content(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Comment - Content Kosong")
    add_resp = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "Comment before empty edit.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    comments = add_resp.json()["comments"]
    target = next((c for c in comments if c["comment_content"] == "Comment before empty edit."), None)
    if target is None:
        return

    edit_resp = client.post("/comment/edit/update", json={
        "comment_id": target["comment_id"],
        "article_id": article_id,
        "comment_content": ""
    }, headers=auth_headers_user)
    assert edit_resp.json()["confirmation"] == "backend error"


def test_edit_comment_over_max_length(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Comment - Content Over Max (8193 chars)")
    add_resp = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "Comment before long edit.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    comments = add_resp.json()["comments"]
    target = next((c for c in comments if c["comment_content"] == "Comment before long edit."), None)
    if target is None:
        return

    edit_resp = client.post("/comment/edit/update", json={
        "comment_id": target["comment_id"],
        "article_id": article_id,
        "comment_content": "A" * 8193
    }, headers=auth_headers_user)
    assert edit_resp.json()["confirmation"] == "backend error"


def test_edit_comment_no_token(client, seed_comment_id, article_id):
    print("\n[TEST CASE] Edit Comment - Tanpa Token")
    response = client.post("/comment/edit/update", json={
        "comment_id": seed_comment_id,
        "article_id": article_id,
        "comment_content": "Some content"
    })
    assert response.status_code == 401


def test_edit_comment_invalid_id(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Comment - Comment ID Tidak Ada")
    response = client.post("/comment/edit/update", json={
        "comment_id": "000000000000000000000000",
        "article_id": article_id,
        "comment_content": "Updated content"
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_edit_comment_not_owner(client, auth_headers_admin, seed_comment_id, article_id):
    print("\n[TEST CASE] Edit Comment - Bukan Pemilik")
    response = client.post("/comment/edit/update", json={
        "comment_id": seed_comment_id,
        "article_id": article_id,
        "comment_content": "Admin trying to edit user comment"
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


# ── new tests: edit/get comment ───────────────────────────────────────────────

def test_edit_get_comment_owner_success(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Get Comment - Owner Berhasil")
    add_resp = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "Comment for get test.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    comments = add_resp.json()["comments"]
    target = next((c for c in comments if c["comment_content"] == "Comment for get test."), None)
    assert target is not None

    get_resp = client.post("/comment/edit/get", json={
        "comment_id": target["comment_id"]
    }, headers=auth_headers_user)
    assert get_resp.json()["confirmation"] == "successful"
    assert "comment_content" in get_resp.json()


def test_edit_get_comment_no_token(client, seed_comment_id):
    print("\n[TEST CASE] Edit Get Comment - Tanpa Token")
    response = client.post("/comment/edit/get", json={"comment_id": seed_comment_id})
    assert response.status_code == 401


# ── new tests: delete comment ─────────────────────────────────────────────────

def test_delete_comment_no_token(client, seed_comment_id):
    print("\n[TEST CASE] Delete Comment - Tanpa Token")
    response = client.post("/comment/delete", json={"comment_id": seed_comment_id})
    assert response.status_code == 401


def test_delete_comment_invalid_id(client, auth_headers_admin):
    print("\n[TEST CASE] Delete Comment - Comment ID Tidak Ada")
    response = client.post("/comment/delete", json={"comment_id": "000000000000000000000000"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


def test_delete_comment_not_owner_regular_user(client, auth_headers_user, auth_headers_admin, article_id):
    print("\n[TEST CASE] Delete Comment - User Biasa Tidak Bisa Hapus Komentar Orang Lain")
    add_resp = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "Comment owned by admin.",
        "parent_comment_id": None
    }, headers=auth_headers_admin)
    comments = add_resp.json()["comments"]
    target = next((c for c in comments if c["comment_content"] == "Comment owned by admin."), None)
    assert target is not None

    del_resp = client.post("/comment/delete", json={
        "comment_id": target["comment_id"]
    }, headers=auth_headers_user)
    assert del_resp.json()["confirmation"] == "backend error"


def test_delete_comment_owner_can_delete_own(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Delete Comment - Owner Bisa Hapus Komentarnya Sendiri")
    add_resp = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "User deletes their own comment.",
        "parent_comment_id": None
    }, headers=auth_headers_user)
    comments = add_resp.json()["comments"]
    target = next((c for c in comments if c["comment_content"] == "User deletes their own comment."), None)
    assert target is not None

    del_resp = client.post("/comment/delete", json={
        "comment_id": target["comment_id"]
    }, headers=auth_headers_user)
    assert del_resp.json()["confirmation"] == "successful"
