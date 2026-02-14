"""
Orders app views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem


class OrderViewSet(viewsets.ModelViewSet):
    """Order viewset - to be implemented"""
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
