# Django Marketplace - OZON/Wildberries Clone

A full-featured multi-vendor marketplace with support for physical and digital products, user balance system, and multi-language support (Russian, English, Ukrainian).

## Features

- 🛍️ **Multi-Vendor Marketplace** - Sellers can register and manage their products
- 💳 **User Balance System** - Top-up balance and pay with local wallet
- 🔑 **Digital Products** - Automatic delivery of digital keys/codes
- 🌍 **Multi-Language** - Russian, English, Ukrainian support
- ⭐ **Reviews & Ratings** - Product reviews with verified purchase badges
- 🎁 **Promo Codes** - Discount system with percentage/fixed discounts
- 💰 **Commission System** - Marketplace commission on seller sales
- 📦 **Order Management** - Track orders with multiple statuses
- 🔍 **Advanced Search** - Elasticsearch integration for fast product search
- 🛒 **Shopping Cart** - Guest and authenticated user carts
- ❤️ **Wishlist** - Save products for later

## Tech Stack

**Backend:**
- Django 4.2
- Django REST Framework
- PostgreSQL
- Redis (caching & Celery broker)
- Celery (async tasks)
- Elasticsearch (search)
- JWT Authentication

**Frontend:**
- Vue.js 3
- Element Plus UI
- Pinia (state management)
- Vue Router
- Vue I18n (internationalization)
- Axios

## Project Structure

```
Django-Marketplace/
├── backend/
│   ├── apps/
│   │   ├── users/          # User authentication & profiles
│   │   ├── products/       # Products, categories, variants
│   │   ├── cart/           # Shopping cart
│   │   ├── orders/         # Order management
│   │   ├── payments/       # Balance & payments
│   │   ├── digital_keys/   # Digital product keys
│   │   └── reviews/        # Product reviews
│   ├── config/             # Django settings
│   ├── requirements/       # Python dependencies
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Page views
│   │   ├── stores/         # Pinia stores
│   │   ├── services/       # API services
│   │   ├── locales/        # Translations
│   │   └── router/         # Vue Router
│   └── package.json
└── docker-compose.yml
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Elasticsearch 8+ (optional, for search)

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
venv\\Scripts\\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements/development.txt
```

3. Copy environment file:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

4. Update `.env` with your database credentials

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Run with Docker

```bash
docker-compose up -d
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/api/docs/`
- Admin Panel: `http://localhost:8000/admin/`

## Key API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Products
- `GET /api/products/` - List products (with filters)
- `GET /api/products/{slug}/` - Product detail
- `POST /api/products/` - Create product (seller only)
- `PUT /api/products/{slug}/` - Update product (seller only)

### Cart
- `GET /api/cart/` - Get current cart
- `POST /api/cart/add/` - Add item to cart
- `PUT /api/cart/items/{id}/` - Update cart item
- `DELETE /api/cart/items/{id}/` - Remove from cart

### Orders
- `GET /api/orders/` - List user orders
- `POST /api/orders/` - Create order
- `GET /api/orders/{id}/` - Order detail

### Balance
- `GET /api/payments/balance/` - Get balance
- `POST /api/payments/topup/` - Top-up balance
- `GET /api/payments/transactions/` - Transaction history

## User Types

1. **Buyer** - Can browse, purchase products, review
2. **Seller** - Can list products, manage inventory, view seller dashboard
3. **Admin** - Full access to admin panel, approve sellers/products

## Payment Flow

1. User tops up balance via payment gateway (Stripe/YooKassa)
2. Balance is credited to user account
3. User can pay for orders using balance
4. For digital products, keys are automatically delivered
5. Sellers receive payment minus marketplace commission

## Digital Products

Digital products work automatically:
1. Seller uploads digital keys/codes in admin
2. Customer purchases digital product
3. System automatically assigns unused key
4. Key is delivered instantly via email and order details
5. Customer can view purchased keys in account

## Multi-Language Support

The application supports 3 languages:
- Russian (default)
- English
- Ukrainian

Language can be switched in the header. All product names, descriptions, and UI elements are translated.

## Development

### Running Celery Worker (for background tasks)

```bash
cd backend
celery -A config worker -l info
```

### Running Celery Beat (for periodic tasks)

```bash
celery -A config beat -l info
```

### Create Demo Data

```bash
python manage.py create_demo_data
```

## Environment Variables

Key environment variables in `.env`:

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=marketplace_db
DB_USER=postgres
DB_PASSWORD=postgres
REDIS_URL=redis://localhost:6379/0
ELASTICSEARCH_URL=localhost:9200
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please open an issue on GitHub.
