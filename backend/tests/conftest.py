import pytest
import httpx

BASE_URL = "http://localhost:8000"

ADMIN_EMAIL = "fathanaryamaulana@gmail.com"
ADMIN_PASSWORD = "Tsukiya0"
USER_EMAIL = "steven098@gmail.com"
USER_PASSWORD = "123Asdfg"

ARTICLE_ID = "675e8a1f2c4d3e8f9a1b2c3d"
ARTICLE_ID_ALREADY_RATED = "675e8a1f2c4d3e8f9a1b2c40"
USER_ID_REGULAR = "69b9009fe445e0618ae70c88"

@pytest.fixture(scope="session")
def client():
    return httpx.Client(base_url=BASE_URL)

@pytest.fixture(scope="session")
def admin_token(client):
    r = client.post("/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert r.json()["confirmation"] == "login successful", f"Admin login failed: {r.json()}"
    return r.json()["token"]

@pytest.fixture(scope="session")
def user_token(client):
    r = client.post("/auth/login", json={"email": USER_EMAIL, "password": USER_PASSWORD})
    assert r.json()["confirmation"] == "login successful", f"User login failed: {r.json()}"
    return r.json()["token"]

@pytest.fixture(scope="session")
def auth_headers_admin(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture(scope="session")
def auth_headers_user(user_token):
    return {"Authorization": f"Bearer {user_token}"}
