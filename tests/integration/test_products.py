# products
def test_create_product(client):
    response = client.post("/products", data={"name": "Тестовый продукт"})
    assert response.status_code == 201


def test_create_variant(client, product):
    response = client.post(
        f"/products/{product.id}/variants", data={"name": "Тестовый вариант", "price": 10000}
    )
    assert response.status_code == 201


def test_get_product(client, product, fake_redis):
    response = client.get(f"/products/{product.id}")
    assert response.status_code == 200


def test_change_product(client, product):
    response = client.patch(f"/products/{product.id}", data={"name": "Тестовый продукт в2"})
    assert response.status_code == 204


def test_change_variant(client, product, variant):
    response = client.patch(
        f"/products/{product.id}/variants/{variant.id}", data={"name": "Тестовый продукт в2", "price": 15000}
    )
    assert response.status_code == 204


def test_change_variant_stock(client, product, variant):
    response = client.patch(f"/products/{product.id}/variants/{variant.id}/stock", data={"stock_delta": 20})
    assert response.status_code == 204


def test_search(client):
    response = client.get("/search?min_price=0")
    assert response.status_code == 200
