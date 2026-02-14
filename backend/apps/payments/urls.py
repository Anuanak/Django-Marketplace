from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BalanceTransactionViewSet, BalanceTopUpView, BalanceView

router = DefaultRouter()
router.register(r'transactions', BalanceTransactionViewSet, basename='balance-transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('balance/', BalanceView.as_view(), name='balance'),
    path('topup/', BalanceTopUpView.as_view(), name='balance-topup'),
]
