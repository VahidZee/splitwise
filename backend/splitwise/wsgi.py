"""
WSGI config for splitwise project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import dotenv

try:
    env_file = dotenv.find_dotenv()
    print('loading environment file:', env_file)
    dotenv.load_dotenv(env_file)
except IOError:
    print('environment file not found')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'splitwise.settings')
application = get_wsgi_application()
