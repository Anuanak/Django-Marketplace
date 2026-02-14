from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, SellerProfileViewSet, RegisterView, 
    LoginView, LogoutView, ChangePasswordView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'seller-profiles', SellerProfileViewSet, basename='seller-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
