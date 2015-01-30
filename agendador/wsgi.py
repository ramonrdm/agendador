"""
WSGI config for agendador project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/home/reservasccs/public_html/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agendador.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
