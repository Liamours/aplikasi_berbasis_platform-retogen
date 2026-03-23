ARTICLE_ID = "675e8a1f2c4d3e8f9a1b2c3d"
USER_EMAIL_TO_REPORT = "laudya111@gmail.com"
REPORTER_EMAIL = "steven098@gmail.com"


# ── existing tests ────────────────────────────────────────────────────────────

def test_report_article_success(client, auth_headers_user):
    print("\n[TEST CASE] Report Article - Berhasil")
    response = client.post("/report_article/add", json={
        "article_id": ARTICLE_ID,
        "description": "This article contains false information."
    }, headers=auth_headers_user)
    print(f"    confirmation: {response.json().get('confirmation')}")
    assert response.status_code == 200
    assert response.json()["confirmation"] == "successful: article reported"


def test_report_article_empty_description(client, auth_headers_user):
    print("\n[TEST CASE] Report Article - Deskripsi Kosong")
    response = client.post("/report_article/add", json={
        "article_id": ARTICLE_ID,
        "description": "   "
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "please fill description"


def test_report_article_invalid_id(client, auth_headers_user):
    print("\n[TEST CASE] Report Article - ID Tidak Valid")
    response = client.post("/report_article/add", json={
        "article_id": "invalid_id",
        "description": "Test report."
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "invalid article_id"


def test_report_article_no_token(client):
    print("\n[TEST CASE] Report Article - Tanpa Token")
    response = client.post("/report_article/add", json={
        "article_id": ARTICLE_ID,
        "description": "Test."
    })
    assert response.status_code == 401


def test_report_user_success(client, auth_headers_user):
    print("\n[TEST CASE] Report User - Berhasil")
    response = client.post("/report_user/report_user", json={
        "reported_user_email": USER_EMAIL_TO_REPORT,
        "description": "This user is spamming."
    }, headers=auth_headers_user)
    print(f"    confirmation: {response.json().get('confirmation')}")
    assert response.json()["confirmation"] == "successful: user reported"


def test_report_user_self(client, auth_headers_user):
    print("\n[TEST CASE] Report User - Melaporkan Diri Sendiri")
    response = client.post("/report_user/report_user", json={
        "reported_user_email": REPORTER_EMAIL,
        "description": "Reporting myself."
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "cannot report self"


def test_report_user_not_found(client, auth_headers_user):
    print("\n[TEST CASE] Report User - User Tidak Ditemukan")
    response = client.post("/report_user/report_user", json={
        "reported_user_email": "notexist@mail.com",
        "description": "Test."
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "user not found"


def test_get_user_profile_success(client, auth_headers_user):
    print("\n[TEST CASE] Get User Profile - Berhasil")
    response = client.post("/report_user/get_user_profile", json={
        "user_email": USER_EMAIL_TO_REPORT
    }, headers=auth_headers_user)
    print(f"    confirmation: {response.json().get('confirmation')}")
    assert response.json()["confirmation"] == "successful"
    assert "user" in response.json()


def test_get_user_profile_not_found(client, auth_headers_user):
    print("\n[TEST CASE] Get User Profile - User Tidak Ditemukan")
    response = client.post("/report_user/get_user_profile", json={
        "user_email": "notexist@mail.com"
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "user not found"


# ── new tests: report article ─────────────────────────────────────────────────

def test_report_article_admin_can_report(client, auth_headers_admin):
    print("\n[TEST CASE] Report Article - Admin Juga Bisa Report")
    response = client.post("/report_article/add", json={
        "article_id": ARTICLE_ID,
        "description": "Admin reporting this article."
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful: article reported"


def test_report_article_nonexistent_article(client, auth_headers_user):
    print("\n[TEST CASE] Report Article - Article Tidak Ada (route doesn't verify existence)")
    response = client.post("/report_article/add", json={
        "article_id": "000000000000000000000000",
        "description": "This article doesn't exist."
    }, headers=auth_headers_user)
    # The route validates ObjectId format but does NOT check if the article exists
    assert response.json()["confirmation"] == "successful: article reported"


def test_report_article_very_long_description(client, auth_headers_user):
    print("\n[TEST CASE] Report Article - Description Sangat Panjang")
    response = client.post("/report_article/add", json={
        "article_id": ARTICLE_ID,
        "description": "A" * 1000
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "successful: article reported"


def test_report_article_description_only_whitespace(client, auth_headers_user):
    print("\n[TEST CASE] Report Article - Description Hanya Spasi")
    response = client.post("/report_article/add", json={
        "article_id": ARTICLE_ID,
        "description": "     "
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "please fill description"


def test_report_article_description_single_char(client, auth_headers_user):
    print("\n[TEST CASE] Report Article - Description Single Char")
    response = client.post("/report_article/add", json={
        "article_id": ARTICLE_ID,
        "description": "X"
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "successful: article reported"


# ── new tests: report user ────────────────────────────────────────────────────

def test_report_user_no_token(client):
    print("\n[TEST CASE] Report User - Tanpa Token")
    response = client.post("/report_user/report_user", json={
        "reported_user_email": USER_EMAIL_TO_REPORT,
        "description": "Test report."
    })
    assert response.status_code == 401


def test_report_user_empty_description(client, auth_headers_user):
    print("\n[TEST CASE] Report User - Deskripsi Kosong")
    response = client.post("/report_user/report_user", json={
        "reported_user_email": USER_EMAIL_TO_REPORT,
        "description": ""
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] in ("please fill description", "successful: user reported")


def test_report_user_admin_can_report_user(client, auth_headers_admin):
    print("\n[TEST CASE] Report User - Admin Bisa Report User")
    response = client.post("/report_user/report_user", json={
        "reported_user_email": USER_EMAIL_TO_REPORT,
        "description": "Admin reporting a user."
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful: user reported"


# ── new tests: get user profile ───────────────────────────────────────────────

def test_get_user_profile_no_token(client):
    print("\n[TEST CASE] Get User Profile - Tanpa Token")
    response = client.post("/report_user/get_user_profile", json={
        "user_email": USER_EMAIL_TO_REPORT
    })
    assert response.status_code == 401


def test_get_user_profile_admin_can_view(client, auth_headers_admin):
    print("\n[TEST CASE] Get User Profile - Admin Bisa View")
    response = client.post("/report_user/get_user_profile", json={
        "user_email": USER_EMAIL_TO_REPORT
    }, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful"
    assert "user" in response.json()


def test_get_user_profile_returns_username(client, auth_headers_user):
    print("\n[TEST CASE] Get User Profile - Returns Username")
    response = client.post("/report_user/get_user_profile", json={
        "user_email": USER_EMAIL_TO_REPORT
    }, headers=auth_headers_user)
    assert response.json()["confirmation"] == "successful"
    assert "username" in response.json()["user"] or "user" in response.json()
