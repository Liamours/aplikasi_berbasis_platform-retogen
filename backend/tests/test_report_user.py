from bson import ObjectId

VALID_EMAIL = "user@mail.com"

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
    print("\n[TEST CASE] Get User Profile - Success")

    seed_user(client)

    payload = {
        "user_email": VALID_EMAIL
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/report_user/get_user_profile", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"
    assert res.json()["user"]["user_email"] == VALID_EMAIL

    print("[RESULT]")
    print("Profil user berhasil diambil")


def test_get_user_profile_not_found(client):
    print("\n[TEST CASE] Get User Profile - Not Found")

    payload = {
        "user_email": "notfound@mail.com"
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/report_user/get_user_profile", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "user not found"

    print("[RESULT]")
    print("User tidak ditemukan")

def test_report_user_success(client):
    print("\n[TEST CASE] Report User - Success")

    seed_user(client)

    payload = {
        "reported_user_email": VALID_EMAIL,
        "description": "spam"
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/report_user/report_user", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful: user reported"

    print("[RESULT]")
    print("User berhasil dilaporkan")


def test_report_user_self(client):
    print("\n[TEST CASE] Report User - Report Diri Sendiri")

    payload = {
        "reported_user_email": "admin@mail.com",
        "description": "spam"
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/report_user/report_user", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "cannot report self"

    print("[RESULT]")
    print("Sistem menolak report diri sendiri")


def test_report_user_not_found(client):
    print("\n[TEST CASE] Report User - User Tidak Ditemukan")

    payload = {
        "reported_user_email": "notfound@mail.com",
        "description": "spam"
    }

    print("[INPUT]")
    for k, v in payload.items():
        print(f"{k}: {v}")

    res = client.post("/report_user/report_user", json=payload)

    print("[OUTPUT]")
    print(res.json())

    assert res.status_code == 200
    assert res.json()["confirmation"] == "user not found"

    print("[RESULT]")
    print("Sistem menolak karena user tidak ditemukan")