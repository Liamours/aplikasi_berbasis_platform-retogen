# tests/conftest.py
import sys
import os
from bson import ObjectId

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from main import app

# =========================
# FAKE DB
# =========================

class FakeUserCollection:
    def __init__(self):
        self.users = []

    async def find_one(self, query):
        for user in self.users:
            if user.get("email") == query.get("email"):
                return user
        return None

    async def insert_one(self, data):
        self.users.append(data)
        return {"inserted_id": "fake_user_id"}


class FakeArticleCollection:
    def __init__(self):
        self.articles = []

    async def insert_one(self, data):
        data["_id"] = ObjectId("507f1f77bcf86cd799439011")
        data["is_deleted"] = False  # penting juga
        self.articles.append(data)
        return type("obj", (), {"inserted_id": data["_id"]})

    async def find_one(self, query):
        for article in self.articles:
            if article.get("_id") == query.get("_id") and article.get("is_deleted") == query.get("is_deleted"):
                return article
        return None
    
    async def update_one(self, query, update):
        return type("obj", (), {"modified_count": 1})

    def find(self, *args, **kwargs):
        class Cursor:
            async def to_list(self, length=None):
                return []
        return Cursor()


class FakeReportArticleCollection:
    def find(self, *args, **kwargs):
        class Cursor:
            async def to_list(self, length=None):
                return []
        return Cursor()


class FakeDB:
    def __init__(self):
        self.user = FakeUserCollection()
        self.article = FakeArticleCollection()
        self.report_article = FakeReportArticleCollection()


# =========================
# FIXTURE
# =========================

@pytest.fixture
def client():
    fake_db = FakeDB()

    # seed admin user
    fake_db.user.users.append({
        "_id": "fake_admin_id",
        "email": "admin@mail.com",
        "username": "admin",
        "role": "admin"
    })

    # =========================
    # OVERRIDE DB (SEMUA TEMPAT)
    # =========================
    import services.auth_service as auth_service
    import services.article_service as article_service
    import routes.article as article_route

    auth_service.db = fake_db
    article_service.db = fake_db
    article_route.db = fake_db   # 🔥 INI YANG KEMARIN KURANG

    # =========================
    # OVERRIDE AUTH
    # =========================
    from core.dependencies import get_current_user

    async def override_get_current_user():
        return {
            "email": "admin@mail.com",
            "role": "admin"
        }

    app.dependency_overrides[get_current_user] = override_get_current_user

    return TestClient(app)