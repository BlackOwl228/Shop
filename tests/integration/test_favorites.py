def test_add_product_to_favorites(client, product):
    response = client.post(f"/favorites/{product.id}")
    assert response.status_code == 201

    response = client.get("/favorites")
    assert response.status_code == 200

    response = client.delete(f"/favorites/{product.id}")
    assert response.status_code == 204
