import os
import uuid
import pytest
import httpx

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000")

ADMIN_EMAIL = os.getenv("TEST_ADMIN_EMAIL", "fathanaryamaulana@gmail.com")
ADMIN_PASSWORD = os.getenv("TEST_ADMIN_PASSWORD", "Tsukiya0")

_SESSION_UUID = uuid.uuid4().hex[:8]
_FRESH_USER_EMAIL = f"freshusr_{_SESSION_UUID}@autotest.com"
_FRESH_USER_PASSWORD = "FreshPass1"

USER_ID_REGULAR = os.getenv("TEST_USER_ID_REGULAR", "69b9009fe445e0618ae70c88")


@pytest.fixture(scope="session")
def client():
    return httpx.Client(base_url=BASE_URL)


@pytest.fixture(scope="session")
def fresh_user_email():
    return _FRESH_USER_EMAIL


@pytest.fixture(scope="session")
def admin_token(client):
    r = client.post("/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert r.json()["confirmation"] == "login successful", f"Admin login failed: {r.json()}"
    return r.json()["token"]


@pytest.fixture(scope="session")
def user_token(client):
    username = f"fu{_SESSION_UUID}"
    client.post("/auth/registration", json={
        "username": username,
        "fullname": "Fresh Test User",
        "email": _FRESH_USER_EMAIL,
        "password": _FRESH_USER_PASSWORD,
    })
    r = client.post("/auth/login", json={"email": _FRESH_USER_EMAIL, "password": _FRESH_USER_PASSWORD})
    assert r.json()["confirmation"] == "login successful", f"Fresh user login failed: {r.json()}"
    return r.json()["token"]


@pytest.fixture(scope="session")
def auth_headers_admin(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(scope="session")
def auth_headers_user(user_token):
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture(scope="session")
def article_id(client, auth_headers_admin):
    """Fetch a real article ID from the live DB — no hardcoded IDs."""
    resp = client.post("/article/main_page", json={}, headers=auth_headers_admin)
    articles = resp.json().get("list_article", [])
    if not articles:
        pytest.fail("No articles found — run reset_database.py before running tests")
    return articles[0]["article_id"]


@pytest.fixture(scope="session")
def seed_comment_id(client, auth_headers_user, article_id):
    """Add a root comment (as regular user) and return its ID for reply/ownership tests."""
    resp = client.post("/comment/add", json={
        "article_id": article_id,
        "comment_content": "Seed comment for reply tests.",
        "parent_comment_id": None,
    }, headers=auth_headers_user)
    comments = resp.json().get("comments", [])
    target = next((c for c in comments if c["comment_content"] == "Seed comment for reply tests."), None)
    if target is None:
        pytest.fail("Could not create seed comment")
    return target["comment_id"]
