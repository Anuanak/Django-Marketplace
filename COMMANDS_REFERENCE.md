# 🛠️ Django Marketplace Commands Reference

## Setup Commands

### Initial Setup
```bash
# Create virtual environment (one-time)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup
```bash
# Navigate to Backend directory
cd Backend

# Create migrations (if models changed)
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Change password for existing user
python manage.py changepassword username

# Create initial data
python manage.py shell < ../setup_sample_data.py
```

## Running the Server

### Development Server
```bash
# Start basic development server (single-threaded)
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run on all network interfaces
python manage.py runserver 0.0.0.0:8000

# Watch file changes (automatic reload)
python manage.py runserver --reload
```

### Production Server
```bash
# With Gunicorn (recommended)
pip install gunicorn
gunicorn Backend.wsgi:application --bind 0.0.0.0:8000

# With Waitress
pip install waitress
waitress-serve --port 8000 Backend.wsgi:application

# With uWSGI
pip install uwsgi
uwsgi --http :8000 --wsgi-file Backend/wsgi.py --master --processes 4 --threads 2
```

## Django Management Commands

### Models & Database
```bash
# Show database table names
python manage.py show_models

# Check for issues
python manage.py check

# Create migrations from model changes
python manage.py makemigrations

# Show SQL for migrations
python manage.py makemigrations --dry-run --verbosity 3

# Apply pending migrations
python manage.py migrate

# Rollback migrations
python manage.py migrate main 0001

# Show migration status
python manage.py showmigrations

# View raw SQL for migration
python manage.py sqlmigrate main 0001
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic --noinput

# Find which static files are used
python manage.py findstatic filename.css

# Clear old static files
python manage.py collectstatic --clear --noinput
```

### User Management
```bash
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username

# Remove user (via shell)
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(username='john').delete()
```

### Shell & Testing
```bash
# Interactive Python shell with Django environment
python manage.py shell

# Run tests
python manage.py test

# Run specific test
python manage.py test main.tests.ProductModelTest

# Run tests with verbosity
python manage.py test --verbosity=2

# Run tests with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Database Queries (Shell)
```bash
python manage.py shell

# Import models
>>> from main.models import Product, SellerProfile, Order
>>> from django.contrib.auth.models import User

# Query examples
>>> Product.objects.all()
>>> Product.objects.filter(status='active').count()
>>> Product.objects.get(id=1)
>>> Product.objects.filter(category__slug='electronics')
>>> User.objects.filter(seller_profile__is_verified=True)
>>> Order.objects.filter(status='delivered')

# Create objects
>>> user = User.objects.create_user(username='john', password='pass123')
>>> SellerProfile.objects.create(user=user, store_name='Johns Store')

# Update objects
>>> product = Product.objects.get(id=1)
>>> product.price = 99.99
>>> product.save()

# Delete objects
>>> Product.objects.filter(status='inactive').delete()
```

## API Testing

### Using curl
```bash
# Get all products
curl http://127.0.0.1:8000/api/v1/products/

# Get specific product
curl http://127.0.0.1:8000/api/v1/products/1/

# List categories
curl http://127.0.0.1:8000/api/v1/categories/

# Get category details
curl http://127.0.0.1:8000/api/v1/categories/electronics/

# Get product reviews
curl http://127.0.0.1:8000/api/v1/products/1/reviews/

# List sellers
curl http://127.0.0.1:8000/api/v1/sellers/

# Get seller profile
curl http://127.0.0.1:8000/api/v1/sellers/electronics_pro/

# Get seller products
curl http://127.0.0.1:8000/api/v1/sellers/electronics_pro/products/
```

### Using Python requests
```python
import requests

# List products
response = requests.get('http://127.0.0.1:8000/api/v1/products/')
products = response.json()

# Get product details
response = requests.get('http://127.0.0.1:8000/api/v1/products/1/')
product = response.json()

# With authentication
headers = {'Authorization': 'Token YOUR_TOKEN_HERE'}
response = requests.get('http://127.0.0.1:8000/api/v1/cart/', headers=headers)
cart = response.json()
```

### Using Postman
1. Import API collection
2. Set base URL: `http://127.0.0.1:8000/api/v1/`
3. For authenticated endpoints, add header:
   ```
   Authorization: Token YOUR_TOKEN_HERE
   ```

## Admin Commands

### Create superuser from command line
```bash
python manage.py createsuperuser --noinput \
  --username admin \
  --email admin@example.com
```

### Bulk operations
```bash
python manage.py shell

# Delete all inactive products
>>> from main.models import Product
>>> Product.objects.filter(status='inactive').delete()

# Update all products price
>>> from decimal import Decimal
>>> Product.objects.all().update(price=99.99)

# Set seller verification
>>> from main.models import SellerProfile
>>> SellerProfile.objects.filter(user__username='john').update(is_verified=True)
```

## Debugging & Logs

### Django Debug Toolbar (install if needed)
```bash
pip install django-debug-toolbar
```

### View detailed logs
```bash
python manage.py runserver --verbose 3
```

### Check for errors
```bash
python manage.py check --deploy  # Production checks
python manage.py check            # Development checks
```

## Performance Commands

### Database query analysis
```bash
python manage.py shell

# Count queries
>>> from django.db import connection
>>> from django.test.utils import CaptureQueriesContext
>>> 
>>> with CaptureQueriesContext(connection) as ctx:
...     products = list(Product.objects.all())
>>> print(f"Queries executed: {len(ctx.captured_queries)}")
```

### Check slow queries
```bash
# Add to settings.py for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Deployment Commands

### Prepare for production
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check for issues
python manage.py check --deploy

# Compile messages
python manage.py compilemessages

# Create database backup
mysqldump -u user -p database > backup.sql
# or for PostgreSQL
pg_dump database > backup.sql
```

### Database migration in production
```bash
# Check for pending migrations
python manage.py showmigrations --plan

# Backup first!
pg_dump database > pre_migration_backup.sql

# Apply migrations
python manage.py migrate --no-input
```

## Useful Shortcuts

### Add to .bashrc or .zshrc (macOS/Linux)
```bash
alias djshell='python manage.py shell'
alias djmigrate='python manage.py migrate'
alias djrun='python manage.py runserver'
alias djtest='python manage.py test'
```

### Windows PowerShell profiles
```powershell
function django-shell { python manage.py shell }
function django-migrate { python manage.py migrate }
function django-run { python manage.py runserver }
function django-test { python manage.py test }
```

## Quick Reference Table

| Command | Purpose |
|---------|---------|
| `python manage.py runserver` | Start dev server |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py makemigrations` | Create migrations from models |
| `python manage.py check` | Check for configuration issues |
| `python manage.py shell` | Interactive Python shell |
| `python manage.py superuser` | Create admin user |
| `python manage.py test` | Run tests |
| `python manage.py collectstatic` | Collect static files |
| `python manage.py changepassword` | Change user password |
| `python manage.py show_models` | List all models |

## Tips & Tricks

### Reset database (development only)
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Speed up tests
```bash
python manage.py test --keepdb
```

### Create test data quickly
```bash
python manage.py shell < setup_sample_data.py
```

### View database in SQLite
```bash
# Install SQLite browser
# Windows: choco install sqlitebrowser
# macOS: brew install sqlitebrowser

# Open database
sqlitebrowser db.sqlite3
```

### Export data
```bash
# Export to JSON
python manage.py dumpdata main > data.json

# Import from JSON
python manage.py loaddata data.json

# Export specific app
python manage.py dumpdata main --indent=2 > main_data.json
```

---

**Happy developing! 🚀**
