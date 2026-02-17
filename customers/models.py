from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=20, unique=True)  # CPF/CNPJ
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Meta:
        db_table = "customers"
        indexes = [
            models.Index(fields=["document"]),
        ]
def __str__(self):
        return self.name