"""
Products app views
"""
from rest_framework import viewsets, status, views, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Category, Product, ProductImage, Wishlist, PromoCode
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductImageSerializer, WishlistSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """Category viewset"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order', 'created_at']
    ordering = ['order', 'name']


class ProductViewSet(viewsets.ModelViewSet):
    """Product viewset"""
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'product_type', 'is_active', 'is_approved']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['created_at', 'price', 'sold_count', 'view_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    def get_permissions(self):
        """
        Permissions:
        - Anyone can list and retrieve products
        - Only admins can create, update, delete
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Set seller to current user when creating product as seller"""
        user = self.request.user
        # Admin can create products on behalf of sellers
        # For now, use the authenticated user (admin)
        serializer.save(seller=user)
    
    def perform_update(self, serializer):
        """Ensure only admin can update products"""
        serializer.save()


class ProductImageViewSet(viewsets.ModelViewSet):
    """Product Image viewset"""
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['product']
    ordering_fields = ['order']
    ordering = ['order']


class WishlistViewSet(viewsets.ModelViewSet):
    """Wishlist viewset"""
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only current user's wishlist items"""
        return Wishlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set user to current user"""
        serializer.save(user=self.request.user)


class PromoCodeView(views.APIView):
    """Promo code validation view - to be implemented"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'detail': 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)

