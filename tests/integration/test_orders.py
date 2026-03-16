def test_create_order(client, variant):
    data = [
        {
            "variant_id": variant.id,
            "quantity": 1,
            "client_price": variant.price,
        }
    ]
    response = client.post("/orders", json=data)
    assert response.status_code == 201


def test_cancel_order(client, order):
    response = client.patch(f"/orders/{order.id}/cancel")
    assert response.status_code == 201


def test_complete_order(client, order):
    response = client.patch(f"/orders/{order.id}/complete")
    assert response.status_code == 400
