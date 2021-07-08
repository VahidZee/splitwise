"""
WSGI config for splitwise project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'splitwise.settings')
if os.path.isfile('.env'):
    dotenv.load_dotenv('.env')
application = get_wsgi_application()
