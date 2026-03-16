def test_registration(client, fake_redis):
    response = client.post(
        "/reg",
        data={"name": "Test_name1234", "email": "example1234@gmail.com", "password": "Test_password1234"},
    )
    assert response.status_code == 202


def test_login_success(client, fake_redis):
    response = client.post(
        "/login",
        data={"username": "example@gmail.com", "password": "Test_password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 201


def test_login_wrong_password(client, fake_redis):
    response = client.post(
        "/login",
        data={"username": "example@gmail.com", "password": "Wrong_password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


def test_logout_user(client, refresh_token):
    response = client.post("/logout", data={"token": refresh_token})
    assert response.status_code == 204


def test_verify_email(client, email_token):
    response = client.post(f"/verify/{email_token}")
    assert response.status_code == 204


def test_refresh_token(client, refresh_token):
    response = client.post("/refresh", data={"token": refresh_token})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_wrong_refresh_token(client, refresh_token):
    response = client.post("/refresh", data={"token": "wrong_refresh_token"})
    assert response.status_code == 401
