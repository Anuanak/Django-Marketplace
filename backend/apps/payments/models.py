from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.users.models import User
from apps.orders.models import Order


class BalanceTransaction(models.Model):
    """Track all balance transactions for users."""
    TRANSACTION_TYPE_CHOICES = (
        ('deposit', 'Deposit/Top-up'),
        ('purchase', 'Purchase'),
        ('refund', 'Refund'),
        ('withdrawal', 'Withdrawal'),
        ('commission', 'Seller Commission'),
        ('earning', 'Seller Earning'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='balance_transactions',
        verbose_name='User'
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='Transaction Type'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Amount'
    )
    balance_after = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Balance After Transaction'
    )
    description = models.TextField(verbose_name='Description')
    related_order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='balance_transactions',
        verbose_name='Related Order'
    )
    metadata = models.JSONField(default=dict, blank=True, verbose_name='Additional Metadata')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        verbose_name = 'Balance Transaction'
        verbose_name_plural = 'Balance Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['transaction_type', '-created_at']),
        ]
    
    def __str__(self):
        sign = '+' if self.transaction_type in ['deposit', 'refund', 'earning'] else '-'
        return f"{self.user.email} - {sign}{self.amount} ({self.transaction_type})"


class BalanceTopUp(models.Model):
    """Balance top-up requests."""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('card', 'Credit/Debit Card'),
        ('yookassa', 'YooKassa'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='balance_topups',
        verbose_name='User'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Top-up Amount'
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Payment Method'
    )
    payment_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='External Payment ID'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    payment_data = models.JSONField(default=dict, blank=True, verbose_name='Payment Data')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Completed At')
    
    class Meta:
        verbose_name = 'Balance Top-up'
        verbose_name_plural = 'Balance Top-ups'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['payment_id']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} ({self.status})"
    
    def complete_topup(self):
        """Complete the top-up and update user balance."""
        from django.utils import timezone
        from django.db import transaction
        
        with transaction.atomic():
            # Update user balance
            user = User.objects.select_for_update().get(pk=self.user.pk)
            user.balance += self.amount
            user.save()
            
            # Create balance transaction
            BalanceTransaction.objects.create(
                user=user,
                transaction_type='deposit',
                amount=self.amount,
                balance_after=user.balance,
                description=f'Balance top-up via {self.get_payment_method_display()}',
                metadata={'topup_id': self.id}
            )
            
            # Update status
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()


class PaymentWebhook(models.Model):
    """Store webhook events from payment providers."""
    provider = models.CharField(max_length=50, verbose_name='Payment Provider')
    event_type = models.CharField(max_length=100, verbose_name='Event Type')
    event_id = models.CharField(max_length=255, unique=True, verbose_name='Event ID')
    payload = models.JSONField(verbose_name='Webhook Payload')
    processed = models.BooleanField(default=False, verbose_name='Processed')
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name='Processed At')
    error_message = models.TextField(blank=True, verbose_name='Error Message')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Received At')
    
    class Meta:
        verbose_name = 'Payment Webhook'
        verbose_name_plural = 'Payment Webhooks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.provider} - {self.event_type} ({self.event_id})"
