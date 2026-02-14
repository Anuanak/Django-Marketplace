from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import User
from apps.products.models import Product
from apps.orders.models import OrderItem


class Review(models.Model):
    """Product reviews and ratings."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Product'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='User'
    )
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='review',
        verbose_name='Order Item'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Rating'
    )
    title = models.CharField(max_length=200, verbose_name='Review Title')
    comment = models.TextField(verbose_name='Comment')
    is_verified_purchase = models.BooleanField(default=False, verbose_name='Verified Purchase')
    is_approved = models.BooleanField(default=True, verbose_name='Is Approved')
    helpful_count = models.PositiveIntegerField(default=0, verbose_name='Helpful Count')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = ['product', 'user']
        indexes = [
            models.Index(fields=['product', 'is_approved']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating}⭐)"
    
    def save(self, *args, **kwargs):
        # Check if this is from a verified purchase
        if self.order_item and self.order_item.order.payment_status == 'completed':
            self.is_verified_purchase = True
        super().save(*args, **kwargs)


class ReviewHelpful(models.Model):
    """Track users who found reviews helpful."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='helpful_marks',
        verbose_name='Review'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='helpful_reviews',
        verbose_name='User'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        verbose_name = 'Review Helpful Mark'
        verbose_name_plural = 'Review Helpful Marks'
        unique_together = ['review', 'user']
    
    def __str__(self):
        return f"{self.user.email} found review helpful"
