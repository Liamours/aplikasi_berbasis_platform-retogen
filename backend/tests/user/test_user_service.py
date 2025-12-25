def test_make_admin_success(client, monkeypatch):

    async def mock_verify_token(token):
        return {"email": "admin@test.com"}

    async def mock_is_admin(payload):
        return True

    async def mock_get_user_by_id(user_id):
        return {"_id": user_id, "role": "user"}

    async def mock_make_admin(user_id):
        return True

    monkeypatch.setattr("services.auth_service.AuthService.verify_token", mock_verify_token)
    monkeypatch.setattr("services.auth_service.AuthService.is_admin", mock_is_admin)
    monkeypatch.setattr("services.user_service.UserService.get_user_by_id", mock_get_user_by_id)
    monkeypatch.setattr("services.user_service.UserService.make_admin", mock_make_admin)

    payload = {
        "token": "token",
        "user_id": "u1"
    }

    res = client.post("/user/make_admin", json=payload)
    assert res.json()["confirmation"] == "successful: role updated to admin"
