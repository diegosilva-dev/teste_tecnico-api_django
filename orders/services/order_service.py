from django.db import transaction
from products.models import Product
from orders.models import Order, OrderItem
from django.core.cache import cache
from decimal import Decimal
import uuid

from customers.models import Customer
from products.models import Product
from orders.models import Order, OrderItem

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(*, data: dict, idempotency_key: str, user: str) -> Order:
        """
        Cria um pedido garantindo:
        - Idempotência
        - Reserva atômica de estoque
        - Proteção contra concorrência
        """
        cache_key = f"idempotency:{idempotency_key}"
        cached_order_id = cache.get(cache_key)
        if cached_order_id:
            return Order.objects.get(id=cached_order_id)
        customer = Customer.objects.get(
            id=data["customer_id"],
            is_active=True,
            deleted_at__isnull=True
        )
        total_amount = Decimal("0.00")
        products_map = {}
        # 🔒 LOCK DE ESTOQUE
        for item in data["items"]:
            product = Product.objects.select_for_update().get(
                id=item["product_id"],
                is_active=True
            )
            if product.stock < item["quantity"]:
                raise ValueError("Insufficient stock")
            products_map[product.id] = product
            total_amount += product.price * item["quantity"]
            order = Order.objects.create(
            order_number=str(uuid.uuid4())[:8],
            customer=customer,
            total_amount=total_amount,
            observations=data.get("observations", ""),
            idempotency_key=idempotency_key,
        )
        for item in data["items"]:
            product = products_map[item["product_id"]]
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                unit_price=product.price,
                subtotal=product.price * item["quantity"],
            )
            product.stock -= item["quantity"]
            product.save()
        cache.set(cache_key, order.id, timeout=3600)
        return order