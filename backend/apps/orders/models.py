from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from apps.users.models import User
from apps.products.models import Product, ProductVariant


class Order(models.Model):
    """Customer order."""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_SOURCE_CHOICES = (
        ('balance', 'Account Balance'),
        ('card', 'Credit/Debit Card'),
        ('external', 'External Payment Gateway'),
    )
    
    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Order Number'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='User'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Total Amount'
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Discount Amount'
    )
    promo_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Promo Code Used'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Order Status'
    )
    payment_method = models.CharField(max_length=50, blank=True, verbose_name='Payment Method')
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='Payment Status'
    )
    payment_source = models.CharField(
        max_length=20,
        choices=PAYMENT_SOURCE_CHOICES,
        default='external',
        verbose_name='Payment Source'
    )
    shipping_address = models.JSONField(default=dict, blank=True, verbose_name='Shipping Address')
    billing_address = models.JSONField(default=dict, blank=True, verbose_name='Billing Address')
    notes = models.TextField(blank=True, verbose_name='Order Notes')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_order_number():
        """Generate unique order number."""
        return f"ORD-{uuid.uuid4().hex[:12].upper()}"
    
    @property
    def final_amount(self):
        """Calculate final amount after discount."""
        return self.total_amount - self.discount_amount
    
    @property
    def has_digital_items(self):
        """Check if order contains digital products."""
        return self.items.filter(is_digital=True).exists()
    
    @property
    def has_physical_items(self):
        """Check if order contains physical products."""
        return self.items.filter(is_digital=False).exists()


class OrderItem(models.Model):
    """Items in an order."""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Order'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name='Product'
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items',
        verbose_name='Variant'
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sold_items',
        verbose_name='Seller'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantity'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Unit Price (Snapshot)'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Subtotal'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Item Status'
    )
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Commission Rate (%)'
    )
    commission_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Commission Amount'
    )
    is_digital = models.BooleanField(default=False, verbose_name='Is Digital Product')
    product_name = models.CharField(max_length=255, verbose_name='Product Name (Snapshot)')
    product_sku = models.CharField(max_length=100, verbose_name='SKU (Snapshot)')
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['id']
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity} (Order #{self.order.order_number})"
    
    @property
    def seller_earnings(self):
        """Calculate seller earnings after commission."""
        return self.subtotal - self.commission_amount
