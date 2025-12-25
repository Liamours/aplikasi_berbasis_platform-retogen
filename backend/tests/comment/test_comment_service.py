def test_add_comment_success(client, monkeypatch):

    async def mock_verify_token(token):
        return {"email": "user@test.com"}

    async def mock_find_user(query):
        return {
            "_id": "u1",
            "email": "user@test.com",
            "username": "user"
        }

    async def mock_fetch_article(article_id):
        return {
            "_id": "a1",
            "article_title": "Judul"
        }

    async def mock_add_comment(**kwargs):
        return "comment_id"

    async def mock_get_comments(article_id):
        return []

    async def mock_get_ratings(article_id):
        return []

    monkeypatch.setattr("services.auth_service.AuthService.verify_token", mock_verify_token)
    monkeypatch.setattr("db.connection.db.user.find_one", mock_find_user)
    monkeypatch.setattr("services.article_service.ArticleService.fetch_article", mock_fetch_article)
    monkeypatch.setattr("services.comment_service.CommentService.add_comment", mock_add_comment)
    monkeypatch.setattr("services.comment_service.CommentService.get_comments", mock_get_comments)
    monkeypatch.setattr("services.rating_service.RatingService.get_ratings", mock_get_ratings)

    payload = {
        "token": "token",
        "article_id": "a1",
        "comment_content": "Komentar"
    }

    res = client.post("/comment/add", json=payload)
    assert res.status_code == 200
    assert res.json()["confirmation"] == "successful"
