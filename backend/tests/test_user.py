VALID_USER_ID = "507f1f77bcf86cd799439013"
ADMIN_USER_ID = "507f1f77bcf86cd799439012"


# =========================
# GET ALL USERS
# =========================

def test_get_all_users_success(client):
    res = client.post("/user/get_all")

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "successful"
    assert len(data["users"]) >= 1


# =========================
# GET USER DETAILS
# =========================

def test_get_user_details_self(client):
    res = client.post("/user/get_details", json={})

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"


def test_get_user_details_other_user_as_admin(client):
    res = client.post("/user/get_details", json={
        "user_email": "user@mail.com"
    })

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"


def test_get_user_details_not_found(client):
    res = client.post("/user/get_details", json={
        "user_email": "notfound@mail.com"
    })

    assert res.json()["confirmation"] == "user not found"


# =========================
# MAKE ADMIN
# =========================

def test_make_admin_success(client):
    res = client.post("/user/make_admin", json={
        "user_id": VALID_USER_ID
    })

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful: role updated to admin"


def test_make_admin_already_admin(client):
    res = client.post("/user/make_admin", json={
        "user_id": ADMIN_USER_ID
    })

    assert res.json()["confirmation"] == "already admin"


def test_make_admin_user_not_found(client):
    res = client.post("/user/make_admin", json={
        "user_id": "507f1f77bcf86cd799439099"
    })

    assert res.json()["confirmation"] == "user not found"


# =========================
# DELETE USER
# =========================

def test_delete_user_success(client):
    res = client.post("/user/delete", json={
        "user_id": VALID_USER_ID
    })

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful: user deleted"


def test_delete_user_admin_forbidden(client):
    res = client.post("/user/delete", json={
        "user_id": ADMIN_USER_ID
    })

    assert res.json()["confirmation"] == "cannot delete admin"


def test_delete_user_not_found(client):
    res = client.post("/user/delete", json={
        "user_id": "507f1f77bcf86cd799439099"
    })

    assert res.json()["confirmation"] == "user not found"