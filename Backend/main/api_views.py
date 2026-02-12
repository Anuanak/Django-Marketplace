from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404
from .models import (
    Product, Category, SellerProfile, Cart, CartItem, Order, OrderItem,
    Review, Payment, Wishlist
)
from .serializers import (
    ProductListSerializer, ProductDetailSerializer, CategorySerializer,
    CartSerializer, CartItemSerializer, OrderListSerializer, OrderDetailSerializer,
    ReviewSerializer, SellerProfileSerializer, WishlistSerializer, PaymentSerializer
)


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product Categories.
    
    Endpoints:
    - GET /api/categories/ - List all categories
    - GET /api/categories/{id}/ - Get category details
    - POST /api/categories/ - Create category (admin only)
    - PUT /api/categories/{id}/ - Update category (admin only)
    - DELETE /api/categories/{id}/ - Delete category (admin only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Products.
    
    Endpoints:
    - GET /api/products/ - List all products with filtering
    - GET /api/products/{id}/ - Get product details
    - POST /api/products/ - Create product (sellers only)
    - PUT /api/products/{id}/ - Update product (owner only)
    - DELETE /api/products/{id}/ - Delete product (owner only)
    
    Query Parameters:
    - category: Filter by category slug
    - min_price: Filter by minimum price
    - max_price: Filter by maximum price
    - search: Full-text search on name, description
    - ordering: Sort by name, price, rating, etc.
    """
    queryset = Product.objects.filter(status='active').select_related('seller', 'category').prefetch_related('images')
    serializer_class = ProductListSerializer
    lookup_field = 'slug'
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'category': ['exact'], 'price': ['lt', 'gt']}
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'name', 'created_at', 'average_rating', 'view_count']
    ordering = ['-created_at']
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    @action(detail=True, methods=['get'], url_path='reviews')
    def get_reviews(self, request, slug=None):
        """Get reviews for a product"""
        product = self.get_object()
        reviews = product.reviews.filter(is_approved=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='add-to-cart')
    def add_to_cart(self, request, slug=None):
        """Add product to cart"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        product = self.get_object()
        quantity = int(request.data.get('quantity', 1))
        
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartViewSet(viewsets.ViewSet):
    """
    ViewSet for Shopping Cart.
    
    Endpoints:
    - GET /api/cart/ - Get current user's cart
    - POST /api/cart/add/ - Add item to cart
    - POST /api/cart/remove/ - Remove item from cart
    - PUT /api/cart/update/ - Update cart item quantity
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get current user's cart"""
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Remove item from cart"""
        cart_item_id = request.data.get('cart_item_id')
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()
        return Response({'success': 'Item removed'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """Update cart item quantity"""
        cart_item_id = request.data.get('cart_item_id')
        quantity = int(request.data.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        
        if quantity <= 0:
            cart_item.delete()
            return Response({'success': 'Item removed'})
        
        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Orders.
    
    Endpoints:
    - GET /api/orders/ - List user's orders
    - GET /api/orders/{id}/ - Get order details
    - POST /api/orders/create/ - Create new order
    - PUT /api/orders/{id}/ - Update order (seller only)
    """
    serializer_class = OrderListSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'created_at']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter orders for current user (as buyer or seller)"""
        user = self.request.user
        return Order.objects.filter(
            Q(buyer=user) | Q(seller=user)
        ).select_related('buyer', 'seller').prefetch_related('items')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """Create order from cart"""
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related('product').all()
        
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Group items by seller
        orders_by_seller = {}
        for cart_item in cart_items:
            seller = cart_item.product.seller
            if seller not in orders_by_seller:
                orders_by_seller[seller] = []
            orders_by_seller[seller].append(cart_item)
        
        # Create orders for each seller
        created_orders = []
        for seller, items in orders_by_seller.items():
            subtotal = sum(item.get_total() for item in items)
            shipping_cost = float(request.data.get('shipping_cost', 10.00))
            tax = subtotal * 0.1
            discount = float(request.data.get('discount', 0.00))
            total = subtotal + shipping_cost + tax - discount
            
            order = Order.objects.create(
                buyer=request.user,
                seller=seller,
                status='pending',
                payment_status='unpaid',
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                tax=tax,
                discount=discount,
                total_amount=total,
                shipping_name=request.data.get('shipping_name'),
                shipping_email=request.data.get('shipping_email'),
                shipping_phone=request.data.get('shipping_phone'),
                shipping_address=request.data.get('shipping_address'),
                shipping_city=request.data.get('shipping_city'),
                shipping_state=request.data.get('shipping_state'),
                shipping_postal_code=request.data.get('shipping_postal_code'),
                shipping_country=request.data.get('shipping_country'),
            )
            
            # Create order items
            for cart_item in items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_price=cart_item.product.current_price,
                    quantity=cart_item.quantity,
                )
            
            created_orders.append(order)
        
        # Clear cart
        cart_items.delete()
        
        serializer = OrderListSerializer(created_orders, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product Reviews.
    
    Endpoints:
    - GET /api/reviews/ - List reviews
    - GET /api/reviews/{id}/ - Get review details
    - POST /api/reviews/ - Create review
    - PUT /api/reviews/{id}/ - Update own review
    - DELETE /api/reviews/{id}/ - Delete own review
    """
    serializer_class = ReviewSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'product': ['exact'], 'rating': ['exact']}
    search_fields = ['title', 'comment', 'buyer__username']
    ordering_fields = ['created_at', 'rating', 'helpful_count']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Review.objects.filter(is_approved=True).select_related('product', 'buyer')
    
    def perform_create(self, serializer):
        """Create review for current user"""
        serializer.save(buyer=self.request.user)
        
        # Update product rating
        product = serializer.instance.product
        avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
        product.average_rating = avg_rating or 0
        product.review_count = product.reviews.count()
        product.save()


class SellerProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Seller Profiles.
    
    Endpoints:
    - GET /api/sellers/ - List all sellers
    - GET /api/sellers/{id}/ - Get seller profile
    - GET /api/sellers/{id}/products/ - Get seller's products
    """
    queryset = SellerProfile.objects.filter(is_verified=True)
    serializer_class = SellerProfileSerializer
    lookup_field = 'user__username'
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['store_name', 'user__username']
    ordering_fields = ['average_rating', 'total_sales', 'created_at']
    ordering = ['-average_rating']
    permission_classes = [AllowAny]
    
    @action(detail=True, methods=['get'])
    def products(self, request, user__username=None):
        """Get products from a seller"""
        seller_profile = self.get_object()
        products = seller_profile.user.products.filter(status='active')
        
        paginator = StandardPagination()
        page = paginator.paginate_queryset(products, request)
        serializer = ProductListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class WishlistViewSet(viewsets.ViewSet):
    """
    ViewSet for User Wishlist.
    
    Endpoints:
    - GET /api/wishlist/ - Get user's wishlist
    - POST /api/wishlist/add/ - Add product to wishlist
    - POST /api/wishlist/remove/ - Remove product from wishlist
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get user's wishlist"""
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """Add product to wishlist"""
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
        
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def remove(self, request):
        """Remove product from wishlist"""
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        wishlist = get_object_or_404(Wishlist, user=request.user)
        wishlist.products.remove(product)
        
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
