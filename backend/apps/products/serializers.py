from rest_framework import serializers
from .models import Category, Product, ProductImage, Wishlist, PromoCode


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'icon', 'is_active', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order']


class ProductListSerializer(serializers.ModelSerializer):
    """Simplified product serializer for list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.email', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    discount_percentage = serializers.FloatField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'stock_quantity', 'sku',
            'category', 'category_name', 'seller', 'seller_name', 'is_active',
            'is_approved', 'product_type', 'average_rating', 
            'discount_percentage', 'is_in_stock', 'view_count', 'sold_count',
            'description', 'compare_at_price'
        ]
        read_only_fields = [
            'id', 'slug', 'view_count', 'sold_count', 'is_approved',
            'average_rating', 'discount_percentage', 'is_in_stock', 'seller',
            'seller_name'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full product serializer for detail views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.email', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    discount_percentage = serializers.FloatField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'compare_at_price',
            'sku', 'stock_quantity', 'category', 'category_name', 'seller', 'seller_name',
            'product_type', 'images', 'is_active', 'is_approved', 'sold_count', 
            'view_count', 'average_rating', 'discount_percentage', 'is_in_stock',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'slug', 'view_count', 'sold_count', 'is_approved',
            'created_at', 'updated_at', 'average_rating', 'discount_percentage',
            'is_in_stock', 'seller', 'seller_name'
        ]


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'user', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']
