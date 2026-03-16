def test_get_all_categories(client, category):
    response = client.get("/categories")
    assert response.status_code == 200


def test_add_product_to_category(client, product, category):
    response = client.post(f"/products/{product.id}/categories/{category.id}")
    assert response.status_code == 204
