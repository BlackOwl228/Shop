def test_block_product(client, product):
    response = client.post(f"/admin/products/{product.id}/block")
    assert response.status_code == 200


def test_unblock_product(client, product):
    response = client.post(f"/admin/products/{product.id}/unblock")
    assert response.status_code == 200


def test_suspend_seller(client, seller):
    response = client.delete(f"/admin/sellers/{seller.id}")
    assert response.status_code == 200


def test_approve_seller_request(client, seller):
    response = client.post(f"/admin/sellers/{seller.id}")
    assert response.status_code == 201


def test_admin_complete_order(client, order):
    response = client.patch(f"/admin/orders/{order.id}/complete")
    data = response.json()
    assert "status" in data


def test_admin_cancel_order(client, order):
    response = client.patch(f"/admin/orders/{order.id}/cancel")
    assert response.status_code == 200


def test_admin_delete_review(client, review):
    response = client.delete(f"/admin/reviews/{review.id}")
    assert response.status_code == 204


def test_create_category(client):
    response = client.post("/admin/categories", data={"name": "Техника"})
    assert response.status_code == 201


def test_add_product_to_category(client, product, category):
    response = client.post(f"/admin/products/{product.id}/categories/{category.id}")
    assert response.status_code == 204
