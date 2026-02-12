# 🚀 Quick Start Guide - Django Marketplace

## 30-Second Setup

```bash
# 1. Navigate to project
cd c:\Users\Montenegro\Desktop\proj\Django-Marketplace

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Run migrations (already done, but just in case)
cd Backend
python manage.py migrate

# 4. Start server
python manage.py runserver
```

**Done!** Your marketplace is now running at `http://127.0.0.1:8000`

---

## Access Points

| URL | Purpose | Credentials |
|-----|---------|-------------|
| `http://127.0.0.1:8000/admin/` | Django Admin Panel | admin / admin123 |
| `http://127.0.0.1:8000/products/` | Product Listing (Variant 1) | N/A |
| `http://127.0.0.1:8000/api/v1/` | REST API Root (Variant 2) | Token auth |
| `http://127.0.0.1:8000/api/v1/products/` | API - List Products | N/A |
| `http://127.0.0.1:8000/api/v1/categories/` | API - Categories | N/A |
| `http://127.0.0.1:8000/api/v1/cart/` | API - Shopping Cart | Auth required |
| `http://127.0.0.1:8000/api/v1/orders/` | API - Orders | Auth required |

---

## What's Implemented

### ✅ Core Models (Database)
- **Users & Sellers** - Multi-seller support
- **Products** - With images, categories, pricing
- **Shopping Cart** - Add/remove/update items
- **Orders** - Order management with status tracking
- **Reviews** - 5-star rating system
- **Payments** - Payment record tracking
- **Wishlist** - Save favorite products
- **Notifications** - User notifications

### ✅ Admin Interface
- Beautiful admin panel with color-coded statuses
- Manage products, categories, sellers, orders
- Track seller balances and commission
- Approve/edit reviews with seller responses
- Monitor payments and refunds

### ✅ Variant 1: Traditional Django Views
Complete traditional views for:
- Product listing with search/filter
- Product details with reviews
- Seller profiles
- Shopping cart management
- Checkout and order processing
- Review submission
- Wishlist management
- User dashboard

URL patterns: `/products/`, `/cart/`, `/orders/`, etc.

### ✅ Variant 2: REST API (Django REST Framework)
Full RESTful API endpoints:
- Product management
- Category browsing
- Shopping cart operations
- Order creation and tracking
- Review management
- Seller profiles
- Wishlist operations

API root: `/api/v1/`

---

## Database Schema

### Key Tables
```
Users
├── SellerProfile (store info, balance, rating)
├── Products (linked to seller)
│   └── ProductImages (multiple per product)
├── Reviews (product ratings)
├── Orders (grouped by seller)
│   └── OrderItems (products in order)
├── Cart
│   └── CartItems
├── Wishlist
├── Payment (linked to order)
└── Notifications
```

---

## API Quick Examples

### Get All Products
```bash
curl http://127.0.0.1:8000/api/v1/products/
```

### Get Product Details
```bash
curl http://127.0.0.1:8000/api/v1/products/1/
```

### List Categories
```bash
curl http://127.0.0.1:8000/api/v1/categories/
```

### Get Seller Profile
```bash
curl http://127.0.0.1:8000/api/v1/sellers/username/
```

### Get Reviews for Product
```bash
curl http://127.0.0.1:8000/api/v1/products/1/reviews/
```

---

## Important Files

| File | Purpose |
|------|---------|
| `Backend/Backend/settings.py` | Django configuration |
| `Backend/Backend/urls.py` | URL routing |
| `Backend/main/models.py` | Database models (11 models) |
| `Backend/main/views.py` | Traditional views |
| `Backend/main/api_views.py` | API viewsets |
| `Backend/main/serializers.py` | DRF serializers |
| `Backend/main/admin.py` | Admin customization |
| `Backend/main/urls.py` | Traditional URL patterns |
| `Backend/main/api_urls.py` | API URL patterns |
| `.env` | Environment variables |
| `requirements.txt` | Python dependencies |

---

## Database Tables (Main App)

1. **SellerProfile** - Seller information and balance
2. **Category** - Product categories
3. **Product** - Product listings
4. **ProductImage** - Product images
5. **Cart** - Shopping carts
6. **CartItem** - Items in cart
7. **Order** - Customer orders
8. **OrderItem** - Products in order
9. **Review** - Product reviews
10. **Payment** - Payment records
11. **Wishlist** - Saved products
12. **Notification** - User notifications

---

## Next Steps

### To Add Products:
1. Go to `/admin/` with admin credentials
2. Click **Products** → **Add Product**
3. Fill in details and upload images
4. Save

### To Create Seller Accounts:
1. Create new user in admin
2. Create SellerProfile for that user
3. Set commission rate and store details

### To Test Cart & Orders:
1. Create a regular user (non-seller)
2. Login at `/admin/`
3. View products at `/products/`
4. Add to cart → checkout → place order

### To Test API:
```bash
# List products (no auth needed)
curl http://127.0.0.1:8000/api/v1/products/

# Get single product
curl http://127.0.0.1:8000/api/v1/products/1/

# Get product reviews
curl http://127.0.0.1:8000/api/v1/products/1/reviews/
```

---

## Configuration

### Environment Variables (`.env`)
```env
SECRET_KEY=django-insecure-test-key-...
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional: PostgreSQL (defaults to SQLite)
# POSTGRES_DB=marketplace_db
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=password
# POSTGRES_HOST=localhost

# Optional: Stripe payments
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLIC_KEY=pk_test_...
```

---

## Troubleshooting

### Server won't start?
```bash
# Activate venv and check for errors
python manage.py check
```

### Can't login to admin?
```bash
# Password for admin is: admin123
# Or reset it:
python manage.py changepassword admin
```

### Static files missing?
```bash
python manage.py collectstatic
```

---

## Admin Login
- **URL**: http://127.0.0.1:8000/admin/
- **Username**: admin
- **Password**: admin123

---

## What You Can Do Now

✅ Manage products and inventory  
✅ Create orders and track status  
✅ Monitor seller accounts and balances  
✅ Review and approve customer reviews  
✅ Track payments  
✅ Use REST API for mobile/frontend apps  

---

## Architecture

```
User (Buyer)
    ↓
Browse Products → Add to Cart → Checkout → Place Order
    ↓
Order splits by Seller → Payment → Seller gets notified
    ↓
Seller fulfills → Ships → Order updated
    ↓
Buyer can review → Seller can respond
```

---

## API Response Example

```json
{
  "id": 1,
  "name": "Premium Headphones",
  "slug": "premium-headphones",
  "price": "99.99",
  "discount_price": null,
  "quantity_in_stock": 50,
  "status": "active",
  "average_rating": 4.5,
  "review_count": 12,
  "seller": {
    "id": 2,
    "username": "electronics_store",
    "email": "store@example.com"
  },
  "category": {
    "id": 1,
    "name": "Electronics",
    "slug": "electronics"
  },
  "images": [
    {
      "id": 1,
      "image": "/media/product_images/2026/02/headphones.jpg",
      "alt_text": "Product image",
      "is_primary": true
    }
  ],
  "created_at": "2026-02-12T18:00:00Z"
}
```

---

## Key Features Implemented

| Feature | Status | Location |
|---------|--------|----------|
| Product Management | ✅ | admin / api |
| Multi-Seller Support | ✅ | models.SellerProfile |
| Shopping Cart | ✅ | models.Cart, models.CartItem |
| Orders | ✅ | models.Order, models.OrderItem |
| Payments | ✅ | models.Payment |
| Reviews & Ratings | ✅ | models.Review |
| Product Search | ✅ | views, api_views |
| Seller Profiles | ✅ | models.SellerProfile, api |
| Wishlist | ✅ | models.Wishlist |
| Notifications | ✅ | models.Notification |
| Admin Dashboard | ✅ | admin.py |
| DRF REST API | ✅ | api_views.py |

---

**Everything is ready to use!** Start the server and begin managing your marketplace.
