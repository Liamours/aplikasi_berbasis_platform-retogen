VALID_EMAIL = "user@mail.com"


from bson import ObjectId

def seed_user(client):
    from services.report_user_service import db

    db.user.users.append({
        "_id": ObjectId("507f1f77bcf86cd799439099"),
        "email": VALID_EMAIL,
        "username": "user",
        "role": "user",
        "report_count": 0
    })
def test_get_user_profile_success(client):
    seed_user(client)

    res = client.post("/report_user/get_user_profile", json={
        "user_email": VALID_EMAIL
    })

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "successful"
    assert data["user"]["user_email"] == VALID_EMAIL


def test_get_user_profile_not_found(client):
    res = client.post("/report_user/get_user_profile", json={
        "user_email": "notfound@mail.com"
    })

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "user not found"


def test_report_user_success(client):
    seed_user(client)

    res = client.post("/report_user/report_user", json={
        "reported_user_email": VALID_EMAIL,
        "description": "spam"
    })

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful: user reported"


def test_report_user_self(client):
    res = client.post("/report_user/report_user", json={
        "reported_user_email": "admin@mail.com",
        "description": "spam"
    })

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "cannot report self"


def test_report_user_not_found(client):
    res = client.post("/report_user/report_user", json={
        "reported_user_email": "notfound@mail.com",
        "description": "spam"
    })

    data = res.json()

    assert res.status_code == 200
    assert data["confirmation"] == "user not found"