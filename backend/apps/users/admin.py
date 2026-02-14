from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, SellerProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'user_type', 'is_verified', 'balance', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_verified', 'is_active', 'date_joined']
    search_fields = ['email', 'username', 'phone_number']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username', 'phone_number')}),
        ('Account Type', {'fields': ('user_type', 'is_verified', 'balance')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type'),
        }),
    )


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'user', 'business_type', 'is_approved', 'rating', 'total_sales', 'created_at']
    list_filter = ['business_type', 'is_approved', 'created_at']
    search_fields = ['business_name', 'user__email', 'tax_id']
    readonly_fields = ['total_sales', 'rating', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Business Information', {'fields': ('business_name', 'business_type', 'tax_id', 'description')}),
        ('Contact', {'fields': ('address', 'phone')}),
        ('Financial', {'fields': ('bank_account', 'commission_rate', 'total_sales')}),
        ('Status', {'fields': ('is_approved', 'rating')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
