import pytest

@pytest.mark.django_db
def test_order_creation_is_idempotent(api_client, customer, product):
    payload = {
        "customer_id": customer.id,
        "items": [
            {"product_id": product.id, "quantity": 2}
        ]
    }
    headers = {"HTTP_IDEMPOTENCY_KEY": "idem-123"}
    response1 = api_client.post(
        "/api/v1/orders/",
        payload,
        format="json",
        **headers
    )
    response2 = api_client.post(
        "/api/v1/orders/",
        payload,
        format="json",
        **headers
    )
    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response1.data["id"] == response2.data["id"]
    
from threading import Thread

@pytest.mark.django_db(transaction=True)
def test_concurrent_stock_reservation(api_client, customer, product):
    payload = {
        "customer_id": customer.id,
        "items": [
            {"product_id": product.id, "quantity": 8}
        ]
    }
    headers = {"HTTP_IDEMPOTENCY_KEY": "concurrent"}
    responses = []
def create_order():
        r = api_client.post(
            "/api/v1/orders/",
            payload,
            format="json",
            **headers
        )
        responses.append(r.status_code)
        t1 = Thread(target=create_order)
        t2 = Thread(target=create_order)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        product.refresh_from_db()
    # Apenas um pedido deve ser aceito
        assert responses.count(201) == 1
        assert product.stock in (2, 10)