from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order, OrderItem


@receiver(post_save, sender=Order)
def handle_order_completion(sender, instance, created, **kwargs):
    """
    Handle order completion - trigger digital key delivery.
    """
    if instance.payment_status == 'completed' and instance.has_digital_items:
        from .tasks import deliver_digital_keys
        # Trigger Celery task for digital key delivery
        if settings.DIGITAL_KEY_AUTO_DELIVERY:
            deliver_digital_keys.delay(instance.id)


@receiver(post_save, sender=OrderItem)
def update_product_sold_count(sender, instance, created, **kwargs):
    """
    Update product sold count when order item is created or status changes.
    """
    if created and instance.order.payment_status == 'completed':
        product = instance.product
        product.sold_count += instance.quantity
        product.save(update_fields=['sold_count'])
        
        # Update seller total sales
        if instance.seller and hasattr(instance.seller, 'seller_profile'):
            seller_profile = instance.seller.seller_profile
            seller_profile.total_sales += instance.subtotal
            seller_profile.save(update_fields=['total_sales'])
