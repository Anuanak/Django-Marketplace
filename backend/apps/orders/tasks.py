from celery import shared_task
from django.db import transaction
from django.utils import timezone


@shared_task
def deliver_digital_keys(order_id):
    """
    Automatically deliver digital keys for completed orders.
    """
    from apps.orders.models import Order, OrderItem
    from apps.digital_keys.models import DigitalKey, DigitalKeyDelivery
    
    try:
        order = Order.objects.get(id=order_id)
        
        for item in order.items.filter(is_digital=True):
            # Check if key already delivered
            if hasattr(item, 'digital_key_delivery'):
                continue
            
            # Find an unused key for this product
            with transaction.atomic():
                available_key = DigitalKey.objects.select_for_update().filter(
                    product=item.product,
                    is_used=False
                ).first()
                
                if available_key:
                    # Mark the key as used
                    available_key.is_used = True
                    available_key.purchased_by = order.user
                    available_key.purchased_at = timezone.now()
                    available_key.save()
                    
                    # Create delivery record
                    DigitalKeyDelivery.objects.create(
                        order_item=item,
                        key=available_key
                    )
                    
                    # TODO: Send email notification with the digital key
                    send_digital_key_email.delay(order.user.email, item.product_name, available_key.key_code)
        
        return f"Digital keys delivered for order #{order.order_number}"
    
    except Order.DoesNotExist:
        return f"Order {order_id} not found"
    except Exception as e:
        return f"Error delivering digital keys: {str(e)}"


@shared_task
def send_digital_key_email(user_email, product_name, key_code):
    """
    Send email with digital key to customer.
    """
    from django.core.mail import send_mail
    from django.conf import settings
    
    subject = f'Your Digital Key for {product_name}'
    message = f'''
    Thank you for your purchase!
    
    Product: {product_name}
    Your Key/Code: {key_code}
    
    You can view your purchased keys in your account dashboard.
    
    Best regards,
    Marketplace Team
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )
        return f"Email sent to {user_email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"


@shared_task
def send_order_confirmation_email(order_id):
    """
    Send order confirmation email to customer.
    """
    from apps.orders.models import Order
    from django.core.mail import send_mail
    from django.conf import settings
    
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Order Confirmation - #{order.order_number}'
        message = f'''
        Thank you for your order!
        
        Order Number: {order.order_number}
        Total Amount: ${order.final_amount}
        Status: {order.get_status_display()}
        
        You can track your order in your account dashboard.
        
        Best regards,
        Marketplace Team
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            fail_silently=False,
        )
        return f"Confirmation email sent for order #{order.order_number}"
    except Exception as e:
        return f"Error sending confirmation email: {str(e)}"
