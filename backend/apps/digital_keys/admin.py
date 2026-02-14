from django.contrib import admin
from .models import DigitalKey, DigitalKeyDelivery


@admin.register(DigitalKey)
class DigitalKeyAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_used', 'purchased_by', 'purchased_at', 'created_at']
    list_filter = ['is_used', 'created_at', 'purchased_at']
    search_fields = ['product__name', 'key_code', 'purchased_by__email']
    readonly_fields = ['purchased_by', 'purchased_at', 'created_at']
    
    fieldsets = (
        ('Product', {
            'fields': ('product',)
        }),
        ('Key Information', {
            'fields': ('key_code',)
        }),
        ('Usage', {
            'fields': ('is_used', 'purchased_by', 'purchased_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(DigitalKeyDelivery)
class DigitalKeyDeliveryAdmin(admin.ModelAdmin):
    list_display = ['order_item', 'key', 'delivered_at']
    list_filter = ['delivered_at']
    search_fields = ['order_item__order__order_number', 'key__key_code']
    readonly_fields = ['delivered_at']
