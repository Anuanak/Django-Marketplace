from django.db import models
from apps.products.models import Product
from apps.users.models import User


class DigitalKey(models.Model):
    """Digital product keys/codes for automatic delivery."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='digital_keys',
        limit_choices_to={'product_type': 'digital'},
        verbose_name='Product'
    )
    key_code = models.TextField(verbose_name='Key/Code')
    is_used = models.BooleanField(default=False, verbose_name='Is Used')
    purchased_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchased_keys',
        verbose_name='Purchased By'
    )
    purchased_at = models.DateTimeField(null=True, blank=True, verbose_name='Purchased At')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        verbose_name = 'Digital Key'
        verbose_name_plural = 'Digital Keys'
        ordering = ['is_used', '-created_at']
        indexes = [
            models.Index(fields=['product', 'is_used']),
        ]
    
    def __str__(self):
        status = "Used" if self.is_used else "Available"
        return f"{self.product.name} - {status}"
    
    def mark_as_used(self, user, order_item=None):
        """Mark key as used and assign to user."""
        self.is_used = True
        self.purchased_by = user
        self.purchased_at = models.DateTimeField(auto_now_add=True)
        self.save()
        
        if order_item:
            DigitalKeyDelivery.objects.create(
                order_item=order_item,
                key=self
            )


class DigitalKeyDelivery(models.Model):
    """Track delivery of digital keys to orders."""
    order_item = models.OneToOneField(
        'orders.OrderItem',
        on_delete=models.CASCADE,
        related_name='digital_key_delivery',
        verbose_name='Order Item'
    )
    key = models.ForeignKey(
        DigitalKey,
        on_delete=models.CASCADE,
        related_name='deliveries',
        verbose_name='Digital Key'
    )
    delivered_at = models.DateTimeField(auto_now_add=True, verbose_name='Delivered At')
    
    class Meta:
        verbose_name = 'Digital Key Delivery'
        verbose_name_plural = 'Digital Key Deliveries'
        ordering = ['-delivered_at']
    
    def __str__(self):
        return f"Key delivered for Order #{self.order_item.order.order_number}"
