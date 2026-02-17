from django.db import transaction
from products.models import Product
from .status_service import VALID_TRANSITIONS
from .status_service import OrderStatusService

@transaction.atomic
def cancel_order(order):
    if order.status not in ["PENDENTE", "CONFIRMADO"]:
        raise ValueError("Order cannot be cancelled")
    for item in order.items.all():
        product = Product.objects.select_for_update().get(id=item.product.id)
        product.stock += item.quantity
        product.save()
    OrderStatusService.change_status(
        order=order,
        new_status="CANCELADO",
        user="system",
        notes="Order cancelled"
    )