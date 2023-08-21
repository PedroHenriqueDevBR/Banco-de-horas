import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bancodehoras.settings.prod')
application = get_wsgi_application()
