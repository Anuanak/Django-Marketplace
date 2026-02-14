"""
Digital Keys app views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import DigitalKey, DigitalKeyDelivery


class DigitalKeyViewSet(viewsets.ModelViewSet):
    """Digital key viewset - to be implemented"""
    queryset = DigitalKey.objects.all()
    permission_classes = [IsAuthenticated]
