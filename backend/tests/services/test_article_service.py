import pytest
from bson import ObjectId
from services.article_service import ArticleService

@pytest.mark.asyncio
async def test_add_article_success(mock_db):
    article_id = await ArticleService.add_article(
        title="Judul",
        preview="Preview",
        content="Isi",
        tag="gaming",
        image_bytes=b"dummy",
        author_id="user123"
    )

    assert article_id is not None

    article = await mock_db.article.find_one({"_id": ObjectId(article_id)})
    assert article["article_title"] == "Judul"
    assert article["article_tag"] == "gaming"
    assert article["report_count"] == 0
    assert article["is_deleted"] is False

@pytest.mark.asyncio
async def test_fetch_article_found(mock_db):
    oid = ObjectId()
    await mock_db.article.insert_one({
        "_id": oid,
        "article_title": "Test",
        "is_deleted": False
    })

    article = await ArticleService.fetch_article(str(oid))

    assert article is not None
    assert article["_id"] == oid


@pytest.mark.asyncio
async def test_fetch_article_deleted(mock_db):
    oid = ObjectId()
    await mock_db.article.insert_one({
        "_id": oid,
        "article_title": "Test",
        "is_deleted": True
    })

    article = await ArticleService.fetch_article(str(oid))
    assert article is None


class DummyUpdate:
    article_id = None
    article_title = None
    article_preview = None
    article_content = None
    article_tag = None


@pytest.mark.asyncio
async def test_update_article_success(mock_db):
    oid = ObjectId()
    await mock_db.article.insert_one({
        "_id": oid,
        "article_title": "Old",
        "article_preview": "Old",
        "article_content": "Old",
        "article_tag": "old",
        "is_deleted": False
    })

    data = DummyUpdate()
    data.article_id = str(oid)
    data.article_title = "New Title"
    data.article_preview = None
    data.article_content = None
    data.article_tag = None

    result = await ArticleService.update_article(data, image_bytes=None)

    assert result is True

    updated = await mock_db.article.find_one({"_id": oid})
    assert updated["article_title"] == "New Title"

@pytest.mark.asyncio
async def test_update_article_invalid_image(mock_db, monkeypatch):
    def fake_validate(_):
        return False

    monkeypatch.setattr(
        "services.article_service.validate_image_bytes",
        fake_validate
    )

    data = type("D", (), {})()
    data.article_id = str(ObjectId())
    data.article_title = None
    data.article_preview = None
    data.article_content = None
    data.article_tag = None

    result = await ArticleService.update_article(data, image_bytes=b"bad")
    assert result == "invalid_image"


