"""
Cart app views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Cart, CartItem


class CartViewSet(viewsets.ModelViewSet):
    """Cart viewset - to be implemented"""
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]
