"""
VentureLens AI - Development Settings
"""

from .base import *  # noqa

DEBUG = True

INSTALLED_APPS += ['django_extensions', 'debug_toolbar']

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

INTERNAL_IPS = ['127.0.0.1']

# Use SQLite for easy dev setup (override DATABASE_URL in .env for PostgreSQL)
# DATABASES already set from base.py via env var

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # disabled: using Resend
