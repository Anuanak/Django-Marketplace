from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q, Avg, Count, F
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from .models import (
    Product, Category, SellerProfile, Cart, CartItem, Order, OrderItem,
    Review, Payment, Wishlist
)


# ==================== HOME VIEWS ====================

def home(request):
    """Display home page with featured products"""
    # Prefer products on sale; fall back to most recent active products
    featured_products = Product.objects.filter(status='active', discount_price__isnull=False).order_by('-created_at')[:8]
    if not featured_products:
        featured_products = Product.objects.filter(status='active').order_by('-created_at')[:8]
    # Popular products by view count
    popular_products = Product.objects.filter(status='active').order_by('-view_count')[:8]
    
    context = {
        'featured_products': featured_products,
        'popular_products': popular_products,
    }
    return render(request, 'main/index.html', context)


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('main:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    context = {'is_login': True}
    return render(request, 'main/auth.html', context)


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'main/auth.html', {'is_login': False})
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'main/auth.html', {'is_login': False})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('main:home')
    
    context = {'is_login': False}
    return render(request, 'main/auth.html', context)


def logout_view(request):
    """User logout"""
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('main:home')


# ==================== PRODUCT VIEWS ====================

def product_list(request):
    """Display all products with filtering and search"""
    products = Product.objects.filter(status='active').select_related('seller', 'category')
    
    # Search (template uses `search` param)
    query = request.GET.get('search')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Category filter (template sends category id)
    category = request.GET.get('category')
    if category:
        products = products.filter(category__id=category)
    
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = ['price', '-price', 'name', '-created_at', '-review_count', '-average_rating']
    if sort in valid_sorts:
        products = products.order_by(sort)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'products': page_obj,  # template expects `products`
        'categories': categories,
        'query': query,
        'selected_category': category,
    }
    return render(request, 'main/product_list.html', context)


def product_detail(request, slug):
    """Display product details"""
    product = get_object_or_404(Product, slug=slug, status='active')
    reviews = product.reviews.filter(is_approved=True).select_related('buyer')
    seller = product.seller
    related_products = Product.objects.filter(
        category=product.category,
        status='active'
    ).exclude(id=product.id)[:6]
    
    product.view_count += 1
    product.save(update_fields=['view_count'])
    
    context = {
        'product': product,
        'reviews': reviews,
        'seller': seller,
        'related_products': related_products,
    }
    
    if request.user.is_authenticated:
        # User may not have a wishlist yet; guard against RelatedObjectDoesNotExist
        try:
            context['is_in_wishlist'] = request.user.wishlist.products.filter(id=product.id).exists()
        except Exception:
            # Ensure a wishlist exists for the user to avoid runtime errors
            Wishlist.objects.get_or_create(user=request.user)
            context['is_in_wishlist'] = False
    
    return render(request, 'main/product_detail.html', context)


# ==================== SELLER VIEWS ====================

def seller_profile(request, username):
    """Display seller profile and their products"""
    seller = get_object_or_404(User, username=username)
    seller_profile = get_object_or_404(SellerProfile, user=seller)
    products = seller.products.filter(status='active')
    reviews = Review.objects.filter(product__seller=seller, is_approved=True)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'seller_profile': seller_profile,
        'seller': seller,
        'page_obj': page_obj,
        'reviews': reviews,
    }
    return render(request, 'main/seller_profile.html', context)


# ==================== CART VIEWS ====================

@login_required(login_url='admin:login')
def view_cart(request):
    """Display shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product')
    # Compute monetary summary values for the template
    subtotal = cart.total_price
    shipping_cost = 10.00
    tax = subtotal * 0.1
    grand_total = subtotal + shipping_cost + tax

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'main/cart.html', context)


@login_required(login_url='admin:login')
@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, status='active')
    quantity = int(request.POST.get('quantity', 1))
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('main:view_cart')


@login_required(login_url='admin:login')
@require_POST
def remove_from_cart(request, cart_item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('main:view_cart')


@login_required(login_url='admin:login')
@require_POST
def update_cart_item(request, cart_item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    else:
        if quantity > cart_item.product.quantity_in_stock:
            messages.error(request, f'Only {cart_item.product.quantity_in_stock} available.')
            quantity = cart_item.product.quantity_in_stock
        
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated.')
    
    return redirect('main:view_cart')


# ==================== CHECKOUT & ORDER VIEWS ====================

@login_required(login_url='admin:login')
def checkout(request):
    """Checkout page"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product')
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('main:view_cart')
    # Compute summary values for display
    subtotal = cart.total_price
    shipping_cost = 10.00
    tax = subtotal * 0.1
    total = subtotal + shipping_cost + tax

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax': tax,
        'total': total,
    }
    return render(request, 'main/checkout.html', context)


@login_required(login_url='admin:login')
@require_POST
def process_order(request):
    """Process order from cart"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    if not cart_items.exists():
        return JsonResponse({'error': 'Cart is empty'}, status=400)
    
    # Get shipping info
    shipping_name = request.POST.get('shipping_name')
    shipping_email = request.POST.get('shipping_email')
    shipping_phone = request.POST.get('shipping_phone')
    shipping_address = request.POST.get('shipping_address')
    shipping_city = request.POST.get('shipping_city')
    shipping_state = request.POST.get('shipping_state')
    shipping_postal_code = request.POST.get('shipping_postal_code')
    shipping_country = request.POST.get('shipping_country')
    
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
        shipping_cost = 10.00  # Fixed shipping cost for demo
        tax = subtotal * 0.1  # 10% tax
        discount = 0.00
        total = subtotal + shipping_cost + tax - discount
        
        order = Order.objects.create(
            buyer=request.user,
            seller=seller,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            discount=discount,
            total_amount=total,
            shipping_name=shipping_name,
            shipping_email=shipping_email,
            shipping_phone=shipping_phone,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_postal_code=shipping_postal_code,
            shipping_country=shipping_country,
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
    
    messages.success(request, f'Order(s) placed successfully!')
    return redirect('main:order_list')


@login_required(login_url='admin:login')
def order_list(request):
    """List user's orders"""
    orders = Order.objects.filter(buyer=request.user).select_related('seller').prefetch_related('items')
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'main/order_list.html', context)


@login_required(login_url='admin:login')
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, order_id=order_id)
    
    # Check if user is buyer or seller
    if request.user != order.buyer and request.user != order.seller:
        return HttpResponseForbidden('You do not have permission to view this order.')
    
    order_items = order.items.select_related('product')
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'main/order_detail.html', context)


# ==================== REVIEW VIEWS ====================

@login_required(login_url='admin:login')
def add_review(request, product_id):
    """Add review to product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        
        review, created = Review.objects.update_or_create(
            product=product,
            buyer=request.user,
            defaults={
                'rating': rating,
                'title': title,
                'comment': comment,
                'is_verified_purchase': Order.objects.filter(
                    buyer=request.user,
                    items__product=product,
                    status__in=['delivered', 'shipped']
                ).exists()
            }
        )
        
        # Update product average rating
        avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
        product.average_rating = avg_rating or 0
        product.review_count = product.reviews.count()
        product.save()
        
        messages.success(request, 'Review added successfully!')
        return redirect('main:product_detail', slug=product.slug)
    
    context = {
        'product': product,
    }
    return render(request, 'main/add_review.html', context)


# ==================== WISHLIST VIEWS ====================

@login_required(login_url='admin:login')
def wishlist(request):
    """Display user's wishlist"""
    wishlist_obj, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist_obj.products.all()
    
    context = {
        'wishlist': wishlist_obj,
        'products': products,
    }
    return render(request, 'main/wishlist.html', context)


@login_required(login_url='admin:login')
@require_POST
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id)
    wishlist_obj, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_obj.products.add(product)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'added'})
    
    messages.success(request, f'{product.name} added to wishlist!')
    return redirect('main:product_detail', slug=product.slug)


@login_required(login_url='admin:login')
@require_POST
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    product = get_object_or_404(Product, id=product_id)
    wishlist_obj = get_object_or_404(Wishlist, user=request.user)
    wishlist_obj.products.remove(product)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'removed'})
    
    messages.success(request, f'{product.name} removed from wishlist.')
    return redirect('main:product_detail', slug=product.slug)


# ==================== DASHBOARD VIEWS ====================

@login_required(login_url='admin:login')
def dashboard(request):
    """User dashboard"""
    # Check if user is a seller
    try:
        seller_profile = request.user.seller_profile
        is_seller = True
    except:
        seller_profile = None
        is_seller = False
    
    # Get buyer stats
    orders = Order.objects.filter(buyer=request.user)
    reviews_given = Review.objects.filter(buyer=request.user)
    
    context = {
        'is_seller': is_seller,
        'seller_profile': seller_profile,
        'orders_count': orders.count(),
        'reviews_count': reviews_given.count(),
    }
    
    # Add seller stats if applicable
    if is_seller:
        seller_orders = Order.objects.filter(seller=request.user)
        context.update({
            'seller_orders_count': seller_orders.count(),
            'seller_products_count': request.user.products.count(),
            'account_balance': seller_profile.account_balance,
        })
    
    return render(request, 'main/dashboard.html', context)
