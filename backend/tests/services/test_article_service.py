import pytest
from bson import ObjectId
from services.article_service import ArticleService
#1
@pytest.mark.asyncio
async def test_add_article_success(mock_db):
    print("\n[TEST CASE] Add Article - Data Valid")
    print("[INPUT]")
    print(" title=Judul, preview=Preview, content=Isi, tag=gaming, image_bytes=dummy, author_id=user123")
    article_id = await ArticleService.add_article(
        title="Judul",
        preview="Preview",
        content="Isi",
        tag="gaming",
        image_bytes=b"dummy",
        author_id="user123"
    )
    print("[OUTPUT]")
    print(" article_id:", article_id)
    assert article_id is not None
    article = await mock_db.article.find_one({"_id": ObjectId(article_id)})
    print("[RESULT]")
    print(" Artikel tersimpan dan data sesuai")
    assert article["article_title"] == "Judul"
    assert article["article_tag"] == "gaming"
    assert article["report_count"] == 0
    assert article["is_deleted"] is False

#2
@pytest.mark.asyncio
async def test_fetch_article_found(mock_db):
    print("\n[TEST CASE] Fetch Article - Artikel Aktif")
    oid = ObjectId()
    await mock_db.article.insert_one({
        "_id": oid,
        "article_title": "Test",
        "is_deleted": False
    })
    print("[INPUT]")
    print(" article_id:", str(oid))
    article = await ArticleService.fetch_article(str(oid))
    print("[OUTPUT]")
    print(" article:", article)
    assert article is not None
    assert article["_id"] == oid
    print("[RESULT] Artikel berhasil diambil")

#3
@pytest.mark.asyncio
async def test_fetch_article_deleted(mock_db):
    print("\n[TEST CASE] Fetch Article - Artikel Terhapus")
    oid = ObjectId()
    await mock_db.article.insert_one({
        "_id": oid,
        "article_title": "Test",
        "is_deleted": True
    })
    print("[INPUT]")
    print(" article_id:", str(oid))
    article = await ArticleService.fetch_article(str(oid))
    print("[OUTPUT]")
    print(" article:", article)
    assert article is None
    print("[RESULT] Artikel tidak ditampilkan (None)")

#4
class DummyUpdate:
    article_id = None
    article_title = None
    article_preview = None
    article_content = None
    article_tag = None

@pytest.mark.asyncio
async def test_update_article_success(mock_db):
    print("\n[TEST CASE] Update Article - Data Valid")
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
    print("[INPUT]")
    print(" article_id:", data.article_id)
    print(" article_title: New Title")
    result = await ArticleService.update_article(data, image_bytes=None)
    print("[OUTPUT]")
    print(" result:", result)
    assert result is True
    updated = await mock_db.article.find_one({"_id": oid})
    assert updated["article_title"] == "New Title"
    print("[RESULT] Artikel berhasil diperbarui")

#5
@pytest.mark.asyncio
async def test_update_article_invalid_image(mock_db, monkeypatch):
    print("\n[TEST CASE] Update Article - Image Tidak Valid")
    def fake_validate(_):
        return False
    monkeypatch.setattr(
        "services.article_service.validate_image_bytes",
        fake_validate
    )
    data = DummyUpdate()
    data.article_id = str(ObjectId())
    data.article_title = None
    data.article_preview = None
    data.article_content = None
    data.article_tag = None
    print("[INPUT]")
    print(" article_id:", data.article_id)
    print(" image_bytes: invalid")
    result = await ArticleService.update_article(data, image_bytes=b"bad")
    print("[OUTPUT]")
    print(" result:", result)
    assert result == "invalid_image"
    print("[RESULT] Sistem menolak image tidak valid")
