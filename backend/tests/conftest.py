import sys
import os
import pytest
import mongomock

# supaya import backend.xxx jalan
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services import auth_service
from services import article_service
from services import comment_service
from services import rating_service
from services import report_article_service
from services import report_user_service


class AsyncCursorWrapper:
    def __init__(self, cursor):
        self._cursor = cursor

    async def to_list(self, length=None):
        return list(self._cursor)


class AsyncCollectionWrapper:
    def __init__(self, collection):
        self._collection = collection

    async def find_one(self, *args, **kwargs):
        return self._collection.find_one(*args, **kwargs)

    async def insert_many(self, *args, **kwargs):
        return self._collection.insert_many(*args, **kwargs)


    async def insert_one(self, *args, **kwargs):
        return self._collection.insert_one(*args, **kwargs)

    async def update_one(self, *args, **kwargs):
        return self._collection.update_one(*args, **kwargs)

    async def delete_one(self, *args, **kwargs):
        return self._collection.delete_one(*args, **kwargs)

    async def delete_many(self, *args, **kwargs):
        return self._collection.delete_many(*args, **kwargs)

    def find(self, *args, **kwargs):
        return AsyncCursorWrapper(self._collection.find(*args, **kwargs))


# =========================
# DB Fixture
# =========================

@pytest.fixture
def mock_db(monkeypatch):
    client = mongomock.MongoClient()
    db = client["test_db"]

    # Bungkus semua collection yang dipakai
    db.user = AsyncCollectionWrapper(db.user)
    db.article = AsyncCollectionWrapper(db.article)
    db.comment = AsyncCollectionWrapper(db.comment)
    db.rating = AsyncCollectionWrapper(db.rating)
    db.report_article = AsyncCollectionWrapper(db.report_article)
    db.report_user = AsyncCollectionWrapper(db.report_user)

    # Patch ke SEMUA service
    monkeypatch.setattr(auth_service, "db", db)
    monkeypatch.setattr(article_service, "db", db)
    monkeypatch.setattr(comment_service, "db", db)
    monkeypatch.setattr(rating_service, "db", db)
    monkeypatch.setattr(report_article_service, "db", db)
    monkeypatch.setattr(report_user_service, "db", db)

    return db