from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    product_image = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'product_price', 'product_image',
            'variant', 'quantity', 'total_price', 'added_at'
        ]
        read_only_fields = [
            'id', 'product_name', 'product_price', 'product_image', 
            'total_price', 'added_at'
        ]
    
    def get_product_image(self, obj):
        """Get product image URL"""
        first_image = obj.product.images.first()
        if first_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None
    
    def get_total_price(self, obj):
        """Calculate total price for this item"""
        return float(obj.product.price * obj.quantity)


class CartSerializer(serializers.ModelSerializer):
    """Serializer for shopping cart"""
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'items', 'total_items', 'subtotal',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'items', 'total_items', 'subtotal',
            'created_at', 'updated_at'
        ]
    
    def get_subtotal(self, obj):
        """Calculate cart subtotal"""
        return float(obj.subtotal)
