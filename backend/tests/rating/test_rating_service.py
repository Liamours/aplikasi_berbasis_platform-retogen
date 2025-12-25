def test_add_rating_success(client, monkeypatch):

    async def mock_verify_token(token):
        return {"email": "user@test.com"}

    async def mock_find_user(query):
        return {
            "_id": "u1",
            "username": "user",
            "role": "user"
        }

    async def mock_fetch_article(article_id):
        return {
            "_id": "a1",
            "article_title": "Judul",
            "is_deleted": False
        }

    async def mock_get_rating_by_user(*args, **kwargs):
        return None

    async def mock_add_rating(*args, **kwargs):
        return "rating_id"

    async def mock_get_comments(article_id):
        return []

    async def mock_get_ratings(article_id):
        return []

    monkeypatch.setattr("services.auth_service.AuthService.verify_token", mock_verify_token)
    monkeypatch.setattr("db.connection.db.user.find_one", mock_find_user)
    monkeypatch.setattr("services.rating_service.RatingService.fetch_article", mock_fetch_article)
    monkeypatch.setattr("services.rating_service.RatingService.get_rating_by_user", mock_get_rating_by_user)
    monkeypatch.setattr("services.rating_service.RatingService.add_rating", mock_add_rating)
    monkeypatch.setattr("services.rating_service.RatingService.get_comments", mock_get_comments)
    monkeypatch.setattr("services.rating_service.RatingService.get_ratings", mock_get_ratings)

    payload = {
        "token": "token",
        "article_id": "a1",
        "rating_value": 5
    }

    res = client.post("/rating/add", json=payload)
    assert res.json()["confirmation"] == "successful"
