from django.db import transaction
from orders.models import OrderStatusHistory

class OrderStatusService:
    VALID_TRANSITIONS = {
        "PENDENTE": ["CONFIRMADO", "CANCELADO"],
        "CONFIRMADO": ["SEPARADO", "CANCELADO"],
        "SEPARADO": ["ENVIADO"],
        "ENVIADO": ["ENTREGUE"],
        "ENTREGUE": [],
        "CANCELADO": [],
    }
    @staticmethod
    @transaction.atomic
    def change_status(*, order, new_status: str, user: str, notes: str = ""):
        allowed = OrderStatusService.VALID_TRANSITIONS[order.status]
        if new_status not in allowed:
            raise ValueError("Invalid status transition")
        OrderStatusHistory.objects.create(
            order=order,
            previous_status=order.status,
            new_status=new_status,
            changed_by=user,
            notes=notes,
        )
        order.status = new_status
        order.save()