from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Avg, Count
from .models import (
    SellerProfile, Category, Product, ProductImage, Cart, CartItem,
    Order, OrderItem, Review, Payment, Wishlist, Notification
)


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'account_balance', 'average_rating', 'total_sales', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at', 'average_rating')
    search_fields = ('store_name', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'average_rating', 'total_sales')
    fieldsets = (
        ('Store Information', {
            'fields': ('user', 'store_name', 'store_description', 'store_image')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Financial Information', {
            'fields': ('bank_account', 'account_balance', 'commission_rate')
        }),
        ('Performance', {
            'fields': ('average_rating', 'total_sales', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Number of Products'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'current_price', 'quantity_in_stock', 'average_rating', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('name', 'seller__username', 'category__name')
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'view_count', 'average_rating', 'review_count')
    
    fieldsets = (
        ('Product Information', {
            'fields': ('seller', 'name', 'slug', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price')
        }),
        ('Inventory', {
            'fields': ('quantity_in_stock', 'sku', 'weight', 'dimensions')
        }),
        ('Status & Rating', {
            'fields': ('status', 'average_rating', 'review_count')
        }),
        ('Tags & Views', {
            'fields': ('tags', 'view_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary', 'uploaded_at')
    search_fields = ('product__name', 'alt_text')
    readonly_fields = ('uploaded_at', 'image_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image Preview'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'total_price', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'get_total')
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('added_at',)
    
    def get_total(self, obj):
        return f'${obj.get_total()}'
    get_total.short_description = 'Total'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'quantity', 'subtotal')
    fields = ('product', 'product_name', 'product_price', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'buyer', 'seller', 'status_badge', 'payment_status_badge', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_id', 'buyer__username', 'seller__username', 'shipping_email')
    inlines = [OrderItemInline]
    readonly_fields = ('order_id', 'created_at', 'updated_at', 'shipped_at', 'delivered_at')
    
    fieldsets = (
        ('Order Details', {
            'fields': ('order_id', 'buyer', 'seller', 'status', 'payment_status')
        }),
        ('Financial Information', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total_amount')
        }),
        ('Shipping Address', {
            'fields': ('shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country')
        }),
        ('Tracking', {
            'fields': ('tracking_number', 'courier')
        }),
        ('Notes', {
            'fields': ('buyer_notes', 'seller_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FF9800',
            'confirmed': '#2196F3',
            'processing': '#9C27B0',
            'shipped': '#4CAF50',
            'delivered': '#8BC34A',
            'cancelled': '#F44336',
            'refunded': '#E91E63',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#999'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def payment_status_badge(self, obj):
        colors = {
            'unpaid': '#FF9800',
            'paid': '#4CAF50',
            'failed': '#F44336',
            'refunded': '#E91E63',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.payment_status, '#999'),
            obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment Status'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'product_price', 'subtotal')
    list_filter = ('order__created_at',)
    search_fields = ('order__order_id', 'product_name')
    readonly_fields = ('subtotal',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'buyer', 'rating_stars', 'is_verified_purchase', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'is_approved', 'created_at')
    search_fields = ('product__name', 'buyer__username', 'title')
    readonly_fields = ('created_at', 'updated_at', 'helpful_count', 'unhelpful_count')
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'buyer', 'order', 'rating', 'title', 'comment')
        }),
        ('Review Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_verified_purchase', 'is_approved')
        }),
        ('Engagement', {
            'fields': ('helpful_count', 'unhelpful_count')
        }),
        ('Seller Response', {
            'fields': ('seller_response', 'seller_response_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def rating_stars(self, obj):
        return '⭐' * obj.rating
    rating_stars.short_description = 'Rating'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'status_badge', 'transaction_id', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order__order_id', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('order', 'payment_method', 'amount', 'status')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'receipt_url')
        }),
        ('Refund Information', {
            'fields': ('refund_amount', 'refund_reason', 'refund_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FF9800',
            'completed': '#4CAF50',
            'failed': '#F44336',
            'refunded': '#E91E63',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#999'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_count')
    search_fields = ('user__username', 'user__email')
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at',)
