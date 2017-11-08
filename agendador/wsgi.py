import os
import sys
from django.core.wsgi import get_wsgi_application

#sys.path.append('/home/reservasccs/public_html/')
sys.path.append('/var/www/html/agendador')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agendador.settings")
application = get_wsgi_application()
