from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, Wishlist, PromoCode


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary', 'order']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ['name', 'sku', 'price_adjustment', 'stock_quantity', 'is_active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'category', 'product_type', 'price', 'stock_quantity', 
                    'is_active', 'is_approved', 'sold_count', 'created_at']
    list_filter = ['product_type', 'is_active', 'is_approved', 'category', 'created_at']
    search_fields = ['name', 'description', 'sku', 'seller__email']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['sold_count', 'view_count', 'created_at', 'updated_at']
    inlines = [ProductImageInline, ProductVariantInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('seller', 'category', 'product_type', 'name', 'slug', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_at_price')
        }),
        ('Inventory', {
            'fields': ('sku', 'stock_quantity')
        }),
        ('Status', {
            'fields': ('is_active', 'is_approved')
        }),
        ('Statistics', {
            'fields': ('sold_count', 'view_count', 'created_at', 'updated_at')
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'sku', 'price_adjustment', 'stock_quantity', 'is_active']
    list_filter = ['is_active', 'product__category']
    search_fields = ['name', 'sku', 'product__name']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__email', 'product__name']


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 
                    'used_count', 'usage_limit', 'is_active']
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_to']
    search_fields = ['code']
    readonly_fields = ['used_count', 'created_at']
