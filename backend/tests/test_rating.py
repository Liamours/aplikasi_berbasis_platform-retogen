ARTICLE_ID_UNRATED = "675e8a1f2c4d3e8f9a1b2c3d"
ARTICLE_ID_ALREADY_RATED = "675e8a1f2c4d3e8f9a1b2c40"


def test_add_rating_success(client, auth_headers_admin):
    print("\n[TEST CASE] Add Rating - Admin Berhasil")
    response = client.post("/rating/add", json={
        "article_id": ARTICLE_ID_UNRATED,
        "rating_value": 4
    }, headers=auth_headers_admin)
    print(f"    confirmation: {response.json().get('confirmation')}")
    assert response.status_code == 200
    assert response.json()["confirmation"] in ("successful", "already rated")


def test_add_rating_out_of_range(client, auth_headers_user):
    print("\n[TEST CASE] Add Rating - Nilai Di Luar Range")
    response = client.post("/rating/add", json={
        "article_id": ARTICLE_ID_UNRATED,
        "rating_value": 6
    }, headers=auth_headers_user)
    assert response.status_code == 422


def test_add_rating_zero(client, auth_headers_user):
    print("\n[TEST CASE] Add Rating - Nilai 0")
    response = client.post("/rating/add", json={
        "article_id": ARTICLE_ID_UNRATED,
        "rating_value": 0
    }, headers=auth_headers_user)
    assert response.status_code == 422


def test_add_rating_already_rated(client, auth_headers_user):
    print("\n[TEST CASE] Add Rating - Sudah Pernah Rating")
    # rate first, then try again
    client.post("/rating/add", json={
        "article_id": ARTICLE_ID_ALREADY_RATED,
        "rating_value": 3
    }, headers=auth_headers_user)
    response = client.post("/rating/add", json={
        "article_id": ARTICLE_ID_ALREADY_RATED,
        "rating_value": 3
    }, headers=auth_headers_user)
    print(f"    confirmation: {response.json().get('confirmation')}")
    assert response.json()["confirmation"] == "already rated"


def test_add_rating_no_token(client):
    print("\n[TEST CASE] Add Rating - Tanpa Token")
    response = client.post("/rating/add", json={
        "article_id": ARTICLE_ID_UNRATED,
        "rating_value": 3
    })
    assert response.status_code == 401


def test_add_rating_invalid_article(client, auth_headers_user):
    print("\n[TEST CASE] Add Rating - Article Tidak Ada")
    response = client.post("/rating/add", json={
        "article_id": "000000000000000000000000",
        "rating_value": 3
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"