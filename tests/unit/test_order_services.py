import pytest
from orders.services.order_service import OrderService

@pytest.mark.django_db(transaction=True)
def test_order_creation_fails_atomically(customer, product):
    """
    Pedido com 2 itens:
    - Item 1: estoque OK
    - Item 2: estoque insuficiente
    Resultado: pedido NÃO é criado e estoque NÃO é alterado
    """
    data = {
        "customer_id": customer.id,
        "items": [
            {"product_id": product.id, "quantity": 8},
            {"product_id": product.id, "quantity": 5},
        ]
    }
    with pytest.raises(ValueError):
        OrderService.create_order(
            data=data,
            idempotency_key="atomic-test",
            user="test",
        )
    product.refresh_from_db()
    assert product.stock == 10