import pytest
from unittest.mock import AsyncMock

def test_add_article_success(client, monkeypatch):

    # --- MOCK TOKEN ---
    async def mock_verify_token(token):
        return {"email": "admin@test.com"}

    async def mock_is_admin(payload):
        return True

    async def mock_find_user(query):
        return {
            "_id": "123",
            "email": "admin@test.com",
            "role": "admin"
        }

    async def mock_add_article(title, preview, content, tag, image, author_id):
        return "article_id"

    monkeypatch.setattr(
        "services.auth_service.AuthService.verify_token",
        mock_verify_token
    )
    monkeypatch.setattr(
        "services.auth_service.AuthService.is_admin",
        mock_is_admin
    )
    monkeypatch.setattr(
        "db.connection.db.user.find_one",
        mock_find_user
    )
    monkeypatch.setattr(
        "services.article_service.ArticleService.add_article",
        mock_add_article
    )

    payload = {
        "token": "valid_token",
        "article_title": "Judul",
        "article_preview": "Preview",
        "article_content": "Isi artikel",
        "article_tag": "gaming",
        "article_image": "aGVsbG8="  # base64
    }

    res = client.post("/article/add", json=payload)
    body = res.json()

    assert res.status_code == 200
    assert body["confirmation"] == "success: article added"
