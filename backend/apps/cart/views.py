"""
Cart app views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.products.models import Product, ProductVariant


class CartViewSet(viewsets.ModelViewSet):
    """Cart viewset for shopping cart management"""
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    
    def get_queryset(self):
        """Return cart for current user only"""
        return Cart.objects.filter(user=self.request.user)
    
    def get_cart(self):
        """Get or create cart for current user"""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    def list(self, request, *args, **kwargs):
        """Get current user's cart (override list to return single cart)"""
        cart = self.get_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Get current user's cart (alias for list)"""
        cart = self.get_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='add')
    def add_to_cart(self, request):
        """Add item to cart"""
        try:
            product_id = request.data.get('product')
            quantity = int(request.data.get('quantity', 1))
            variant_id = request.data.get('variant')
            
            if not product_id:
                return Response(
                    {'detail': 'Product ID is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if quantity <= 0:
                return Response(
                    {'detail': 'Quantity must be greater than 0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get or create cart
            cart = self.get_cart()
            
            # Get product
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {'detail': 'Product not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get variant if provided
            variant = None
            if variant_id:
                try:
                    variant = ProductVariant.objects.get(id=variant_id, product=product)
                except ProductVariant.DoesNotExist:
                    return Response(
                        {'detail': 'Variant not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            # Check stock
            if product.stock_quantity < quantity:
                return Response(
                    {'detail': f'Only {product.stock_quantity} items available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Add or update cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                variant=variant,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Check if total quantity would exceed stock
                new_quantity = cart_item.quantity + quantity
                if product.stock_quantity < new_quantity:
                    return Response(
                        {'detail': f'Only {product.stock_quantity} items available in total'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                cart_item.quantity = new_quantity
                cart_item.save()
            
            # Return updated cart
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except ValueError:
            return Response(
                {'detail': 'Invalid quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], url_path='clear')
    def clear_cart(self, request):
        """Clear entire cart"""
        cart = self.get_cart()
        cart.items.all().delete()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    def remove_item(self, request, *args, **kwargs):
        """Remove item from cart"""
        cart = self.get_cart()
        item_id = kwargs.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response(
                {'detail': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update_item(self, request, *args, **kwargs):
        """Update cart item quantity"""
        cart = self.get_cart()
        item_id = kwargs.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            quantity = request.data.get('quantity')
            
            if not quantity:
                return Response(
                    {'detail': 'Quantity is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            quantity = int(quantity)
            if quantity <= 0:
                item.delete()
            else:
                # Check stock
                if item.product.stock_quantity < quantity:
                    return Response(
                        {'detail': f'Only {item.product.stock_quantity} items available'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                item.quantity = quantity
                item.save()
            
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response(
                {'detail': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'detail': 'Invalid quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )
