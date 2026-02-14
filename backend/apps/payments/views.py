"""
Payments app views
"""
from rest_framework import viewsets, status, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import BalanceTransaction, BalanceTopUp


class BalanceTransactionViewSet(viewsets.ModelViewSet):
    """Balance transaction viewset - to be implemented"""
    queryset = BalanceTransaction.objects.all()
    permission_classes = [IsAuthenticated]


class BalanceView(views.APIView):
    """Balance view - to be implemented"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'balance': str(request.user.balance)})


class BalanceTopUpView(views.APIView):
    """Balance top-up view - to be implemented"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'detail': 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)
