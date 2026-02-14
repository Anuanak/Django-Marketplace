from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class UserManager(DjangoUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        # Auto-generate username from email if not provided
        if 'username' not in extra_fields or not extra_fields.get('username'):
            extra_fields['username'] = email.split('@')[0]
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model extending AbstractUser.
    All user data in this model - NO separate UserProfile.
    """
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True, verbose_name='Email Address')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Phone Number')
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='buyer',
        verbose_name='User Type'
    )
    is_verified = models.BooleanField(default=False, verbose_name='Is Verified')
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Account Balance'
    )
    
    # Override username to make it optional
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Auto-generate username from email if not provided
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
    
    @property
    def is_buyer(self):
        return self.user_type == 'buyer'
    
    @property
    def is_seller(self):
        return self.user_type == 'seller'
    
    @property
    def is_marketplace_admin(self):
        return self.user_type == 'admin'


class SellerProfile(models.Model):
    """
    Additional information for sellers.
    Separate model to keep seller-specific data organized.
    """
    BUSINESS_TYPE_CHOICES = (
        ('individual', 'Individual Entrepreneur'),
        ('company', 'Company'),
    )
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='seller_profile',
        verbose_name='User'
    )
    business_name = models.CharField(max_length=255, verbose_name='Business Name')
    business_type = models.CharField(
        max_length=20, 
        choices=BUSINESS_TYPE_CHOICES,
        verbose_name='Business Type'
    )
    tax_id = models.CharField(max_length=50, blank=True, verbose_name='Tax ID / INN')
    bank_account = models.CharField(max_length=100, blank=True, verbose_name='Bank Account')
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('15.00'),
        verbose_name='Commission Rate (%)'
    )
    is_approved = models.BooleanField(default=False, verbose_name='Is Approved')
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=Decimal('0.00'),
        verbose_name='Rating'
    )
    total_sales = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00'),
        verbose_name='Total Sales'
    )
    address = models.TextField(blank=True, verbose_name='Business Address')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Business Phone')
    description = models.TextField(blank=True, verbose_name='Business Description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Seller Profile'
        verbose_name_plural = 'Seller Profiles'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.business_name} ({self.user.email})"
