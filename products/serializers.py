from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "description",
            "price",
            "stock",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
        
class ProductStockUpdateSerializer(serializers.Serializer):
    stock = serializers.IntegerField(min_value=0)