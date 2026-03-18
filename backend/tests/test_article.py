ARTICLE_ID = "675e8a1f2c4d3e8f9a1b2c3d"
SMALL_IMAGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="


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
