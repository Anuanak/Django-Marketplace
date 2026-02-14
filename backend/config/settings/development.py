"""
Development settings for Marketplace project.
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database
# Use SQLite for local development, PostgreSQL for Docker
USE_SQLITE = config('USE_SQLITE', default=True, cast=bool)

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='marketplace_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='postgres'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# CORS Settings for development
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:5177',
    'http://127.0.0.1:5177',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ALLOW_CREDENTIALS = True

# Add debug toolbar for development
INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

# Remove apps that require additional services for simple local dev
if 'django_elasticsearch_dsl' in INSTALLED_APPS:
    INSTALLED_APPS.remove('django_elasticsearch_dsl')
if 'modeltranslation' in INSTALLED_APPS:
    INSTALLED_APPS.remove('modeltranslation')

# Remove whitenoise middleware for local development
MIDDLEWARE = [m for m in MIDDLEWARE if 'whitenoise' not in m.lower()]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Use simple cache backend for local development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
