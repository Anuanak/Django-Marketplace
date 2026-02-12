from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    SellerProfile, Category, Product, ProductImage, Cart, CartItem,
    Order, OrderItem, Review, Payment, Wishlist
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class SellerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = SellerProfile
        fields = (
            'id', 'user', 'store_name', 'store_description', 'store_image',
            'phone_number', 'address', 'city', 'state', 'postal_code', 'country',
            'account_balance', 'commission_rate', 'average_rating', 'total_sales',
            'is_verified', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'account_balance', 'created_at', 'updated_at', 'average_rating', 'total_sales')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'icon')
        read_only_fields = ('id',)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'alt_text', 'is_primary')
        read_only_fields = ('id',)


class ProductListSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'price', 'discount_price', 'quantity_in_stock',
            'status', 'average_rating', 'review_count', 'seller', 'category',
            'images', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'description', 'price', 'discount_price',
            'quantity_in_stock', 'weight', 'dimensions', 'sku', 'status',
            'average_rating', 'review_count', 'view_count', 'tags',
            'seller', 'category', 'images', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'view_count', 'created_at', 'updated_at')


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_id', 'quantity', 'total', 'added_at')
        read_only_fields = ('id', 'added_at')
    
    def get_total(self, obj):
        return float(obj.get_total())


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ('id', 'items', 'item_count', 'total_price', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_item_count(self, obj):
        return obj.item_count
    
    def get_total_price(self, obj):
        return float(obj.total_price)


class ReviewSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = (
            'id', 'product', 'buyer', 'rating', 'title', 'comment', 'image',
            'helpful_count', 'unhelpful_count', 'is_verified_purchase',
            'is_approved', 'seller_response', 'seller_response_date',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'helpful_count', 'unhelpful_count', 'created_at', 'updated_at')


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'product_name', 'product_price', 'quantity', 'subtotal')
        read_only_fields = ('id', 'subtotal')


class OrderListSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = (
            'id', 'order_id', 'buyer', 'seller', 'status', 'payment_status',
            'total_amount', 'items', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'order_id', 'created_at', 'updated_at')


class OrderDetailSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = (
            'id', 'order_id', 'buyer', 'seller', 'status', 'payment_status',
            'subtotal', 'shipping_cost', 'tax', 'discount', 'total_amount',
            'shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address',
            'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country',
            'tracking_number', 'courier', 'buyer_notes', 'seller_notes',
            'items', 'created_at', 'updated_at', 'shipped_at', 'delivered_at'
        )
        read_only_fields = ('id', 'order_id', 'created_at', 'updated_at', 'shipped_at', 'delivered_at')


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderListSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = (
            'id', 'order', 'payment_method', 'amount', 'status',
            'transaction_id', 'receipt_url', 'refund_amount', 'refund_reason',
            'created_at', 'updated_at', 'completed_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'completed_at')


class WishlistSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='products',
        many=True,
        write_only=True
    )
    
    class Meta:
        model = Wishlist
        fields = ('id', 'products', 'product_ids', 'created_at')
        read_only_fields = ('id', 'created_at')
