from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import (
    ProductViewSet, CategoryViewSet, CartViewSet, OrderViewSet,
    ReviewViewSet, SellerProfileViewSet, WishlistViewSet, register_user
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'sellers', SellerProfileViewSet, basename='seller')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
    # Authentication endpoints
    path('auth/login/', obtain_auth_token, name='api_token_auth'),
    path('auth/register/', register_user, name='api_register'),
]
