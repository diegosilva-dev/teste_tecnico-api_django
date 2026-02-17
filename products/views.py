from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer, ProductStockUpdateSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    @action(detail=True, methods=["patch"])
    def stock(self, request, pk=None):
        serializer = ProductStockUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = self.get_object()
        product.stock = serializer.validated_data["stock"]
        product.save()
        return Response(
            ProductSerializer(product).data,
            status=status.HTTP_200_OK
        )