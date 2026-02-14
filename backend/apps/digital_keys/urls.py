from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DigitalKeyViewSet

router = DefaultRouter()
router.register(r'', DigitalKeyViewSet, basename='digital-key')

urlpatterns = [
    path('', include(router.urls)),
]
