from django.db import models
from customers.models import Customer
from products.models import Product


class Order(models.Model):
    STATUS_PENDING = "PENDENTE"
    STATUS_CONFIRMED = "CONFIRMADO"
    STATUS_SEPARATED = "SEPARADO"
    STATUS_SHIPPED = "ENVIADO"
    STATUS_DELIVERED = "ENTREGUE"
    STATUS_CANCELED = "CANCELADO"
    STATUS_CHOICES = [
        (STATUS_PENDING, "PENDENTE"),
        (STATUS_CONFIRMED, "CONFIRMADO"),
        (STATUS_SEPARATED, "SEPARADO"),
        (STATUS_SHIPPED, "ENVIADO"),
        (STATUS_DELIVERED, "ENTREGUE"),
        (STATUS_CANCELED, "CANCELADO"),
    ]
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    observations = models.TextField(blank=True)
    idempotency_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Meta:
        db_table = "orders"
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["status"]),
        ]
def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
class Meta:
        db_table = "order_items"
        indexes = [
            models.Index(fields=["order"]),
        ]
def __str__(self):
        return f"Order {self.order_id} - Product {self.product_id}"

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="status_history",
        on_delete=models.CASCADE
    )
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
class Meta:
        db_table = "order_status_history"
        ordering = ["-changed_at"]
def __str__(self):
        return f"{self.order_id}: {self.previous_status} → {self.new_status}"