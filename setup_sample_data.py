#!/usr/bin/env python
"""
Django Management Command: Load Sample Data

This script populates the marketplace with sample data for testing.

Usage:
    python manage.py shell < setup_sample_data.py

Or directly in Python shell:
    python manage.py shell
    exec(open('setup_sample_data.py').read())
"""

from django.contrib.auth.models import User
from main.models import (
    SellerProfile, Category, Product, ProductImage, 
    Review, Cart, Order, OrderItem, Payment
)
from decimal import Decimal
from django.utils import timezone

# ==================== SETUP SAMPLE DATA ====================

print("🚀 Setting up sample marketplace data...\n")

# 1. Create Categories
print("📦 Creating categories...")
categories = [
    Category.objects.get_or_create(
        name='Electronics',
        defaults={'slug': 'electronics', 'description': 'Electronic devices and gadgets'}
    ),
    Category.objects.get_or_create(
        name='Clothing',
        defaults={'slug': 'clothing', 'description': 'Apparel and fashion items'}
    ),
    Category.objects.get_or_create(
        name='Books',
        defaults={'slug': 'books', 'description': 'Books and reading materials'}
    ),
    Category.objects.get_or_create(
        name='Home & Garden',
        defaults={'slug': 'home-garden', 'description': 'Home and garden products'}
    ),
]
print(f"✅ Created {len([c for c, _ in categories])} categories\n")

# 2. Create Sellers
print("👥 Creating seller accounts...")
sellers = []
seller_data = [
    {'username': 'electronics_pro', 'email': 'electronics@store.com', 'store': 'Tech Store'},
    {'username': 'fashion_hub', 'email': 'fashion@store.com', 'store': 'Fashion Hub'},
    {'username': 'book_world', 'email': 'books@store.com', 'store': 'Book World'},
    {'username': 'home_depot', 'email': 'home@store.com', 'store': 'Home Depot'},
]

for data in seller_data:
    user, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['store'],
            'is_staff': False
        }
    )
    if created:
        user.set_password('seller123')
        user.save()
    
    seller_profile, _ = SellerProfile.objects.get_or_create(
        user=user,
        defaults={
            'store_name': data['store'],
            'store_description': f"Welcome to {data['store']}! We offer quality products.",
            'is_verified': True,
            'commission_rate': Decimal('10.00'),
            'account_balance': Decimal('1000.00'),
            'average_rating': Decimal('4.5'),
        }
    )
    sellers.append(user)

print(f"✅ Created {len(sellers)} seller accounts\n")

# 3. Create Sample Products
print("📱 Creating sample products...")
products_data = [
    {
        'seller': sellers[0],
        'category': categories[0][0],
        'name': 'Wireless Bluetooth Headphones',
        'price': Decimal('79.99'),
        'discount_price': Decimal('59.99'),
        'quantity': 50,
        'description': 'High-quality wireless headphones with noise cancellation. Perfect for music lovers and professionals.',
    },
    {
        'seller': sellers[0],
        'category': categories[0][0],
        'name': 'USB-C Fast Charger',
        'price': Decimal('29.99'),
        'quantity': 100,
        'description': '65W USB-C fast charger compatible with most modern devices.',
    },
    {
        'seller': sellers[0],
        'category': categories[0][0],
        'name': 'Laptop Stand',
        'price': Decimal('44.99'),
        'discount_price': Decimal('34.99'),
        'quantity': 30,
        'description': 'Ergonomic aluminum laptop stand for comfortable working.',
    },
    {
        'seller': sellers[1],
        'category': categories[1][0],
        'name': 'Cotton T-Shirt',
        'price': Decimal('19.99'),
        'quantity': 200,
        'description': '100% organic cotton comfortable everyday t-shirt.',
    },
    {
        'seller': sellers[1],
        'category': categories[1][0],
        'name': 'Denim Jeans',
        'price': Decimal('59.99'),
        'discount_price': Decimal('39.99'),
        'quantity': 75,
        'description': 'Classic blue denim jeans, perfect fit and comfort.',
    },
    {
        'seller': sellers[2],
        'category': categories[2][0],
        'name': 'Python Programming Book',
        'price': Decimal('39.99'),
        'quantity': 40,
        'description': 'Learn Python programming from basics to advanced concepts.',
    },
    {
        'seller': sellers[2],
        'category': categories[2][0],
        'name': 'Django Web Development',
        'price': Decimal('49.99'),
        'quantity': 25,
        'description': 'Master Django web framework with practical examples.',
    },
    {
        'seller': sellers[3],
        'category': categories[3][0],
        'name': 'LED Desk Lamp',
        'price': Decimal('34.99'),
        'quantity': 60,
        'description': 'Energy-efficient LED desk lamp with adjustable brightness.',
    },
]

products = []
for data in products_data:
    product, created = Product.objects.get_or_create(
        name=data['name'],
        seller=data['seller'],
        defaults={
            'category': data['category'],
            'slug': data['name'].lower().replace(' ', '-'),
            'description': data['description'],
            'price': data['price'],
            'discount_price': data.get('discount_price'),
            'quantity_in_stock': data['quantity'],
            'status': 'active',
            'average_rating': Decimal('4.3'),
        }
    )
    if created:
        products.append(product)

print(f"✅ Created {len(products)} products\n")

# 4. Create Sample Reviews
print("⭐ Creating sample reviews...")
review_data = [
    {'product': 0, 'rating': 5, 'title': 'Great quality!', 'comment': 'Love these headphones, amazing sound quality.'},
    {'product': 0, 'rating': 4, 'title': 'Good value', 'comment': 'Good product but a bit pricey.'},
    {'product': 1, 'rating': 5, 'title': 'Fast charging', 'comment': 'Charges my phone super fast!'},
    {'product': 4, 'rating': 4, 'title': 'Comfortable fit', 'comment': 'Super comfortable and looks great.'},
    {'product': 6, 'rating': 5, 'title': 'Perfect for learning', 'comment': 'Great book for Django beginners!'},
]

reviews_created = 0
for data in review_data:
    # Create a test user for reviews
    buyer, _ = User.objects.get_or_create(
        username=f'buyer_{reviews_created}',
        defaults={'email': f'buyer{reviews_created}@example.com'}
    )
    if not buyer.has_usable_password():
        buyer.set_password('buyer123')
        buyer.save()
    
    Review.objects.get_or_create(
        product=products[data['product']],
        buyer=buyer,
        defaults={
            'rating': data['rating'],
            'title': data['title'],
            'comment': data['comment'],
            'is_verified_purchase': True,
            'is_approved': True,
        }
    )
    reviews_created += 1

print(f"✅ Created {reviews_created} reviews\n")

# 5. Create Sample Regular Users
print("👤 Creating regular customer accounts...")
customers = []
for i in range(3):
    customer, created = User.objects.get_or_create(
        username=f'customer_{i+1}',
        defaults={
            'email': f'customer{i+1}@example.com',
            'first_name': f'Customer {i+1}',
        }
    )
    if created:
        customer.set_password('customer123')
        customer.save()
    customers.append(customer)
    
    # Create cart for each customer
    Cart.objects.get_or_create(user=customer)

print(f"✅ Created {len(customers)} customer accounts\n")

# 6. Create Sample Orders
print("📦 Creating sample orders...")
orders_created = 0
if len(customers) > 0 and len(products) > 0:
    customer = customers[0]
    product = products[0]
    seller = product.seller
    
    order, created = Order.objects.get_or_create(
        buyer=customer,
        seller=seller,
        status='delivered',
        defaults={
            'subtotal': Decimal('119.98'),
            'shipping_cost': Decimal('10.00'),
            'tax': Decimal('13.20'),
            'discount': Decimal('0.00'),
            'total_amount': Decimal('143.18'),
            'shipping_name': customer.first_name,
            'shipping_email': customer.email,
            'shipping_phone': '555-0123',
            'shipping_address': '123 Main St',
            'shipping_city': 'New York',
            'shipping_state': 'NY',
            'shipping_postal_code': '10001',
            'shipping_country': 'USA',
            'payment_status': 'paid',
            'created_at': timezone.now(),
        }
    )
    
    if created:
        # Add order items
        OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={
                'product_name': product.name,
                'product_price': product.current_price,
                'quantity': 2,
            }
        )
        
        # Create payment
        Payment.objects.get_or_create(
            order=order,
            defaults={
                'payment_method': 'credit_card',
                'amount': order.total_amount,
                'status': 'completed',
                'transaction_id': 'txn_test_123456',
            }
        )
        orders_created += 1

print(f"✅ Created {orders_created} orders\n")

# 7. Print Summary
print("=" * 50)
print("✅ SAMPLE DATA SETUP COMPLETE!")
print("=" * 50)
print("\n📊 Created:")
print(f"  • {len(categories)} product categories")
print(f"  • {len(sellers)} seller accounts")
print(f"  • {len(products)} products")
print(f"  • {reviews_created} product reviews")
print(f"  • {len(customers)} customer accounts")
print(f"  • {orders_created} sample orders")

print("\n🔐 Test Credentials:")
print("\n  Admin Account:")
print("    Username: admin")
print("    Password: admin123")

print("\n  Seller Accounts:")
for data in seller_data:
    print(f"    Username: {data['username']}")
    print(f"    Password: seller123")

print("\n  Customer Accounts:")
for i in range(len(customers)):
    print(f"    Username: customer_{i+1}")
    print(f"    Password: customer123")

print("\n🌐 Access Points:")
print("  • Admin: http://127.0.0.1:8000/admin/")
print("  • Products: http://127.0.0.1:8000/products/")
print("  • API: http://127.0.0.1:8000/api/v1/")

print("\n✨ You're all set! Start the server and explore the marketplace.\n")
