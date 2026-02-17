from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Order
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer
)
from .services.order_service import OrderService
from .services.status_service import OrderStatusService
from .services.cancel_service import cancel_order

class OrderViewSet(ViewSet):
    def create(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            return Response(
                {"error": "Idempotency-Key header is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        order = OrderService.create_order(
            data=serializer.validated_data,
            idempotency_key=idempotency_key,
            user=str(request.user)
        )
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
        
    def list(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        return Response(OrderSerializer(order).data)
    
    def partial_update(self, request, pk=None):
        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = get_object_or_404(Order, pk=pk)
        OrderStatusService.change_status(
            order=order,
            new_status=serializer.validated_data["status"],
            user=str(request.user),
            notes=serializer.validated_data.get("notes", "")
        )
        return Response(status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        cancel_order(order)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    