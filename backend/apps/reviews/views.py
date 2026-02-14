"""
Reviews app views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Review, ReviewHelpful


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset - to be implemented"""
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
