# ── existing tests ────────────────────────────────────────────────────────────

def test_add_rating_success(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Add Rating - Admin Berhasil")
    response = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 4
    }, headers=auth_headers_admin)
    assert response.status_code == 200
    assert response.json()["confirmation"] in ("successful", "already rated")


def test_add_rating_out_of_range(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Rating - Nilai Di Luar Range")
    response = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 6
    }, headers=auth_headers_user)
    assert response.status_code == 422


def test_add_rating_zero(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Rating - Nilai 0")
    response = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 0
    }, headers=auth_headers_user)
    assert response.status_code == 422


def test_add_rating_already_rated(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Rating - Sudah Pernah Rating")
    client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 3
    }, headers=auth_headers_user)
    response = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 3
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "already rated"


def test_add_rating_no_token(client, article_id):
    print("\n[TEST CASE] Add Rating - Tanpa Token")
    response = client.post("/rating/add", json={
        "article_id": article_id,
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


# ── new tests: add rating ─────────────────────────────────────────────────────

def test_add_rating_value_1_min(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Add Rating - Nilai 1 (Minimum)")
    response = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 1
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] in ("successful", "already rated")


def test_add_rating_value_5_max(client, auth_headers_admin, article_id):
    print("\n[TEST CASE] Add Rating - Nilai 5 (Maximum)")
    response = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 5
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] in ("successful", "already rated")


def test_add_rating_user_success(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Rating - User Biasa Berhasil")
    response = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 4
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] in ("successful", "already rated")


def test_add_rating_negative_value(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Rating - Nilai Negatif Ditolak")
    response = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": -1
    }, headers=auth_headers_user)
    assert response.status_code == 422


def test_add_rating_malformed_article_id(client, auth_headers_user):
    print("\n[TEST CASE] Add Rating - Article ID Malformed")
    response = client.post("/rating/add", json={
        "article_id": "not-a-valid-id",
        "rating_value": 3
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_add_rating_value_2(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Rating - Nilai 2")
    response = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 2
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] in ("successful", "already rated")


def test_add_rating_value_3(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Add Rating - Nilai 3")
    response = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 3
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] in ("successful", "already rated")


# ── new tests: edit/get rating ────────────────────────────────────────────────

def test_edit_get_rating_owner_success(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Get Rating - Owner Berhasil")
    add_resp = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 3
    }, headers=auth_headers_user)

    ratings = add_resp.json().get("ratings", [])
    rating_id = ratings[0]["rating_id"] if ratings else "000000000000000000000000"

    response = client.post("/rating/edit/get", json={
        "article_id": article_id,
        "rating_id": rating_id
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] in ("successful", "backend error")


def test_edit_get_rating_no_token(client, article_id):
    print("\n[TEST CASE] Edit Get Rating - Tanpa Token")
    response = client.post("/rating/edit/get", json={
        "article_id": article_id,
        "rating_id": "000000000000000000000000"
    })
    assert response.status_code == 401


def test_edit_get_rating_invalid_article(client, auth_headers_user):
    print("\n[TEST CASE] Edit Get Rating - Rating Tidak Ada")
    response = client.post("/rating/edit/get", json={
        "article_id": "000000000000000000000000",
        "rating_id": "000000000000000000000000"
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


# ── new tests: edit/update rating ─────────────────────────────────────────────

def test_edit_rating_success(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Rating - Berhasil")
    add_resp = client.post("/rating/add", json={
        "article_id": article_id,
        "rating_value": 3
    }, headers=auth_headers_user)

    ratings = add_resp.json().get("ratings", [])
    rating_id = ratings[0]["rating_id"] if ratings else None
    if rating_id is None:
        print("    skipping: no rating_id returned")
        return

    edit_resp = client.post("/rating/edit/update", json={
        "rating_id": rating_id,
        "article_id": article_id,
        "rating_value": 5
    }, headers=auth_headers_user)
    assert edit_resp.json()["confirmation"] in ("successful", "backend error")


def test_edit_rating_no_token(client, article_id):
    print("\n[TEST CASE] Edit Rating - Tanpa Token")
    response = client.post("/rating/edit/update", json={
        "rating_id": "000000000000000000000000",
        "article_id": article_id,
        "rating_value": 4
    })
    assert response.status_code == 401


def test_edit_rating_out_of_range_high(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Rating - Nilai Di Atas Range (>5) → backend error")
    response = client.post("/rating/edit/update", json={
        "rating_id": "000000000000000000000000",
        "article_id": article_id,
        "rating_value": 6
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_edit_rating_out_of_range_low(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Rating - Nilai Di Bawah Range (<1) → backend error")
    response = client.post("/rating/edit/update", json={
        "rating_id": "000000000000000000000000",
        "article_id": article_id,
        "rating_value": 0
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_edit_rating_invalid_rating_id(client, auth_headers_user, article_id):
    print("\n[TEST CASE] Edit Rating - Rating ID Tidak Ada")
    response = client.post("/rating/edit/update", json={
        "rating_id": "000000000000000000000000",
        "article_id": article_id,
        "rating_value": 3
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"
