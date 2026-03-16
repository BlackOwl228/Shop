def test_get_profile(client):
    response = client.get("/me")
    assert response.status_code == 200


def test_change_name(client):
    response = client.patch("/me/name", data={"new_name": "Test_name"})
    assert response.status_code == 200


"""async def test_change_avatar(client, buyer, avatar: UploadFile):
    response = client.patch("/me/avatar", data={"name": "Test_name"})
    assert response.status_code == 202"""


def test_change_password(client):
    response = client.patch(
        "/me/password", data={"password": "Test_password", "new_password": "Test_password123"}
    )
    assert response.status_code == 200


def test_get_my_orders(client):
    response = client.get("/me/orders")
    assert response.status_code == 200


def test_create_seller_request(client):
    response = client.post("/me/seller-request", data={"company_name": "Test_company"})
    assert response.status_code == 201
