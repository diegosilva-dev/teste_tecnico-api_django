from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Meta:
        db_table = "products"
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["is_active"]),
        ]
def __str__(self):
        return f"{self.sku} - {self.name}"