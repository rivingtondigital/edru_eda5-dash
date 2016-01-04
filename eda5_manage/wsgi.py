"""
WSGI config for eda5_manage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import re

base_path = os.path.abspath(os.path.dirname(__file__) + '/..')

sys.path.append(base_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eda5_manage.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

