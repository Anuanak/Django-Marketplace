from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet

router = DefaultRouter()
router.register(r'', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    # Custom endpoints for cart items
    path('items/<int:item_id>/', CartViewSet.as_view({
        'delete': 'remove_item',
        'patch': 'update_item'
    }), name='cart-item-detail'),
]
