import base64

SMALL_IMAGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="
INVALID_IMAGE_B64 = "dGhpcyBpcyBub3QgYW4gaW1hZ2U="


# ── helpers ──────────────────────────────────────────────────────────────────

def _add_temp_article(client, headers, title="Temp Delete Test Article"):
    payload = {
        "article_title": title,
        "article_preview": "Temp preview for test",
        "article_content": "Temp content for test",
        "article_tags": ["gaming"],
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


# ── main page ─────────────────────────────────────────────────────────────────

def test_main_page_default(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - Default (Newest)")
    response = client.post("/article/main_page", json={}, headers=auth_headers_user)
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
        assert "productivity" in a["article_tags"]


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
    print("\n[TEST CASE] Main Page - Image is valid base64")
    client.post("/article/add", json={
        "article_title": "Base64 Image Test Article",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tags": ["gaming"],
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
        assert "article_tags" in a


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


def test_main_page_article_tags_always_list(client, auth_headers_user):
    print("\n[TEST CASE] Main Page - article_tags Selalu List Di Setiap Artikel")
    response = client.post("/article/main_page", json={}, headers=auth_headers_user)
    for a in response.json()["list_article"]:
        assert isinstance(a["article_tags"], list)


# ── view article ──────────────────────────────────────────────────────────────

def test_view_article_success(client, auth_headers_user, article_id):
    print("\n[TEST CASE] View Article - Berhasil")
    response = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    assert response.status_code == 200
    assert response.json()["confirmation"] == "successful"
    assert "article_title" in response.json()


def test_view_article_invalid_id(client, auth_headers_user):
    print("\n[TEST CASE] View Article - ID Tidak Valid")
    response = client.post("/article/view", json={"article_id": "000000000000000000000000"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_view_article_no_token(client, article_id):
    print("\n[TEST CASE] View Article - Tanpa Token")
    response = client.post("/article/view", json={"article_id": article_id})
    assert response.status_code == 401


def test_view_article_has_comments_field(client, auth_headers_user, article_id):
    print("\n[TEST CASE] View Article - Has Comments Field")
    response = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    assert "comments" in response.json()
    assert isinstance(response.json()["comments"], list)


def test_view_article_has_ratings_field(client, auth_headers_user, article_id):
    print("\n[TEST CASE] View Article - Has Ratings Field")
    response = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    assert "ratings" in response.json()
    assert isinstance(response.json()["ratings"], list)


def test_view_article_has_reports_field_admin(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] View Article - Admin Sees Reports Field")
    response = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_admin)
    assert "reports" in response.json()
    assert isinstance(response.json()["reports"], list)


def test_view_article_userclass_is_user(client, auth_headers_user, article_id):
    print("\n[TEST CASE] View Article - Userclass Is 'user'")
    response = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    assert response.json()["userclass"] == "user"


def test_view_article_userclass_is_admin(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] View Article - Userclass Is 'admin'")
    response = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_admin)
    assert response.json()["userclass"] == "admin"


def test_view_article_malformed_id(client, auth_headers_user):
    print("\n[TEST CASE] View Article - Malformed ID (non-hex)")
    response = client.post("/article/view", json={"article_id": "not-a-valid-objectid"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_view_article_has_correct_fields(client, auth_headers_user, article_id):
    print("\n[TEST CASE] View Article - Has All Correct Fields")
    response = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    data = response.json()
    for field in ("confirmation", "userclass", "user_email", "username", "article_title", "article_content", "article_tags", "comments", "ratings"):
        assert field in data, f"Missing field: {field}"


def test_view_article_tags_is_list(client, auth_headers_user, article_id):
    print("\n[TEST CASE] View Article - article_tags Is List")
    response = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    assert isinstance(response.json()["article_tags"], list)


def test_view_article_tags_not_empty(client, auth_headers_user, article_id):
    print("\n[TEST CASE] View Article - article_tags Tidak Kosong")
    response = client.post("/article/view", json={"article_id": article_id}, headers=auth_headers_user)
    assert len(response.json()["article_tags"]) > 0


# ── verification ──────────────────────────────────────────────────────────────

def test_verification_admin(client, auth_headers_admin):
    print("\n[TEST CASE] Verification - Admin")
    response = client.post("/article/verification", headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful"


def test_verification_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Verification - User Biasa Ditolak")
    response = client.post("/article/verification", headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_verification_no_token(client):
    print("\n[TEST CASE] Verification - Tanpa Token")
    response = client.post("/article/verification")
    assert response.status_code == 401


def test_verification_invalid_token(client):
    print("\n[TEST CASE] Verification - Invalid Token")
    response = client.post("/article/verification", headers={"Authorization": "Bearer badtoken"})
    assert response.status_code == 401


# ── add article ───────────────────────────────────────────────────────────────

def test_add_article_success(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Admin Berhasil")
    payload = {
        "article_title": "Test Article Title",
        "article_preview": "Test preview text here",
        "article_content": "Test content body here for the article.",
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert response.status_code == 200
    assert response.json()["confirmation"] == "success: article added"


def test_add_article_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Add Article - User Biasa Ditolak")
    payload = {
        "article_title": "Test Article Title",
        "article_preview": "Test preview text here",
        "article_content": "Test content body here.",
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_add_article_title_too_long(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Judul Terlalu Panjang")
    payload = {
        "article_title": "A" * 257,
        "article_preview": "Test preview",
        "article_content": "Test content",
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert "Title must be" in response.json()["confirmation"]


def test_add_article_preview_too_long(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Preview Terlalu Panjang")
    payload = {
        "article_title": "Valid Title",
        "article_preview": "P" * 129,
        "article_content": "Valid content",
        "article_tags": ["gaming"],
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
        "article_tags": ["gaming"],
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
        "article_tags": ["gaming"],
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
        "article_tags": ["gaming"],
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
        "article_tags": ["gaming"],
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
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "success: article added"


def test_add_article_image_stored_as_binary_and_retrievable(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Image Stored as Binary and Retrievable")
    payload = {
        "article_title": "Binary Image Storage Test",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tags": ["gaming"],
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


def test_add_article_no_tags_rejected(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Tanpa Tags Ditolak")
    payload = {
        "article_title": "No Tags Article",
        "article_preview": "Preview text",
        "article_content": "Content body",
        "article_tags": [],
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert "tag" in response.json()["confirmation"].lower()


def test_add_article_tags_stored_as_lowercase(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Tags Disimpan Lowercase")
    payload = {
        "article_title": "Tag Lowercase Storage Test",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tags": ["GAMING", "Tech"],
        "article_image": SMALL_IMAGE_B64,
    }
    client.post("/article/add", json=payload, headers=auth_headers_admin)
    resp = client.post("/article/main_page", json={"sort": "search_title", "search": "Tag Lowercase Storage Test"}, headers=auth_headers_admin)
    articles = resp.json().get("list_article", [])
    found = next((a for a in articles if a["article_title"] == "Tag Lowercase Storage Test"), None)
    assert found is not None
    assert "gaming" in found["article_tags"]
    assert "tech" in found["article_tags"]


def test_add_article_multiple_tags_stored(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Multiple Tags Tersimpan Semua")
    payload = {
        "article_title": "Multi Tag Article Test",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tags": ["alpha", "beta", "gamma"],
        "article_image": SMALL_IMAGE_B64,
    }
    client.post("/article/add", json=payload, headers=auth_headers_admin)
    resp = client.post("/article/main_page", json={"sort": "search_title", "search": "Multi Tag Article Test"}, headers=auth_headers_admin)
    articles = resp.json().get("list_article", [])
    found = next((a for a in articles if a["article_title"] == "Multi Tag Article Test"), None)
    assert found is not None
    for t in ["alpha", "beta", "gamma"]:
        assert t in found["article_tags"]


def test_add_article_tags_whitespace_trimmed(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Tags Whitespace Ditriming")
    payload = {
        "article_title": "Tag Trim Test Article",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tags": ["  sportz  ", "  techz  "],
        "article_image": SMALL_IMAGE_B64,
    }
    client.post("/article/add", json=payload, headers=auth_headers_admin)
    resp = client.post("/article/main_page", json={"sort": "search_title", "search": "Tag Trim Test Article"}, headers=auth_headers_admin)
    articles = resp.json().get("list_article", [])
    found = next((a for a in articles if a["article_title"] == "Tag Trim Test Article"), None)
    assert found is not None
    assert "sportz" in found["article_tags"]
    assert "techz" in found["article_tags"]


def test_add_article_single_tag(client, auth_headers_admin):
    print("\n[TEST CASE] Add Article - Single Tag Tersimpan")
    payload = {
        "article_title": "Single Tag Article",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tags": ["singletag"],
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/add", json=payload, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "success: article added"


# ── edit/get ──────────────────────────────────────────────────────────────────

def test_edit_get_success_admin(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Edit Get - Admin Berhasil")
    response = client.post("/article/edit/get", json={"article_id": article_id}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful"
    assert "article_title" in response.json()
    assert "article_content" in response.json()


def test_edit_get_user_forbidden(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Get - User Biasa Ditolak")
    response = client.post("/article/edit/get", json={"article_id": article_id}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_edit_get_no_token(client, article_id):
    print("\n[TEST CASE] Edit Get - Tanpa Token")
    response = client.post("/article/edit/get", json={"article_id": article_id})
    assert response.status_code == 401


def test_edit_get_invalid_article_id(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Get - Article ID Tidak Ditemukan")
    response = client.post("/article/edit/get", json={"article_id": "000000000000000000000000"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


def test_edit_get_malformed_article_id(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Get - Article ID Malformed")
    response = client.post("/article/edit/get", json={"article_id": "not-a-valid-id"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


def test_edit_get_tags_is_list(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Edit Get - article_tags Is List")
    response = client.post("/article/edit/get", json={"article_id": article_id}, headers=auth_headers_admin)
    assert isinstance(response.json()["article_tags"], list)


# ── edit/update ───────────────────────────────────────────────────────────────

def test_edit_update_user_forbidden(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Update - User Biasa Ditolak")
    payload = {
        "article_id": article_id,
        "article_title": "Updated Title",
        "article_preview": "Updated preview",
        "article_content": "Updated content",
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_edit_update_no_token(client, article_id):
    print("\n[TEST CASE] Edit Update - Tanpa Token")
    payload = {
        "article_id": article_id,
        "article_title": "Updated Title",
        "article_preview": "Updated preview",
        "article_content": "Updated content",
        "article_tags": ["gaming"],
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
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "backend error"


def test_edit_update_title_empty(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Edit Update - Judul Kosong")
    payload = {
        "article_id": article_id,
        "article_title": "",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert "Title must be" in response.json()["confirmation"]


def test_edit_update_preview_too_long(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Edit Update - Preview Terlalu Panjang")
    payload = {
        "article_id": article_id,
        "article_title": "Valid Title",
        "article_preview": "P" * 129,
        "article_content": "Content",
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert "Preview must be" in response.json()["confirmation"]


def test_edit_update_content_too_long(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Edit Update - Content Terlalu Panjang")
    payload = {
        "article_id": article_id,
        "article_title": "Valid Title",
        "article_preview": "Valid preview",
        "article_content": "C" * 65537,
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert "Content must be" in response.json()["confirmation"]


def test_edit_update_invalid_image(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Edit Update - Invalid Image Bytes (not PNG/JPEG)")
    payload = {
        "article_id": article_id,
        "article_title": "Valid Title",
        "article_preview": "Valid preview",
        "article_content": "Valid content",
        "article_tags": ["gaming"],
        "article_image": INVALID_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert "invalid image" in response.json()["confirmation"].lower()


def test_edit_update_admin_success(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Edit Update - Admin Berhasil")
    payload = {
        "article_id": article_id,
        "article_title": "Updated Title by Admin",
        "article_preview": "Updated preview",
        "article_content": "Updated content body",
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful: article edited"


def test_edit_update_title_exactly_256(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Edit Update - Title Exactly 256 Chars (Boundary)")
    payload = {
        "article_id": article_id,
        "article_title": "A" * 256,
        "article_preview": "Valid preview",
        "article_content": "Valid content",
        "article_tags": ["gaming"],
        "article_image": SMALL_IMAGE_B64,
    }
    response = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful: article edited"


def test_edit_update_tags_change(client, auth_headers_admin):
    print("\n[TEST CASE] Edit Update - Tags Berubah Setelah Update")
    article_id = _add_temp_article(client, auth_headers_admin, "Tags Change Test Article")
    assert article_id is not None

    new_tags = ["newtag_x", "newtag_y"]
    payload = {
        "article_id": article_id,
        "article_title": "Tags Change Test Article",
        "article_preview": "Temp preview for test",
        "article_content": "Temp content for test",
        "article_tags": new_tags,
        "article_image": SMALL_IMAGE_B64,
    }
    update_resp = client.post("/article/edit/update", json=payload, headers=auth_headers_admin)
    assert update_resp.json()["confirmation"] == "successful: article edited"

    get_resp = client.post("/article/edit/get", json={"article_id": article_id}, headers=auth_headers_admin)
    stored_tags = get_resp.json()["article_tags"]
    for t in new_tags:
        assert t in stored_tags


# ── delete article ────────────────────────────────────────────────────────────

def test_delete_article_user_forbidden(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Delete Article - User Biasa Ditolak")
    response = client.post("/article/delete", json={"article_id": article_id}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_delete_article_no_token(client, article_id):
    print("\n[TEST CASE] Delete Article - Tanpa Token")
    response = client.post("/article/delete", json={"article_id": article_id})
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
    temp_id = _add_temp_article(client, auth_headers_admin, "Article To Be Deleted By Admin")
    assert temp_id is not None, "Could not create temp article for delete test"
    response = client.post("/article/delete", json={"article_id": temp_id}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful: article deleted"


def test_delete_article_then_view_returns_error(client, auth_headers_admin):
    print("\n[TEST CASE] Delete Article - View After Delete Returns Error")
    temp_id = _add_temp_article(client, auth_headers_admin, "Article View After Delete Test")
    assert temp_id is not None
    client.post("/article/delete", json={"article_id": temp_id}, headers=auth_headers_admin)
    view_resp = client.post("/article/view", json={"article_id": temp_id}, headers=auth_headers_admin)
    assert view_resp.json()["confirmation"] == "backend error"


# ── tags feature ──────────────────────────────────────────────────────────────

def test_main_page_filter_by_tag_exact_match(client, auth_headers_admin):
    print("\n[TEST CASE] Main Page - Filter Tag Exact Match")
    unique_tag = f"uniquetag_{base64.b64encode(b'test').decode()[:6].lower()}"
    client.post("/article/add", json={
        "article_title": "Unique Tag Filter Test",
        "article_preview": "Preview",
        "article_content": "Content",
        "article_tags": [unique_tag],
        "article_image": SMALL_IMAGE_B64,
    }, headers=auth_headers_admin)
    resp = client.post("/article/main_page", json={"sort": "by_tag", "tag": unique_tag}, headers=auth_headers_admin)
    articles = resp.json().get("list_article", [])
    for a in articles:
        assert unique_tag in a["article_tags"]
