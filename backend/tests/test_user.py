VALID_USER_ID = "507f1f77bcf86cd799439013"
ADMIN_USER_ID = "507f1f77bcf86cd799439012"


# =========================
# GET ALL USERS
# =========================

def test_get_all_users_success(client):
    print("\n[TEST CASE] Get All Users - Success")

    print("[INPUT]")
    print("No payload")

    res = client.post("/user/get_all")

    print("[OUTPUT]")
    print(res.json())

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "successful"
    assert len(data["users"]) >= 1

    print("[RESULT]")
    print("Berhasil mengambil semua user")


# =========================
# GET USER DETAILS
# =========================

def test_get_user_details_self(client):
    print("\n[TEST CASE] Get User Details - Self")

    payload = {}

    print("[INPUT]")
    print(payload)

    res = client.post("/user/get_details", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Berhasil mengambil detail user sendiri")


def test_get_user_details_other_user_as_admin(client):
    print("\n[TEST CASE] Get User Details - Admin Akses User Lain")

    payload = {
        "user_email": "user@mail.com"
    }

    print("[INPUT]")
    print(payload)

    res = client.post("/user/get_details", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"

    print("[RESULT]")
    print("Admin berhasil mengambil detail user lain")


def test_get_user_details_not_found(client):
    print("\n[TEST CASE] Get User Details - User Tidak Ditemukan")

    payload = {
        "user_email": "notfound@mail.com"
    }

    print("[INPUT]")
    print(payload)

    res = client.post("/user/get_details", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "user not found"

    print("[RESULT]")
    print("User tidak ditemukan")


# =========================
# MAKE ADMIN
# =========================

def test_make_admin_success(client):
    print("\n[TEST CASE] Make Admin - Success")

    payload = {
        "user_id": VALID_USER_ID
    }

    print("[INPUT]")
    print(payload)

    res = client.post("/user/make_admin", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful: role updated to admin"

    print("[RESULT]")
    print("User berhasil dijadikan admin")


def test_make_admin_already_admin(client):
    print("\n[TEST CASE] Make Admin - Already Admin")

    payload = {
        "user_id": ADMIN_USER_ID
    }

    print("[INPUT]")
    print(payload)

    res = client.post("/user/make_admin", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "already admin"

    print("[RESULT]")
    print("User sudah admin sebelumnya")


def test_make_admin_user_not_found(client):
    print("\n[TEST CASE] Make Admin - User Tidak Ditemukan")

    payload = {
        "user_id": "507f1f77bcf86cd799439099"
    }

    print("[INPUT]")
    print(payload)

    res = client.post("/user/make_admin", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "user not found"

    print("[RESULT]")
    print("User tidak ditemukan")


# =========================
# DELETE USER
# =========================

def test_delete_user_success(client):
    print("\n[TEST CASE] Delete User - Success")

    payload = {
        "user_id": VALID_USER_ID
    }

    print("[INPUT]")
    print(payload)

    res = client.post("/user/delete", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful: user deleted"

    print("[RESULT]")
    print("User berhasil dihapus")


def test_delete_user_admin_forbidden(client):
    print("\n[TEST CASE] Delete User - Admin Forbidden")

    payload = {
        "user_id": ADMIN_USER_ID
    }

    print("[INPUT]")
    print(payload)

    res = client.post("/user/delete", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "cannot delete admin"

    print("[RESULT]")
    print("Sistem menolak menghapus admin")


def test_delete_user_not_found(client):
    print("\n[TEST CASE] Delete User - User Tidak Ditemukan")

    payload = {
        "user_id": "507f1f77bcf86cd799439099"
    }

    print("[INPUT]")
    print(payload)

    res = client.post("/user/delete", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.json()["confirmation"] == "user not found"

    print("[RESULT]")
    print("User tidak ditemukan saat delete")