def test_login_uses_service_stub(client, monkeypatch):
    from apps.fastapi.platform.modules.auth.src import service as auth_service_module

    def fake_login_user(_login_data):
        return {
            "success": True,
            "message": "Successfully logged in",
            "data": {
                "id": "user-123",
                "access_token": "access-token",
                "refresh_token": "refresh-token",
                "token_type": "Bearer",
                "email": "user@example.com",
            },
        }

    monkeypatch.setattr(auth_service_module.auth_service, "login_user", fake_login_user)

    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "secret"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["access_token"] == "access-token"


def test_signup_uses_service_stub(client, monkeypatch):
    from apps.fastapi.platform.modules.auth.src import service as auth_service_module

    def fake_signup_user(_signup_data):
        return {
            "success": True,
            "message": "Successfully registered",
            "data": {
                "id": "user-456",
                "name": "New User",
                "email": "new@example.com",
            },
        }

    monkeypatch.setattr(auth_service_module.auth_service, "signup_user", fake_signup_user)

    response = client.post(
        "/api/auth/signup",
        json={"name": "New User", "email": "new@example.com", "password": "secret"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["email"] == "new@example.com"


def test_login_returns_400_on_value_error(client, monkeypatch):
    from apps.fastapi.platform.modules.auth.src import service as auth_service_module

    def fake_login_user(_login_data):
        raise ValueError("Incorrect email or password")

    monkeypatch.setattr(auth_service_module.auth_service, "login_user", fake_login_user)

    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "wrong"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert payload["message"] == "Incorrect email or password"
