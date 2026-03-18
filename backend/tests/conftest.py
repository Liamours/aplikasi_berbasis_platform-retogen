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
            match = True
            for k, v in query.items():
                if user.get(k) != v:
                    match = False
                    break
            if match:
                return user
        return None

    async def insert_one(self, data):
        data["_id"] = ObjectId()
        self.users.append(data)
        return type("obj", (), {"inserted_id": data["_id"]})

    async def update_one(self, query, update):
        for user in self.users:
            if user.get("_id") == query.get("_id"):
                # handle $inc
                if "$inc" in update:
                    for k, v in update["$inc"].items():
                        user[k] = user.get(k, 0) + v

                # handle $set
                if "$set" in update:
                    user.update(update["$set"])

                return type("obj", (), {
                    "modified_count": 1,
                    "matched_count": 1
                })

        return type("obj", (), {
            "modified_count": 0,
            "matched_count": 0
        })
        
    def find(self, query):
        class Cursor:
            def __init__(self, data):
                self.data = data

            async def to_list(self, length=None):
                return self.data

        return Cursor(self.users)
    
    async def delete_one(self, query):
        for i, user in enumerate(self.users):
            if user.get("_id") == query.get("_id"):
                self.users.pop(i)
                return type("obj", (), {"deleted_count": 1})

        return type("obj", (), {"deleted_count": 0})


class FakeArticleCollection:
    def __init__(self):
        self.articles = []

    async def insert_one(self, data):
        data["_id"] = ObjectId("507f1f77bcf86cd799439011")
        data["is_deleted"] = False
        self.articles.append(data)
        return type("obj", (), {"inserted_id": data["_id"]})

    async def find_one(self, query):
        for article in self.articles:
            match = True
            for k, v in query.items():
                if article.get(k) != v:
                    match = False
                    break
            if match:
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

# 🔥 FIX: report_user collection (WAJIB ADA)
class FakeReportUserCollection:
    def __init__(self):
        self.reports = []

    async def insert_one(self, data):
        data["_id"] = ObjectId()
        self.reports.append(data)
        return type("obj", (), {"inserted_id": data["_id"]})

    async def delete_many(self, query):
        self.reports = [
            r for r in self.reports
            if r.get("reported_user_id") != query.get("reported_user_id")
        ]
        
    def find(self, query):
            class Cursor:
                def __init__(self, data):
                    self.data = data

                async def to_list(self, length=None):
                    return self.data

            filtered = [
                r for r in self.reports
                if r.get("reported_user_id") == query.get("reported_user_id")
            ]

            return Cursor(filtered)

class FakeCommentCollection:
    def __init__(self):
        self.comments = []

    async def insert_one(self, data):
        data["_id"] = ObjectId()
        self.comments.append(data)
        return type("obj", (), {"inserted_id": data["_id"]})

    def find(self, query):
        class Cursor:
            def __init__(self, data):
                self.data = data

            async def to_list(self, length=None):
                return self.data

        filtered = [
            c for c in self.comments
            if c.get("article_id") == query.get("article_id")
        ]

        return Cursor(filtered)

    async def find_one(self, query):
        for c in self.comments:
            if str(c.get("_id")) == str(query.get("_id")):
                return c
        return None

    async def update_one(self, query, update):
        return type("obj", (), {"acknowledged": True})

    async def delete_many(self, query):
        self.comments = []


class FakeRatingCollection:
    def __init__(self):
        self.ratings = []

    async def insert_one(self, data):
        data["_id"] = ObjectId()
        self.ratings.append(data)
        return type("obj", (), {"inserted_id": data["_id"]})

    async def find_one(self, query):
        for r in self.ratings:
            match = True
            for k, v in query.items():
                if r.get(k) != v:
                    match = False
                    break
            if match:
                return r
        return None

    def find(self, query):
        class Cursor:
            def __init__(self, data):
                self.data = data

            async def to_list(self, length=None):
                return self.data

        filtered = [
            r for r in self.ratings
            if r.get("article_id") == query.get("article_id")
        ]

        return Cursor(filtered)

    async def update_one(self, query, update):
        for r in self.ratings:
            if r.get("_id") == query.get("_id"):
                r.update(update.get("$set", {}))
                return type("obj", (), {"modified_count": 1})
        return type("obj", (), {"modified_count": 0})

    async def delete_many(self, query):
        self.ratings = [
            r for r in self.ratings
            if r.get("owner_id") != query.get("owner_id")
        ]

class FakeDB:
    def __init__(self):
        self.user = FakeUserCollection()
        self.article = FakeArticleCollection()
        self.report_article = FakeReportArticleCollection()
        self.report_user = FakeReportUserCollection()  # 🔥 FIX
        self.comment = FakeCommentCollection()
        self.rating = FakeRatingCollection()

    # 🔥 FIX: biar db.command("ping") tidak error
    async def command(self, *args, **kwargs):
        return {"ok": 1}


# =========================
# FIXTURE
# =========================

@pytest.fixture
def client():
    fake_db = FakeDB()

    fake_db.user.users.append({
        "_id": ObjectId("507f1f77bcf86cd799439012"),
        "email": "admin@mail.com",
        "username": "admin",
        "role": "admin"
    })

    # seed user
    fake_db.user.users.append({
        "_id": ObjectId("507f1f77bcf86cd799439013"),
        "email": "user@mail.com",
        "username": "user",
        "role": "user"
    })

    # =========================
    # OVERRIDE DB (SEMUA TEMPAT)
    # =========================
    import services.auth_service as auth_service
    import services.article_service as article_service
    import routes.article as article_route
    import services.comment_service as comment_service
    import routes.comment as comment_route
    import services.rating_service as rating_service
    import routes.rating as rating_route
    import services.report_user_service as report_user_service
    import routes.report_user as report_user_route
    import db.connection as db_connection
    import services.user_service as user_service
    import routes.user as user_route

    db_connection.db = fake_db

    auth_service.db = fake_db
    article_service.db = fake_db
    comment_service.db = fake_db
    rating_service.db = fake_db
    report_user_service.db = fake_db
    user_service.db = fake_db

    article_route.db = fake_db
    comment_route.db = fake_db
    rating_route.db = fake_db
    report_user_route.db = fake_db
    user_route.db = fake_db

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