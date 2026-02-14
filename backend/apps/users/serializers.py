from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User, SellerProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone_number', 'user_type', 'is_verified', 'balance',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if this is an admin user making the request
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if request.user.user_type != 'admin':
                # Regular users can't modify balance and verification status
                self.fields['balance'].read_only = True
                self.fields['is_verified'].read_only = True


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2', 'first_name', 'last_name',
            'phone_number', 'user_type'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        
        # Create seller profile if user type is seller
        if user.user_type == 'seller':
            SellerProfile.objects.create(
                user=user,
                business_name=f"{user.first_name} {user.last_name}'s Store"
            )
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
        
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class SellerProfileSerializer(serializers.ModelSerializer):
    """Serializer for Seller Profile."""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SellerProfile
        fields = [
            'id', 'user', 'user_email', 'user_name', 'business_name',
            'business_type', 'tax_id', 'commission_rate', 'is_approved',
            'rating', 'total_sales', 'address', 'phone', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'rating', 'total_sales', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user serializer with seller profile."""
    seller_profile = SellerProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone_number', 'user_type', 'is_verified', 'balance',
            'date_joined', 'last_login', 'seller_profile'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if this is an admin user making the request
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if request.user.user_type != 'admin':
                # Regular users can't modify balance and verification status
                self.fields['balance'].read_only = True
                self.fields['is_verified'].read_only = True
