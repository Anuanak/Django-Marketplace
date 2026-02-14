from django.db import models
from django.core.validators import MinValueValidator
from apps.users.models import User
from apps.products.models import Product, ProductVariant


class Cart(models.Model):
    """Shopping cart for users and guests."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart',
        verbose_name='User'
    )
    session_key = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Session Key'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.email}"
        return f"Guest Cart ({self.session_key})"
    
    @property
    def total_items(self):
        """Get total number of items in cart."""
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    @property
    def subtotal(self):
        """Calculate cart subtotal."""
        total = sum(item.total_price for item in self.items.all())
        return total
    
    def merge_with_guest_cart(self, guest_cart):
        """Merge guest cart items into user cart."""
        for guest_item in guest_cart.items.all():
            # Check if item already exists in user cart
            try:
                user_item = self.items.get(
                    product=guest_item.product,
                    variant=guest_item.variant
                )
                # Update quantity
                user_item.quantity += guest_item.quantity
                user_item.save()
            except CartItem.DoesNotExist:
                # Create new item in user cart
                guest_item.cart = self
                guest_item.save()
        
        # Delete guest cart
        guest_cart.delete()


class CartItem(models.Model):
    """Items in shopping cart."""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Cart'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Product'
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart_items',
        verbose_name='Variant'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Quantity'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Added At')
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ['cart', 'product', 'variant']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def unit_price(self):
        """Get unit price (variant price if variant selected)."""
        if self.variant:
            return self.variant.final_price
        return self.product.price
    
    @property
    def total_price(self):
        """Calculate total price for this cart item."""
        return self.unit_price * self.quantity
    
    def clean(self):
        """Validate cart item."""
        from django.core.exceptions import ValidationError
        
        # Check stock availability
        if self.product.product_type == 'physical':
            available_stock = self.variant.stock_quantity if self.variant else self.product.stock_quantity
            if self.quantity > available_stock:
                raise ValidationError(
                    f"Only {available_stock} items available in stock."
                )
