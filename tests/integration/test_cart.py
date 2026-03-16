def test_add_product_to_cart(client, variant):
    response = client.post(f"/cart/{variant.id}")
    assert response.status_code == 204

    response = client.patch(f"/cart/{variant.id}", data={"quantity": 3})
    assert response.status_code == 204

    response = client.get("/cart")
    assert response.status_code == 200

    response = client.delete(f"/cart/{variant.id}")
    assert response.status_code == 204
