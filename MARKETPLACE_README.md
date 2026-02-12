# 🛍️ Django Multi-Seller Marketplace

A fully-featured multi-seller marketplace built with Django, featuring dual implementations: **Traditional Django Views + Templates (Variant 1)** and **RESTful API with Django REST Framework (Variant 2)**.

## Features

✅ **Multi-Seller Support** - Multiple vendors can list and sell products  
✅ **Product Management** - Create, update, and manage product listings with multiple images  
✅ **Shopping Cart** - Add/remove items, manage quantities  
✅ **Orders & Payments** - Complete order workflow with payment integration  
✅ **Product Reviews** - 5-star rating system with vendor responses  
✅ **Search & Filtering** - Advanced search by category, price, rating  
✅ **Seller Profiles** - Vendor profiles with stats and balance tracking  
✅ **Wishlist** - Save products for later  
✅ **Admin Dashboard** - Comprehensive admin panel for order and vendor management  
✅ **Dual Implementations** - Use traditional views OR REST API based on your needs  

## Tech Stack

- **Backend**: Django 5.2.11
- **Database**: SQLite (development) / PostgreSQL (production)
- **API**: Django REST Framework
- **Authentication**: Token-based + Session-based
- **Payment**: Stripe integration ready
- **Image Storage**: Pillow for image processing

## Project Structure

```
Backend/
├── manage.py
├── Backend/
│   ├── settings.py          # Configuration
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI config
│   └── asgi.py              # ASGI config
├── main/
│   ├── models.py            # Data models
│   ├── views.py             # Traditional views (Variant 1)
│   ├── api_views.py         # REST API views (Variant 2)
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # Traditional URL patterns
│   ├── api_urls.py          # API URL patterns
│   ├── admin.py             # Admin configuration
│   └── migrations/          # Database migrations
├── static/                  # CSS, JS, images
├── media/                   # User uploaded files
└── db.sqlite3              # Development database
```

## Installation & Setup

### 1. Clone and Setup Environment

```bash
cd Django-Marketplace
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create `.env` file in project root with:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional, uses SQLite if not set)
# POSTGRES_DB=marketplace_db
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=password
# POSTGRES_HOST=localhost

# Stripe (for payments)
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_PUBLIC_KEY=pk_test_your_key
```

### 4. Run Migrations

```bash
cd Backend
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@marketplace.local
# Password: (set your own)
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Access at `http://127.0.0.1:8000`

- **Admin**: http://127.0.0.1:8000/admin
- **API**: http://127.0.0.1:8000/api/v1/

## API Endpoints (Variant 2)

### Base URL: `/api/v1/`

### Products
- `GET /products/` - List all products
- `GET /products/{id}/` - Get product details
- `GET /products/{id}/reviews/` - Get product reviews
- `POST /products/{id}/add-to-cart/` - Add to cart

### Categories
- `GET /categories/` - List all categories
- `GET /categories/{slug}/` - Get category details

### Cart
- `GET /cart/` - View cart
- `POST /cart/add_item/` - Add item to cart
- `POST /cart/remove_item/` - Remove item from cart
- `POST /cart/update_item/` - Update item quantity

### Orders
- `GET /orders/` - List user's orders
- `GET /orders/{id}/` - Get order details
- `POST /orders/create_order/` - Create order from cart

### Reviews
- `GET /reviews/` - List reviews
- `POST /reviews/` - Create review
- `PUT /reviews/{id}/` - Update review
- `DELETE /reviews/{id}/` - Delete review

### Sellers
- `GET /sellers/` - List sellers
- `GET /sellers/{username}/` - Get seller profile
- `GET /sellers/{username}/products/` - Get seller's products

### Wishlist
- `GET /wishlist/` - View wishlist
- `POST /wishlist/add/` - Add to wishlist
- `POST /wishlist/remove/` - Remove from wishlist

## Data Models

### User Models
- **User** - Django built-in user model
- **SellerProfile** - Extended seller information (store name, balance, rating)

### Product Models
- **Category** - Product categories
- **Product** - Product listings
- **ProductImage** - Product images (multiple per product)

### Shopping Models
- **Cart** - User shopping cart
- **CartItem** - Items in cart
- **Wishlist** - Saved products

### Order Models
- **Order** - Customer orders (grouped by seller)
- **OrderItem** - Individual items in an order
- **Payment** - Payment records

### Review Models
- **Review** - Product reviews with ratings

### Misc Models
- **Notification** - User notifications

## Admin Panel

Access `/admin/` with superuser credentials to:

- Manage products and categories
- View and process orders
- Monitor seller accounts and balances
- Manage reviews and ratings
- Track payments
- User management

### Admin Features
- **Color-coded order status badges**
- **Product image previews**
- **Seller balance tracking**
- **Review management with seller responses**
- **Payment status indicators**

## Authentication

### Token Authentication (API)
```bash
POST /api/v1/api-token-auth/
{
  "username": "seller1",
  "password": "password123"
}
```

Response:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

Include token in headers:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Session Authentication (Traditional Views)
Login at `/admin/login` or through view-based login.

## Usage Examples

### Example 1: Create a Product (as Seller)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/products/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "name=Premium Headphones" \
  -F "price=99.99" \
  -F "category=electronics" \
  -F "description=High quality audio" \
  -F "quantity_in_stock=50"
```

### Example 2: Add Product to Cart
```bash
curl -X POST http://127.0.0.1:8000/api/v1/cart/add_item/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### Example 3: Create Order
```bash
curl -X POST http://127.0.0.1:8000/api/v1/orders/create_order/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "shipping_name": "John Doe",
    "shipping_email": "john@example.com",
    "shipping_phone": "1234567890",
    "shipping_address": "123 Main St",
    "shipping_city": "New York",
    "shipping_state": "NY",
    "shipping_postal_code": "10001",
    "shipping_country": "USA"
  }'
```

## Configuration

### Settings File: `Backend/Backend/settings.py`

Key configurations:

```python
# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS for frontend apps
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# File Upload
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
```

## Testing

Run tests with:
```bash
python manage.py test
```

## Production Deployment

### Create production `.env`:
```env
SECRET_KEY=generate-secure-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

POSTGRES_DB=marketplace_prod
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password
POSTGRES_HOST=db.example.com
POSTGRES_PORT=5432
```

### Deploy with Gunicorn:
```bash
pip install gunicorn
gunicorn Backend.wsgi:application --bind 0.0.0.0:8000
```

### Use PostgreSQL in production:
1. Set `POSTGRES_*` environment variables
2. Run migrations: `python manage.py migrate`
3. Collect static files: `python manage.py collectstatic`

## API Documentation

### Query Parameters

**Products**
```
GET /api/v1/products/?search=headphones&category=electronics&min_price=50&max_price=200&ordering=-price
```

**Orders**
```
GET /api/v1/orders/?status=pending&payment_status=paid
```

**Reviews**
```
GET /api/v1/reviews/?product=1&rating=5
```

### Pagination
```
GET /api/v1/products/?page=1&page_size=20
```

## Performance Optimization

- Products are prefetched with related data (seller, images, reviews)
- Database indexes on frequently filtered fields
- Pagination to limit large result sets
- Select/prefetch related queries to minimize N+1 problems

## Security

- ✅ CSRF protection enabled
- ✅ SQL injection protection (ORM)
- ✅ XSS protection
- ✅ Secure password hashing
- ✅ Token authentication with expiration ready
- ✅ Permission checks on sensitive operations

⚠️ **Note**: This is a development template. For production:
1. Set `DEBUG=False`
2. Use strong `SECRET_KEY`
3. Enable HTTPS
4. Use PostgreSQL
5. Set up proper authentication (JWT, OAuth)
6. Configure email backend
7. Set up Celery for async tasks

## Roadmap

- [ ] JWT authentication
- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Email notifications
- [ ] Seller dashboard with analytics
- [ ] Inventory management
- [ ] Product variants and options
- [ ] Promotional codes and discounts
- [ ] Advanced search with Elasticsearch
- [ ] Real-time notifications with WebSockets
- [ ] Mobile app support
- [ ] Seller ratings and reviews

## Troubleshooting

### ModuleNotFoundError
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Issues
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit a pull request

## License

MIT License - feel free to use this for personal or commercial projects.

## Support

For issues and questions, please open an issue on the repository.

---

**Made with ❤️ using Django**

Built as a complete marketplace solution with dual implementations for maximum flexibility.
