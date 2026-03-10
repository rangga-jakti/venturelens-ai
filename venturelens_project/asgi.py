"""
VentureLens AI - ASGI Configuration
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'venturelens_project.settings.development')
application = get_asgi_application()
