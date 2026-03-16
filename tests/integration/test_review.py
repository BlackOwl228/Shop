def test_create_review(client, product):
    response = client.post(f"/products/{product.id}/reviews", data={"rating": 5})
    assert response.status_code == 201


def test_get_product_reviews(client, product):
    response = client.get(f"/products/{product.id}/reviews")
    assert response.status_code == 200


def test_edit_review(client, review):
    response = client.patch(f"/reviews/{review.id}", data={"rating": 4})
    assert response.status_code == 204


def test_delete_review(client, review):
    response = client.delete(f"/reviews/{review.id}")
    assert response.status_code == 204
