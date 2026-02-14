from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from decimal import Decimal
from apps.users.models import User


class Category(models.Model):
    """Product category with hierarchical structure."""
    name = models.CharField(max_length=255, verbose_name='Category Name')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Parent Category'
    )
    icon = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Icon')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    order = models.IntegerField(default=0, verbose_name='Display Order')
    description = models.TextField(blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def full_path(self):
        """Get full category path (e.g., 'Electronics > Phones > Smartphones')"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name


class Product(models.Model):
    """Main product model for both physical and digital products."""
    PRODUCT_TYPE_CHOICES = (
        ('physical', 'Physical Product'),
        ('digital', 'Digital Product'),
    )
    
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        limit_choices_to={'user_type': 'seller'},
        verbose_name='Seller'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name='Category'
    )
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default='physical',
        verbose_name='Product Type'
    )
    name = models.CharField(max_length=255, verbose_name='Product Name')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Price'
    )
    compare_at_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Compare at Price'
    )
    sku = models.CharField(max_length=100, unique=True, verbose_name='SKU')
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Stock Quantity')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    is_approved = models.BooleanField(default=False, verbose_name='Is Approved by Admin')
    sold_count = models.PositiveIntegerField(default=0, verbose_name='Sold Count')
    view_count = models.PositiveIntegerField(default=0, verbose_name='View Count')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['seller', 'is_active']),
            models.Index(fields=['category', 'is_active', 'is_approved']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['-sold_count']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def is_in_stock(self):
        """Check if product is in stock."""
        if self.product_type == 'digital':
            # For digital products, check if there are unused keys
            return self.digital_keys.filter(is_used=False).exists()
        return self.stock_quantity > 0
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage if compare_at_price is set."""
        if self.compare_at_price and self.compare_at_price > self.price:
            discount = ((self.compare_at_price - self.price) / self.compare_at_price) * 100
            return round(discount, 2)
        return 0
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews."""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 2)
        return 0


class ProductImage(models.Model):
    """Product images with ordering."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Product'
    )
    image = models.ImageField(upload_to='products/', verbose_name='Image')
    is_primary = models.BooleanField(default=False, verbose_name='Is Primary Image')
    order = models.IntegerField(default=0, verbose_name='Display Order')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['order', '-is_primary']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"
    
    def save(self, *args, **kwargs):
        # If this is set as primary, unset other primary images
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductVariant(models.Model):
    """Product variants for size, color, etc."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name='Product'
    )
    name = models.CharField(max_length=255, verbose_name='Variant Name')
    sku = models.CharField(max_length=100, unique=True, verbose_name='SKU')
    price_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Price Adjustment'
    )
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Stock Quantity')
    attributes = models.JSONField(default=dict, verbose_name='Attributes')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    
    class Meta:
        verbose_name = 'Product Variant'
        verbose_name_plural = 'Product Variants'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
    @property
    def final_price(self):
        """Calculate final price with adjustment."""
        return self.product.price + self.price_adjustment


class Wishlist(models.Model):
    """User wishlist for products."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist_items',
        verbose_name='User'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlisted_by',
        verbose_name='Product'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Added At')
    
    class Meta:
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'
        unique_together = ['user', 'product']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name}"


class PromoCode(models.Model):
    """Promotional discount codes."""
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )
    
    code = models.CharField(max_length=50, unique=True, verbose_name='Promo Code')
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        verbose_name='Discount Type'
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Discount Value'
    )
    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Minimum Purchase Amount'
    )
    max_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Maximum Discount Amount'
    )
    valid_from = models.DateTimeField(verbose_name='Valid From')
    valid_to = models.DateTimeField(verbose_name='Valid To')
    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Usage Limit'
    )
    used_count = models.PositiveIntegerField(default=0, verbose_name='Used Count')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        verbose_name = 'Promo Code'
        verbose_name_plural = 'Promo Codes'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.code
    
    def is_valid(self):
        """Check if promo code is valid."""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False, "Promo code is inactive."
        
        if now < self.valid_from:
            return False, "Promo code is not yet valid."
        
        if now > self.valid_to:
            return False, "Promo code has expired."
        
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False, "Promo code usage limit reached."
        
        return True, "Promo code is valid."
    
    def calculate_discount(self, order_amount):
        """Calculate discount amount for given order amount."""
        if self.discount_type == 'percentage':
            discount = (order_amount * self.discount_value) / 100
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:
            discount = self.discount_value
        
        return min(discount, order_amount)
