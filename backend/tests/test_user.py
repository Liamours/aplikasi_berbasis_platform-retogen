USER_ID_REGULAR = "69b9009fe445e0618ae70c88"
USER_EMAIL_REGULAR = "steven098@gmail.com"


def test_get_all_users_admin(client, auth_headers_admin):
    print("\n[TEST CASE] Get All Users - Admin Berhasil")
    response = client.post("/user/get_all", headers=auth_headers_admin)
    print(f"    user count: {len(response.json().get('users', []))}")
    assert response.status_code == 200
    assert response.json()["confirmation"] == "successful"
    assert isinstance(response.json()["users"], list)


def test_get_all_users_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Get All Users - User Biasa Ditolak")
    response = client.post("/user/get_all", headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_get_all_users_no_token(client):
    print("\n[TEST CASE] Get All Users - Tanpa Token")
    response = client.post("/user/get_all")
    assert response.status_code == 401


def test_get_user_details_own_profile(client, auth_headers_user):
    print("\n[TEST CASE] Get User Details - Profil Sendiri")
    response = client.post("/user/get_details", json={}, headers=auth_headers_user)
    print(f"    confirmation: {response.json().get('confirmation')}")
    assert response.json()["confirmation"] == "successful"
    assert response.json()["user"]["email"] == USER_EMAIL_REGULAR


def test_get_user_details_other_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Get User Details - Akses User Lain Ditolak")
    response = client.post("/user/get_details", json={
        "user_email": "laudya111@gmail.com"
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "backend error"


def test_get_user_details_admin_can_view_any(client, auth_headers_admin):
    print("\n[TEST CASE] Get User Details - Admin Bisa Lihat User Lain")
    response = client.post("/user/get_details", json={
        "user_email": USER_EMAIL_REGULAR
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful"
    assert "reports" in response.json()["user"]


def test_get_user_details_not_found(client, auth_headers_admin):
    print("\n[TEST CASE] Get User Details - User Tidak Ditemukan")
    response = client.post("/user/get_details", json={
        "user_email": "notexist@mail.com"
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "user not found"


def test_make_admin_success(client, auth_headers_admin):
    print("\n[TEST CASE] Make Admin - Berhasil")
    response = client.post("/user/make_admin", json={
        "user_id": USER_ID_REGULAR
    }, headers=auth_headers_admin)
    print(f"    confirmation: {response.json().get('confirmation')}")
    assert response.json()["confirmation"] in ("successful: role updated to admin", "already admin")


def test_make_admin_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Make Admin - User Biasa Ditolak")
    response = client.post("/user/make_admin", json={
        "user_id": USER_ID_REGULAR
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_make_admin_not_found(client, auth_headers_admin):
    print("\n[TEST CASE] Make Admin - User Tidak Ditemukan")
    response = client.post("/user/make_admin", json={
        "user_id": "000000000000000000000000"
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "user not found"
