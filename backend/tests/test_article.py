import base64

ARTICLE_ID = "675e8a1f2c4d3e8f9a1b2c3d"
SMALL_IMAGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="
INVALID_IMAGE_B64 = "dGhpcyBpcyBub3QgYW4gaW1hZ2U="  # valid base64 but not PNG/JPEG bytes


# ── helpers ──────────────────────────────────────────────────────────────────

def _add_temp_article(client, headers, title="Temp Delete Test Article"):
    payload = {
        "article_title": title,
        "article_preview": "Temp preview for test",
        "article_content": "Temp content for test",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    client.post("/article/add", json=payload, headers=headers)
    resp = client.post(
        "/article/main_page",
        json={"sort": "search_title", "search": title},
        headers=headers,
    )
    for a in resp.json().get("list_article", []):
        if a["article_title"] == title:
            return a["article_id"]
    return None


# ── existing tests ────────────────────────────────────────────────────────────

def test_main_page_default(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Default (Newest)")
    response = client.post("/article/main_page", json={}, headers=auth_headers_user)
    print(f"    confirmation: {response.json().get('confirmation')}")
    print(f"    article count: {len(response.json().get('list_article', []))}")
    assert response.status_code == 200
    assert response.json()["confirmation"] == "fetch data successful"
    assert isinstance(response.json()["list_article"], list)


def test_main_page_sort_oldest(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Sort Oldest")
    response = client.post("/article/main_page", json={"sort": "oldest"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "fetch data successful"
    assert response.json()["sort"] == "oldest"


def test_main_page_sort_most_reported(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Sort Most Reported")
    response = client.post("/article/main_page", json={"sort": "most_reported"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "fetch data successful"


def test_main_page_sort_highest_rated(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Sort Highest Rated")
    response = client.post("/article/main_page", json={"sort": "highest_rated"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "fetch data successful"


def test_main_page_sort_most_commented(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Sort Most Commented")
    response = client.post("/article/main_page", json={"sort": "most_commented"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "fetch data successful"


def test_main_page_filter_by_tag(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Filter by Tag")
    response = client.post("/article/main_page", json={"sort": "by_tag", "tag": "productivity"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "fetch data successful"
    for a in response.json()["list_article"]:
        assert a["article_tag"] == "productivity"


def test_main_page_search_title(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Search by Title")
    response = client.post("/article/main_page", json={"sort": "search_title", "search": "Dell"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "fetch data successful"
    for a in response.json()["list_article"]:
        assert "dell" in a["article_title"].lower()


def test_main_page_no_token(client):
    print("\n[TEST CASE] Main Page - Tanpa Token")
    response = client.post("/article/main_page", json={})
    assert response.status_code == 401


def test_view_article_success(client, auth_headers_user):
    print("\n[TEST CASE] View Article - Berhasil")
    response = client.post("/article/view", json={"article_id": ARTICLE_ID}, headers=auth_headers_user)
    print(f"    confirmation: {response.json().get('confirmation')}")
    assert response.status_code == 200
    assert response.json()["confirmation"] == "successful"
    assert "article_title" in response.json()


def test_view_article_invalid_id(client, auth_headers_user):
    print("\n[TEST CASE] View Article - ID Tidak Valid")
    response = client.post("/article/view", json={"article_id": "000000000000000000000000"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_view_article_no_token(client):
    print("\n[TEST CASE] View Article - Tanpa Token")
    response = client.post("/article/view", json={"article_id": ARTICLE_ID})
    assert response.status_code == 401


def test_add_article_success(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Admin Berhasil")
    payload = {
        "article_title": "Test Article Title",
        "article_preview": "Test preview text here",
        "article_content": "Test content body here for the article.",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    print(f"    response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["confirmation"] == "success: article added"


def test_add_article_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Add Article - User Biasa Ditolak")
    payload = {
        "article_title": "Test Article Title",
        "article_preview": "Test preview text here",
        "article_content": "Test content body here.",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_user)
    print(f"    response: {response.json()}")
    assert response.json()["confirmation"] == "not admin"


def test_add_article_title_too_long(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Judul Terlalu Panjang")
    payload = {
        "article_title": "A" * 257,
        "article_preview": "Test preview",
        "article_content": "Test content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert "Title must be" in response.json()["confirmation"]


def test_verification_admin(client, auth_headers_admin):
    print("\n[TEST CASE] Verification - Admin")
    response = client.post("/article/verification", headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful"


def test_verification_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Verification - User Biasa Ditolak")
    response = client.post("/article/verification", headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


# ── new tests: main_page ──────────────────────────────────────────────────────

def test_main_page_sort_by_tag_without_tag_param(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - by_tag without tag param")
    response = client.post("/article/main_page", json={"sort": "by_tag"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "fetch data successful"
    assert isinstance(response.json()["list_article"], list)


def test_main_page_search_no_results(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Search No Results")
    response = client.post("/article/main_page", json={"sort": "search_title", "search": "XYZZZNOTEXIST999"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "fetch data successful"
    assert response.json()["list_article"] == []


def test_main_page_invalid_token(client):
    print("\n[TEST CASE] Main Page - Invalid Token")
    response = client.post("/article/main_page", json={}, headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401


def test_main_page_image_is_valid_base64(client, auth_headers_admin):
    print("\n[TEST CASE] Main Page - Image is valid base64 (not latin1)")
    client.post("/article/add", json={
        "article_title": "Base64 Image Test Article",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64
    }, headers=auth_headers_admin)
    response = client.post("/article/main_page", json={"sort": "search_title", "search": "Base64 Image Test Article"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "fetch data successful"
    for a in response.json()["list_article"]:
        if a.get("article_image"):
            try:
                base64.b64decode(a["article_image"])
            except Exception:
                assert False, "article_image is not valid base64"


def test_main_page_all_articles_have_required_fields(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - All Articles Have Required Fields")
    response = client.post("/article/main_page", json={}, headers=auth_headers_user)
    for a in response.json()["list_article"]:
        assert "article_id" in a
        assert "article_title" in a
        assert "article_preview" in a
        assert "article_tag" in a


def test_main_page_returns_username(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Returns Username")
    response = client.post("/article/main_page", json={}, headers=auth_headers_user)
    assert "username" in response.json()
    assert response.json()["username"] != ""


def test_main_page_search_case_insensitive(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Search Case Insensitive")
    resp_lower = client.post("/article/main_page", json={"sort": "search_title", "search": "dell"}, headers=auth_headers_user)
    resp_upper = client.post("/article/main_page", json={"sort": "search_title", "search": "DELL"}, headers=auth_headers_user)
    assert resp_lower.json()["confirmation"] == "fetch data successful"
    assert resp_upper.json()["confirmation"] == "fetch data successful"
    assert len(resp_lower.json()["list_article"]) == len(resp_upper.json()["list_article"])


# ── new tests: view article ───────────────────────────────────────────────────

def test_view_article_has_comments_field(client, auth_headers_user):
    print("\n[TEST CASE] View Article - Has Comments Field")
    response = client.post("/article/view", json={"article_id": ARTICLE_ID}, headers=auth_headers_user)
    assert "comments" in response.json()
    assert isinstance(response.json()["comments"], list)


def test_view_article_has_ratings_field(client, auth_headers_user):
    print("\n[TEST CASE] View Article - Has Ratings Field")
    response = client.post("/article/view", json={"article_id": ARTICLE_ID}, headers=auth_headers_user)
    assert "ratings" in response.json()
    assert isinstance(response.json()["ratings"], list)


def test_view_article_has_reports_field_admin(client, auth_headers_admin):
    print("\n[TEST CASE] View Article - Admin Sees Reports Field")
    response = client.post("/article/view", json={"article_id": ARTICLE_ID}, headers=auth_headers_admin)
    assert "reports" in response.json()
    assert isinstance(response.json()["reports"], list)


def test_view_article_userclass_is_user(client, auth_headers_user):
    print("\n[TEST CASE] View Article - Userclass Is 'user'")
    response = client.post("/article/view", json={"article_id": ARTICLE_ID}, headers=auth_headers_user)
    assert response.json()["userclass"] == "user"


def test_view_article_userclass_is_admin(client, auth_headers_admin):
    print("\n[TEST CASE] View Article - Userclass Is 'admin'")
    response = client.post("/article/view", json={"article_id": ARTICLE_ID}, headers=auth_headers_admin)
    assert response.json()["userclass"] == "admin"


def test_view_article_malformed_id(client, auth_headers_user):
    print("\n[TEST CASE] View Article - Malformed ID (non-hex)")
    response = client.post("/article/view", json={"article_id": "not-a-valid-objectid"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_view_article_has_correct_fields(client, auth_headers_user):
    print("\n[TEST CASE] View Article - Has All Correct Fields")
    response = client.post("/article/view", json={"article_id": ARTICLE_ID}, headers=auth_headers_user)
    data = response.json()
    for field in ("confirmation", "userclass", "user_email", "username", "article_title", "article_content", "article_tag", "comments", "ratings"):
        assert field in data, f"Missing field: {field}"


# ── new tests: edit/get ───────────────────────────────────────────────────────

def test_edit_get_success_admin(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Get - Admin Berhasil")
    response = client.post("/article/edit/get", json={"article_id": ARTICLE_ID}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful"
    assert "article_title" in response.json()
    assert "article_content" in response.json()


def test_edit_get_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Edit Get - User Biasa Ditolak (FIX: admin check first)")
    response = client.post("/article/edit/get", json={"article_id": ARTICLE_ID}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_edit_get_no_token(client):
    print("\n[TEST CASE] Edit Get - Tanpa Token")
    response = client.post("/article/edit/get", json={"article_id": ARTICLE_ID})
    assert response.status_code == 401


def test_edit_get_invalid_article_id(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Get - Article ID Tidak Ditemukan")
    response = client.post("/article/edit/get", json={"article_id": "000000000000000000000000"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


def test_edit_get_malformed_article_id(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Get - Article ID Malformed")
    response = client.post("/article/edit/get", json={"article_id": "not-a-valid-id"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


# ── new tests: edit/update ────────────────────────────────────────────────────

def test_edit_update_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Edit Update - User Biasa Ditolak (FIX: admin check added)")
    payload = {
        "article_id": ARTICLE_ID,
        "article_title": "Updated Title",
        "article_preview": "Updated preview",
        "article_content": "Updated content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_edit_update_no_token(client):
    print("\n[TEST CASE] Edit Update - Tanpa Token")
    payload = {
        "article_id": ARTICLE_ID,
        "article_title": "Updated Title",
        "article_preview": "Updated preview",
        "article_content": "Updated content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload)
    assert response.status_code == 401


def test_edit_update_invalid_article_id(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Update - Article Tidak Ditemukan")
    payload = {
        "article_id": "000000000000000000000000",
        "article_title": "Updated Title",
        "article_preview": "Updated preview",
        "article_content": "Updated content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


def test_edit_update_title_empty(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Update - Judul Kosong")
    payload = {
        "article_id": ARTICLE_ID,
        "article_title": "",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert "Title must be" in response.json()["confirmation"]


def test_edit_update_preview_too_long(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Update - Preview Terlalu Panjang")
    payload = {
        "article_id": ARTICLE_ID,
        "article_title": "Valid Title",
        "article_preview": "P" * 129,
        "article_content": "Content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert "Preview must be" in response.json()["confirmation"]


def test_edit_update_content_too_long(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Update - Content Terlalu Panjang")
    payload = {
        "article_id": ARTICLE_ID,
        "article_title": "Valid Title",
        "article_preview": "Valid preview",
        "article_content": "C" * 65537,
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert "Content must be" in response.json()["confirmation"]


def test_edit_update_invalid_image(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Update - Invalid Image Bytes (not PNG/JPEG)")
    payload = {
        "article_id": ARTICLE_ID,
        "article_title": "Valid Title",
        "article_preview": "Valid preview",
        "article_content": "Valid content",
        "article_tag": "gaming",
        "article_image": INVALID_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert "invalid image" in response.json()["confirmation"].lower()


def test_edit_update_admin_success(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Update - Admin Berhasil")
    payload = {
        "article_id": ARTICLE_ID,
        "article_title": "Updated Title by Admin",
        "article_preview": "Updated preview",
        "article_content": "Updated content body",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful: article edited"


def test_edit_update_title_exactly_256(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Update - Title Exactly 256 Chars (Boundary)")
    payload = {
        "article_id": ARTICLE_ID,
        "article_title": "A" * 256,
        "article_preview": "Valid preview",
        "article_content": "Valid content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful: article edited"


# ── new tests: add article ────────────────────────────────────────────────────

def test_add_article_preview_too_long(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Preview Terlalu Panjang")
    payload = {
        "article_title": "Valid Title",
        "article_preview": "P" * 129,
        "article_content": "Valid content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert "Preview must be" in response.json()["confirmation"]


def test_add_article_content_too_long(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Content Terlalu Panjang")
    payload = {
        "article_title": "Valid Title",
        "article_preview": "Valid preview",
        "article_content": "C" * 65537,
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert "Content must be" in response.json()["confirmation"]


def test_add_article_invalid_image(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Invalid Image Bytes")
    payload = {
        "article_title": "Valid Title",
        "article_preview": "Valid preview",
        "article_content": "Valid content",
        "article_tag": "gaming",
        "article_image": INVALID_IMAGE_B64,
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert "image" in response.json()["confirmation"].lower()


def test_add_article_no_token(client):
    print("\n[TEST CASE] Add Article - Tanpa Token")
    payload = {
        "article_title": "Valid Title",
        "article_preview": "Valid preview",
        "article_content": "Valid content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/add", json=payload)
    assert response.status_code == 401


def test_add_article_empty_title(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Judul Kosong")
    payload = {
        "article_title": "",
        "article_preview": "Valid preview",
        "article_content": "Valid content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert "Title must be" in response.json()["confirmation"]


def test_add_article_title_exactly_256(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Judul Exactly 256 Chars (Boundary)")
    payload = {
        "article_title": "B" * 256,
        "article_preview": "Valid preview",
        "article_content": "Valid content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "success: article added"


def test_add_article_image_stored_as_binary_and_retrievable(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Image Stored as Binary and Retrievable (FIX)")
    payload = {
        "article_title": "Binary Image Storage Test",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tag": "gaming",
        "article_image": SMALL_IMAGE_B64,
    }
    client.post("/article/add", json=payload, headers=auth_headers_admin)
    resp = client.post("/article/main_page", json={"sort": "search_title", "search": "Binary Image Storage Test"}, headers=auth_headers_admin)
    articles = resp.json().get("list_article", [])
    found = next((a for a in articles if a["article_title"] == "Binary Image Storage Test"), None)
    assert found is not None
    if found.get("article_image"):
        decoded = base64.b64decode(found["article_image"])
        assert len(decoded) > 0


# ── new tests: delete article ─────────────────────────────────────────────────

def test_delete_article_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Delete Article - User Biasa Ditolak")
    response = client.post("/article/delete", json={"article_id": ARTICLE_ID}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_delete_article_no_token(client):
    print("\n[TEST CASE] Delete Article - Tanpa Token")
    response = client.post("/article/delete", json={"article_id": ARTICLE_ID})
    assert response.status_code == 401


def test_delete_article_invalid_id(client, auth_headers_admin):
    print("\n[TEST CASE] Delete Article - ID Tidak Ditemukan")
    response = client.post("/article/delete", json={"article_id": "000000000000000000000000"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


def test_delete_article_malformed_id(client, auth_headers_admin):
    print("\n[TEST CASE] Delete Article - ID Malformed")
    response = client.post("/article/delete", json={"article_id": "not-valid"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


def test_delete_article_admin_success(client, auth_headers_admin):
    print("\n[TEST CASE] Delete Article - Admin Berhasil")
    article_id = _add_temp_article(client, auth_headers_admin, "Article To Be Deleted By Admin")
    assert article_id is not None, "Could not create temp article for delete test"
    response = client.post("/article/delete", json={"article_id": article_id}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful: article deleted"


def test_delete_article_then_view_returns_error(client, auth_headers_admin):
    print("\n[TEST CASE] Delete Article - View After Delete Returns Error")
    article_id = _add_temp_article(client, auth_headers_admin, "Article View After Delete Test")
    assert article_id is not None
    client.post("/article/delete", json={"article_id": article_id}, headers=auth_headers_admin)
    view_resp = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_admin)
    assert view_resp.json()["confirmation"] == "backend error"


# ── new tests: verification ───────────────────────────────────────────────────

def test_verification_no_token(client):
    print("\n[TEST CASE] Verification - Tanpa Token")
    response = client.post("/article/verification")
    assert response.status_code == 401


def test_verification_invalid_token(client):
    print("\n[TEST CASE] Verification - Invalid Token")
    response = client.post("/article/verification", headers={"Authorization": "Bearer badtoken"})
    assert response.status_code == 401
