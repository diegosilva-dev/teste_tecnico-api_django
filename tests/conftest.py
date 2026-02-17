import pytest
from rest_framework.test import APIClient
from customers.models import Customer
from products.models import Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def customer():
    return Customer.objects.create(
        name="Cliente Teste",
        document="12345678900",
        email="cliente@test.com",
        phone="11999999999",
        address="Rua Teste",
        is_active=True,
    )
    
@pytest.fixture
def product():
    return Product.objects.create(
        sku="PROD-001",
        name="Produto Teste",
        description="Produto Teste",
        price=100,
        stock=10,
        is_active=True,
    )