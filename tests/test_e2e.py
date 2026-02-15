def test_full_path(client, seller, buyer):    
    response = client.post("/products", data={"name": "Test_product"})
    assert response.status_code == 201
    data = response.json()
    product_id = data.get("product_id")

    response = client.post(f"/products/{product_id}/variants", data={"name": "Test_variant", "price": 10000, "stock": 10})
    assert response.status_code == 201
    data = response.json()
    variant_id = data.get("variant_id")
    assert variant_id == 1

    response = client.patch(f"/products/{product_id}/variants/{variant_id}/stock", data={"stock_delta": 10})
    assert response.status_code == 204

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["variants"][0]["stock"] == 20

    response = client.post(f"/cart/{variant_id}")
    assert response.status_code == 204

    response = client.get("/cart")
    data = response.json()
    
    order_input = []
    for item in data["items"]:
        order_input.append({
            "variant_id": item["variant"]["id"],
            "quantity": item["quantity"],
            "client_price": item["variant"]["price"],
        })

    response = client.post("/orders", 
                           json=order_input)
    assert response.status_code == 201