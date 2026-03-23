import uuid

USER_ID_REGULAR = "69b9009fe445e0618ae70c88"
USER_EMAIL_REGULAR = "steven098@gmail.com"
ADMIN_EMAIL = "fathanaryamaulana@gmail.com"


# ── helpers ───────────────────────────────────────────────────────────────────

def _register_temp_user(client):
    """Register a throwaway user and return their email."""
    unique = uuid.uuid4().hex[:8]
    email = f"tmpuser{unique}@mail.com"
    payload = {
        "username": f"tmp{unique}",
        "fullname": "Temp User",
        "email": email,
        "password": "TempPass1",
    }
    client.post("/auth/registration", json=payload)
    return email


def _get_user_id_by_email(client, headers, email):
    """Admin: get user ID from get_details endpoint."""
    resp = client.post("/user/get_details", json={"user_email": email}, headers=headers)
    return resp.json().get("user", {}).get("_id") or resp.json().get("user", {}).get("id")


# ── existing tests ────────────────────────────────────────────────────────────

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


# ── new tests: get all users ──────────────────────────────────────────────────

def test_get_all_users_returns_list_with_fields(client, auth_headers_admin):
    print("\n[TEST CASE] Get All Users - Returns List With Fields")
    response = client.post("/user/get_all", headers=auth_headers_admin)
    users = response.json().get("users", [])
    assert len(users) > 0
    first = users[0]
    assert "email" in first or "username" in first


def test_get_all_users_invalid_token(client):
    print("\n[TEST CASE] Get All Users - Invalid Token")
    response = client.post("/user/get_all", headers={"Authorization": "Bearer badtoken"})
    assert response.status_code == 401


# ── new tests: get user details ───────────────────────────────────────────────

def test_get_user_details_no_token(client):
    print("\n[TEST CASE] Get User Details - Tanpa Token")
    response = client.post("/user/get_details", json={})
    assert response.status_code == 401


def test_get_user_details_admin_views_own_profile(client, auth_headers_admin):
    print("\n[TEST CASE] Get User Details - Admin Views Own Profile")
    response = client.post("/user/get_details", json={"user_email": ADMIN_EMAIL}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful"
    assert response.json()["user"]["email"] == ADMIN_EMAIL


def test_get_user_details_returns_correct_email(client, auth_headers_admin):
    print("\n[TEST CASE] Get User Details - Returns Correct Email")
    response = client.post("/user/get_details", json={"user_email": USER_EMAIL_REGULAR}, headers=auth_headers_admin)
    assert response.json()["user"]["email"] == USER_EMAIL_REGULAR


def test_get_user_details_user_views_own_no_email_param(client, auth_headers_user):
    print("\n[TEST CASE] Get User Details - User Views Own (No Email Param)")
    response = client.post("/user/get_details", json={}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "successful"
    assert response.json()["user"]["email"] == USER_EMAIL_REGULAR


# ── new tests: make admin ─────────────────────────────────────────────────────

def test_make_admin_no_token(client):
    print("\n[TEST CASE] Make Admin - Tanpa Token")
    response = client.post("/user/make_admin", json={"user_id": USER_ID_REGULAR})
    assert response.status_code == 401


def test_make_admin_invalid_id_format(client, auth_headers_admin):
    print("\n[TEST CASE] Make Admin - ID Malformed")
    response = client.post("/user/make_admin", json={"user_id": "not-a-valid-id"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] in ("backend error", "user not found")


def test_make_admin_already_admin_stays_admin(client, auth_headers_admin):
    print("\n[TEST CASE] Make Admin - Already Admin Stays Admin")
    client.post("/user/make_admin", json={"user_id": USER_ID_REGULAR}, headers=auth_headers_admin)
    response = client.post("/user/make_admin", json={"user_id": USER_ID_REGULAR}, headers=auth_headers_admin)
    assert response.json()["confirmation"] in ("successful: role updated to admin", "already admin")


# ── new tests: delete user ────────────────────────────────────────────────────

def test_delete_user_no_token(client):
    print("\n[TEST CASE] Delete User - Tanpa Token")
    response = client.post("/user/delete", json={"user_id": USER_ID_REGULAR})
    assert response.status_code == 401


def test_delete_user_user_forbidden(client, auth_headers_user):
    print("\n[TEST CASE] Delete User - User Biasa Ditolak")
    response = client.post("/user/delete", json={"user_id": USER_ID_REGULAR}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "not admin"


def test_delete_user_not_found(client, auth_headers_admin):
    print("\n[TEST CASE] Delete User - User Tidak Ditemukan")
    response = client.post("/user/delete", json={"user_id": "000000000000000000000000"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] in ("backend error", "user not found")


def test_delete_user_invalid_id_format(client, auth_headers_admin):
    print("\n[TEST CASE] Delete User - ID Malformed")
    response = client.post("/user/delete", json={"user_id": "not-a-valid-id"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] in ("backend error", "user not found")


def test_delete_user_lifecycle(client, auth_headers_admin):
    print("\n[TEST CASE] Delete User - Full Lifecycle: Register then Delete")
    email = _register_temp_user(client)

    details_resp = client.post("/user/get_details", json={"user_email": email}, headers=auth_headers_admin)
    assert details_resp.json()["confirmation"] == "successful"
    user_id = details_resp.json()["user"].get("user_id")
    assert user_id is not None, "Could not retrieve new user ID"

    del_resp = client.post("/user/delete", json={"user_id": user_id}, headers=auth_headers_admin)
    assert del_resp.json()["confirmation"] in ("successful: user deleted", "successful")

    after_resp = client.post("/user/get_details", json={"user_email": email}, headers=auth_headers_admin)
    assert after_resp.json()["confirmation"] == "user not found"
